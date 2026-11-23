// component_version: 1.0.0
// last_modified: 2026-11-23
// Offline contract tests; do not start Kilo or write to the user's HOME.
import test from "node:test"
import assert from "node:assert/strict"
import { createObservationHooks, safeProject } from "../runtime/kilo-observer/lib/vx-observer-hooks.js"
import Plugin from "../runtime/kilo-observer/vx-runtime-observer.js"

test("disabled by default; no plugin hooks nor database initialization", async () => {
  assert.equal(Plugin.id, "vx-runtime-observer-source")
  assert.equal(typeof Plugin.server, "function")
  assert.deepEqual(await Plugin.server({ directory: "/isolated/vecidya" }), {})
})

test("only metadata from recognized tools, never arguments or outputs", async () => {
  const events = []
  const hooks = createObservationHooks({
    project: "vecidya",
    write: (...args) => events.push(args),
    clock: () => new Date("2026-11-23T07:22:00.000Z"),
  })
  const secret = "SECRET_NEVER_STORE_98765"
  const input = {
    tool: "task", sessionID: "private-session-123", callID: "private-call-456",
    args: { prompt: secret }, output: { output: secret }, metadata: { token: secret },
  }
  await hooks["tool.execute.before"](input, { args: input.args })
  await hooks["tool.execute.after"](input, { output: input.output })
  await hooks["tool.execute.after"](input, { output: input.output })
  await hooks["tool.execute.before"]({ ...input, tool: "bash" })
  assert.equal(events.length, 3)
  assert.equal(events[0].length, 7)
  assert.equal(events[0][4], "TOOL_CALLED_NOT_CONFIRMED")
  assert.equal(events[1][4], "TOOL_RETURNED_NOT_VERIFIED")
  assert.equal(events[1][0], events[2][0], "same callback must yield same event key")
  assert.notEqual(events[0][0], events[1][0], "before/after are different observations")
  const serialized = JSON.stringify(events)
  for (const hidden of [secret, input.sessionID, input.callID]) {
    assert.equal(serialized.includes(hidden), false, "private content must not be stored")
  }
})

test("session lifecycle sampled and unknown events ignored", async () => {
  const events = []
  let minute = 22
  const hooks = createObservationHooks({
    project: "lab",
    write: (...values) => events.push(values),
    clock: () => new Date('2026-11-23T07:' + String(minute).padStart(2, "0") + ":00.000Z"),
  })
  await hooks.event({ event: { type: "message.updated", properties: { sessionID: "hidden" } } })
  await hooks.event({ event: { type: "session.updated", properties: { info: { id: "hidden" } } } })
  await hooks.event({ event: { type: "session.updated", properties: { info: { id: "hidden" } } } })
  assert.equal(events.length, 2)
  assert.equal(events[0][0], events[1][0])
  minute = 23
  await hooks.event({ event: { type: "session.updated", properties: { info: { id: "hidden" } } } })
  assert.notEqual(events[1][0], events[2][0])
  assert.deepEqual(events.map(e => e[4]), Array(3).fill("session.updated"))
})

test("observer write failure or full disk disables itself without interrupting Kilo", async () => {
  let writes = 0
  const hooks = createObservationHooks({
    project: "lab",
    write: () => { writes++; throw new Error("sqlite busy") },
  })
  await hooks["tool.execute.before"]({ tool: "task", sessionID: "s", callID: "c" })
  await hooks["tool.execute.after"]({ tool: "task", sessionID: "s", callID: "c" })
  assert.equal(writes, 1)
  const fullHooks = createObservationHooks({
    project: "lab",
    write: () => { throw new Error("must not write") },
    canWrite: () => false,
  })
  await fullHooks.event({ event: { type: "session.created", properties: { info: { id: "s" } } } })
})

test("source plugin does not infer project identifiers from secrets or paths", () => {
  assert.equal(safeProject("/work/Vecidya"), "vecidya")
  assert.equal(safeProject("/work/../../Project With Spaces"), "private-project")
})
