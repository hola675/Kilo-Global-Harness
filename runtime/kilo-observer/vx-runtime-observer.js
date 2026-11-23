// component_version: 0.1.0
// last_modified: 2026-11-23
// OBSERVATION_ONLY / SOURCE_CANDIDATE / NOT_INSTALLED / OPT_IN_REQUIRED
// This module does NOT change tool arguments, approvals, chat, or Kilo config.
// Hook support in Kilo Desktop must be proven separately from CLI/VS Code.
import { createHash } from "node:crypto"
import { homedir } from "node:os"
import { basename, join } from "node:path"
import { existsSync, lstatSync, mkdirSync } from "node:fs"

const ENABLED = process.env.VX_OBSERVER_ENABLE === "1"
const PRIVATE_DIR = join(homedir(), ".config", "kilo", "harness", "state")
const PRIVATE_DB = join(PRIVATE_DIR, "vx-runtime-observations.sqlite3")
const TOOLS = new Set(["task", "skill", "board_post", "board_read"])
const SESSION_EVENTS = new Set([
  "session.created", "session.updated", "session.idle", "session.error",
])
const MAX_DB_BYTES = 64 * 1024 * 1024

function hash(...values) {
  return createHash("sha256").update(values.join("\x00")).digest("hex")
}

function safeProject(directory) {
  const leaf = basename(String(directory || "unknown")).toLowerCase()
  return /^[a-z0-9][a-z0-9._-]{0,63}$/.test(leaf) ? leaf : "private-project"
}

function safeTool(tool) {
  return typeof tool === "string" && TOOLS.has(tool) ? tool : null
}

function sessionFromEvent(event) {
  const info = event?.properties?.info
  const id = info?.id ?? event?.properties?.sessionID
  return typeof id === "string" && id.length > 0 && id.length <= 256 ? id : null
}

function ensurePrivateDatabase(Database) {
  // Do not follow a direct symlink for the private SQLite file or directory.
  if (existsSync(PRIVATE_DIR) && lstatSync(PRIVATE_DIR).isSymbolicLink()) {
    throw new Error("observer state directory is a symlink")
  }
  mkdirSync(PRIVATE_DIR, { recursive: true })
  if (existsSync(PRIVATE_DB) && lstatSync(PRIVATE_DB).isSymbolicLink()) {
    throw new Error("observer database is a symlink")
  }
  const db = new Database(PRIVATE_DB, { create: true, strict: true })
  try {
    db.exec("PRAGMA busy_timeout = 1500")
    db.exec("PRAGMA journal_mode = WAL")
    const versionRow = db.query("PRAGMA user_version").get()
    const version = Number(versionRow?.user_version ?? -1)
    if (version !== 0 && version !== 1) {
      throw new Error("unsupported observer schema version")
    }
    if (version === 0) {
      const tables = db.query(
        "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'",
      ).all()
      if (tables.length !== 0) {
        throw new Error("observer database belongs to another schema")
      }
    }
    db.exec("BEGIN IMMEDIATE")
    try {
      db.exec(
        "CREATE TABLE IF NOT EXISTS host_observations (" +
        "event_key TEXT PRIMARY KEY, project TEXT NOT NULL, " +
        "session_ref TEXT NOT NULL, call_ref TEXT, " +
        "event_type TEXT NOT NULL, tool TEXT, observed_at TEXT NOT NULL)"
      )
      db.exec(
        "CREATE INDEX IF NOT EXISTS host_observations_project_time " +
        "ON host_observations(project, observed_at)"
      )
      db.exec("PRAGMA user_version = 1")
      db.exec("COMMIT")
    } catch (error) {
      db.exec("ROLLBACK")
      throw error
    }
    return db
  } catch (error) {
    db.close()
    throw error
  }
}

const observer = async ({ directory }) => {
  if (!ENABLED) return {}
  let Database
  try {
    ;({ Database } = await import("bun:sqlite"))
  } catch {
    // Not every Kilo host has Bun's SQLite runtime. Fail open; do not block Kilo.
    return {}
  }
  let db
  try {
    db = ensurePrivateDatabase(Database)
  } catch {
    return {}
  }
  const project = safeProject(directory)
  const insert = db.query(
    "INSERT OR IGNORE INTO host_observations " +
    "(event_key, project, session_ref, call_ref, event_type, tool, observed_at) " +
    "VALUES (?1, ?2, ?3, ?4, ?5, ?6, ?7)"
  )
  let disabledByError = false

  function observe(type, sessionID, callID = null, tool = null) {
    if (disabledByError || typeof sessionID !== "string" || !sessionID) return
    try {
      if (existsSync(PRIVATE_DB) && lstatSync(PRIVATE_DB).size > MAX_DB_BYTES) {
        disabledByError = true
        return
      }
      const now = new Date()
      const sessionRef = hash(sessionID)
      const callRef = typeof callID === "string" && callID ? hash(sessionID, callID) : null
      // Lifecycle 'updated' is sampled per minute; tool events are idempotent by callID.
      const keyScope = callRef || (type === "session.updated"
        ? now.toISOString().slice(0, 16)
        : "lifecycle")
      const key = hash(type, sessionRef, keyScope, tool || "")
      insert.run(key, project, sessionRef, callRef, type, tool, now.toISOString())
    } catch {
      // Never fail the user's task because the passive observer cannot record data.
      disabledByError = true
    }
  }

  return {
    "tool.execute.before": async (input) => {
      const tool = safeTool(input?.tool)
      if (tool && typeof input?.callID === "string") {
        observe("TOOL_CALLED_NOT_CONFIRMED", input.sessionID, input.callID, tool)
      }
    },
    "tool.execute.after": async (input) => {
      const tool = safeTool(input?.tool)
      if (tool && typeof input?.callID === "string") {
        observe("TOOL_RETURNED_NOT_VERIFIED", input.sessionID, input.callID, tool)
      }
    },
    event: async ({ event }) => {
      if (!SESSION_EVENTS.has(event?.type)) return
      const sessionID = sessionFromEvent(event)
      if (sessionID) observe(event.type, sessionID)
    },
  }
}

export default { id: "vx-runtime-observer-source", server: observer }
