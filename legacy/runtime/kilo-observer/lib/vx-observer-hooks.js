// component_version: 0.1.0
// last_modified: 2026-11-23
// Pure normalization boundary: no user prompts, tool arguments or outputs enter storage.
import { createHash } from "node:crypto"
import { basename } from "node:path"

const TOOLS = new Set(["task", "skill", "board_post", "board_read"])
const SESSIONS = new Set(["session.created", "session.updated", "session.idle", "session.error"])

function hash(...values) {
  return createHash("sha256").update(values.join("\x00")).digest("hex")
}

export function safeProject(directory) {
  const leaf = basename(String(directory || "unknown")).toLowerCase()
  return /^[a-z0-9][a-z0-9._-]{0,63}$/.test(leaf) ? leaf : "private-project"
}

function safeSessionID(id) {
  return typeof id === "string" && id.length > 0 && id.length <= 256 ? id : null
}

function sessionFromEvent(event) {
  const id = event?.properties?.info?.id ?? event?.properties?.sessionID
  return safeSessionID(id)
}

/**
 * Low-risk deterministic hook transformer. The sink receives exactly seven scalar
 * metadata values; it never receives the original Kilo event or tool payload.
 * Presence of a hook callback proves observation, never tool success or verification.
 */
export function createObservationHooks({ project, write, clock = () => new Date(),
                                         canWrite = () => true }) {
  if (typeof write !== "function") throw new TypeError("write sink required")
  let disabled = false
  function observe(type, sessionID, callID = null, tool = null) {
    const session = safeSessionID(sessionID)
    if (disabled || !session) return
    try {
      if (!canWrite()) { disabled = true; return }
      const stamp = clock().toISOString()
      const sessionRef = hash(session)
      const callRef = typeof callID === "string" && callID.length > 0 && callID.length <= 256
        ? hash(session, callID) : null
      const scope = callRef || (type === "session.created" ? "lifecycle" : stamp.slice(0, 16))
      const eventKey = hash(project, type, sessionRef, scope, tool || "")
      write(eventKey, project, sessionRef, callRef, type, tool, stamp)
    } catch {
      // Observability is never permitted to stop the user agent's execution.
      disabled = true
    }
  }
  return {
    "tool.execute.before": async (input) => {
      if (TOOLS.has(input?.tool) && typeof input?.callID === "string") {
        observe("TOOL_CALLED_NOT_CONFIRMED", input.sessionID, input.callID, input.tool)
      }
    },
    "tool.execute.after": async (input) => {
      if (TOOLS.has(input?.tool) && typeof input?.callID === "string") {
        observe("TOOL_RETURNED_NOT_VERIFIED", input.sessionID, input.callID, input.tool)
      }
    },
    event: async ({ event } = {}) => {
      if (SESSIONS.has(event?.type)) observe(event.type, sessionFromEvent(event))
    },
  }
}
