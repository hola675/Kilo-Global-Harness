import { buildB } from "./module-b"

export function buildA() {
  return { source: "A", dependency: buildB() }
}
