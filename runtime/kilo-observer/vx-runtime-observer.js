// component_version: 0.2.0
// last_modified: 2026-11-23
// OBSERVATION_ONLY / SOURCE_CANDIDATE / NOT_INSTALLED / OPT_IN_REQUIRED
// This module does NOT change tool arguments, approvals, chat, or Kilo config.
// Hook support in Kilo Desktop must be proven separately from CLI/VS Code.
import { homedir } from "node:os"
import { join } from "node:path"
import { safeProject, createObservationHooks } from "./lib/vx-observer-hooks.js"
import { existsSync, lstatSync, mkdirSync } from "node:fs"

const ENABLED = process.env.VX_OBSERVER_ENABLE === "1"
const PROJECT_SCOPE = String(process.env.VX_OBSERVER_PROJECT || "").toLowerCase()
const PRIVATE_DIR = join(homedir(), ".config", "kilo", "harness", "state")
const PRIVATE_DB = join(PRIVATE_DIR, "vx-runtime-observations.sqlite3")
const MAX_DB_BYTES = 64 * 1024 * 1024

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
    db.exec("PRAGMA busy_timeout = 250")
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
  if (!ENABLED || !PROJECT_SCOPE || safeProject(directory) !== PROJECT_SCOPE) return {}
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
  try {
    const insert = db.query(
      "INSERT OR IGNORE INTO host_observations " +
      "(event_key, project, session_ref, call_ref, event_type, tool, observed_at) " +
      "VALUES (?1, ?2, ?3, ?4, ?5, ?6, ?7)"
    )
    return createObservationHooks({
      project,
      write: (...values) => insert.run(...values),
      canWrite: () => !(existsSync(PRIVATE_DB) && lstatSync(PRIVATE_DB).size > MAX_DB_BYTES),
    })
  } catch {
    db.close()
    return {}
  }
}

export default { id: "vx-runtime-observer-source", server: observer }
