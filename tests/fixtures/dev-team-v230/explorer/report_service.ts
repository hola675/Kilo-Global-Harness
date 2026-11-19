export async function buildReport(userId: string, retentionDays: number) {
  return {
    userId,
    retentionDays,
    generatedAt: new Date().toISOString(),
  }
}
