export type CreateAccountInput = { email: string }
export type Account = { id: string; email: string; normalizedEmail: string }

export class ValidationError extends Error {}
export class DuplicateAccountError extends Error {}

export interface AccountRepository {
  findByNormalizedEmail(normalizedEmail: string): Promise<Account | null>
  insert(account: Account): Promise<Account>
}

export async function createAccount(
  repo: AccountRepository,
  input: CreateAccountInput
): Promise<Account> {
  const email = input.email.trim()
  if (!email || !email.includes("@")) {
    throw new ValidationError("invalid email")
  }

  const normalizedEmail = email.toLowerCase()
  const existing = await repo.findByNormalizedEmail(normalizedEmail)
  if (existing) {
    throw new DuplicateAccountError("duplicate email")
  }

  return repo.insert({
    id: crypto.randomUUID(),
    email,
    normalizedEmail,
  })
}
