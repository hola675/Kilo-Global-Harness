import { buildReport } from "./report_service"
import config from "./config.json"

export async function runAuditReport(userId: string) {
  return buildReport(userId, config.retentionDays)
}
