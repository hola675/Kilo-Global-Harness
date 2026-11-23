// component_version: 1.0.0
// last_modified: 2026-11-23
// Requires Bun only in isolated CI/test lab; never invokes Kilo runtime.
import { test, expect } from "bun:test"
import { Database } from "bun:sqlite"
import { mkdtempSync, existsSync, rmSync } from "node:fs"
import { tmpdir } from "node:os"
import { join } from "node:path"

test("isolated Bun SQLite persists filtered real hook callbacks, not task claims", async () => {
  const root = mkdtempSync(join(tmpdir(), "vx-observer-bun-ci-"))
  const before = {
    VX_OBSERVER_ENABLE: process.env.VX_OBSERVER_ENABLE,
    VX_OBSERVER_PROJECT: process.env.VX_OBSERVER_PROJECT,
    VX_OBSERVER_STATE_ROOT: process.env.VX_OBSERVER_STATE_ROOT,
  }
  try {
    process.env.VX_OBSERVER_ENABLE = "1"
    process.env.VX_OBSERVER_PROJECT = "vx-observer-lab"
    process.env.VX_OBSERVER_STATE_ROOT = join(root, "state")
    const { default: plugin } = await import("../runtime/kilo-observer/vx-runtime-observer.js")
    const hooks = await plugin.server({ directory: join(root, "vx-observer-lab") })
    expect(typeof hooks["tool.execute.before"]).toBe("function")
    const token = "NEVER_PERSIST_PRIVATE_CONTENT"
    const call = {
      tool: "task", sessionID: "private_session_0123", callID: "private_call_0456",
      args: { secret: token }, output: { content: token },
    }
    await hooks["tool.execute.before"](call, { args: call.args })
    await hooks["tool.execute.after"](call, { output: call.output })
    await hooks["tool.execute.after"](call, { output: call.output })
    await hooks.event({ event: { type: "session.updated", properties: { sessionID: "private_session_0123" } } })
    await hooks["tool.execute.before"]({ ...call, tool: "bash" })
    const dbpath = join(root, "state", "vx-runtime-observations.sqlite3")
    expect(existsSync(dbpath)).toBe(true)
    const db = new Database(dbpath, { readonly: true })
    try {
      const integrity = db.query("PRAGMA integrity_check").get()
      expect(integrity.integrity_check).toBe("ok")
      expect(db.query("PRAGMA user_version").get().user_version).toBe(1)
      const rows = db.query("SELECT * FROM host_observations ORDER BY event_type").all()
      expect(rows).toHaveLength(3)
      expect(rows.map((row) => row.event_type)).toEqual([
        "TOOL_CALLED_NOT_CONFIRMED", "TOOL_RETURNED_NOT_VERIFIED", "session.updated",
      ])
      expect(rows.every((row) => row.project === "vx-observer-lab")).toBe(true)
      const serialized = JSON.stringify(rows)
      for (const secret of [token, call.sessionID, call.callID]) {
        expect(serialized.includes(secret)).toBe(false)
      }
      // The same call can be replayed safely: INSERT OR IGNORE prevents duplicates.
    } finally { db.close() }
    const wrong = await plugin.server({ directory: join(root, "vecidya") })
    expect(wrong).toEqual({})
    expect(existsSync(join(root, "vx-team-queue.sqlite3"))).toBe(false)
  } finally {
    for (const [key, value] of Object.entries(before)) {
      if (value === undefined) delete process.env[key]
      else process.env[key] = value
    }
    rmSync(root, { recursive: true, force: true })
  }
})
