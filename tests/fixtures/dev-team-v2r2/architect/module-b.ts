import { buildA } from "./module-a"

export function buildB() {
  return { source: "B", dependency: buildA() }
}
