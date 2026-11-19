import {
  AccountRepository,
  createAccount,
  DuplicateAccountError,
  ValidationError,
} from "./account_service"

type Response = { status: number; body: unknown }

export async function postAccounts(
  repo: AccountRepository,
  body: unknown
): Promise<Response> {
  if (!body || typeof body !== "object" || !("email" in body)) {
    return { status: 422, body: { error: "invalid input" } }
  }

  try {
    const account = await createAccount(repo, {
      email: String((body as { email: unknown }).email),
    })
    return { status: 201, body: account }
  } catch (error) {
    if (error instanceof DuplicateAccountError) {
      return { status: 409, body: { error: "duplicate account" } }
    }
    if (error instanceof ValidationError) {
      return { status: 422, body: { error: "invalid input" } }
    }
    throw error
  }
}
