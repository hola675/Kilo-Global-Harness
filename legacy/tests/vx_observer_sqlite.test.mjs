// component_version: 1.0.1
// last_modified: 2026-11-23
// Execute Kilo hook adapter in isolated Bun child; only parent reads SQLite.
// Windows requires child process exit to release the adapter's DB handle.
import { test, expect } from "bun:test"
import { Database } from "bun:sqlite"
import { mkdtempSync, existsSync, rmSync } from "node:fs"
import { tmpdir } from "node:os"
import { join } from "node:path"
import { spawnSync } from "node:child_process"
import { fileURLToPath } from "node:url"

const secret = "NEVER_PERSIST_PRIVATE_CONTENT"
const sessionID = "private_session_0123"
const callID = "private_call_0456"

if (process.argv.includes("--vx-worker")) {
  const { default: plugin } = await import("../runtime/kilo-observer/vx-runtime-observer.js")
  const hooks = await plugin.server({
    directory: join(process.env.VX_OBSERVER_LAB_PARENT, "vx-observer-lab"),
  })
  if (typeof hooks["tool.execute.before"] !== "function") {
    throw new Error("observer hook not enabled in isolated worker")
  }
  const call = { tool: "task", sessionID, callID,
                 args: { secret }, output: { content: secret } }
  await hooks["tool.execute.before"](call, { args: call.args })
  await hooks["tool.execute.after"](call, { output: call.output })
  await hooks["tool.execute.after"](call, { output: call.output })
  await hooks.event({ event: { type: "session.updated", properties: { sessionID } } })
  await hooks["tool.execute.before"]({ ...call, tool: "bash" })
  const wrong = await plugin.server({
    directory: join(process.env.VX_OBSERVER_LAB_PARENT, "vecidya"),
  })
  if (Object.keys(wrong).length !== 0) throw new Error("observer accepted another project")
} else {
  test("Bun SQLite real: hooks idempotentes, sin datos privados ni cambios a DAG", () => {
    const root = mkdtempSync(join(tmpdir(), "vx-observer-bun-ci-"))
    try {
      const env = {
        ...process.env,
        VX_OBSERVER_ENABLE: "1",
        VX_OBSERVER_PROJECT: "vx-observer-lab",
        VX_OBSERVER_LAB_PARENT: root,
        VX_OBSERVER_STATE_ROOT: join(root, "state"),
      }
      const execution = spawnSync(process.execPath,
        [fileURLToPath(import.meta.url), "--vx-worker"],
        { env, encoding: "utf8", timeout: 20000 })
      expect(execution.status).toBe(0)
      if (execution.status !== 0) {
        throw new Error("Child hook failed: " + execution.stderr)
      }
      const dbpath = join(root, "state", "vx-runtime-observations.sqlite3")
      expect(existsSync(dbpath)).toBe(true)
      const db = new Database(dbpath, { readonly: true })
      try {
        expect(db.query("PRAGMA integrity_check").get().integrity_check).toBe("ok")
        expect(db.query("PRAGMA user_version").get().user_version).toBe(1)
        const rows = db.query("SELECT * FROM host_observations ORDER BY event_type").all()
        expect(rows).toHaveLength(3)
        expect(rows.map((row) => row.event_type)).toEqual([
          "TOOL_CALLED_NOT_CONFIRMED", "TOOL_RETURNED_NOT_VERIFIED", "session.updated",
        ])
        expect(rows.every((row) => row.project === "vx-observer-lab")).toBe(true)
        const serialized = JSON.stringify(rows)
        for (const privateText of [secret, sessionID, callID]) {
          expect(serialized.includes(privateText)).toBe(false)
        }
        expect(existsSync(join(root, "vx-team-queue.sqlite3"))).toBe(false)
      } finally { db.close() }
    } finally {
      rmSync(root, { recursive: true, force: true })
    }
  })
}
