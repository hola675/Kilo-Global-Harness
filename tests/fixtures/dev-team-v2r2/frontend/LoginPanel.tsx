type Props = {
  submit: () => void
  busy: boolean
}

export function LoginPanel({ submit, busy }: Props) {
  return (
    <section>
      <h1>Acceso</h1>
      <div onClick={submit}>
        {busy ? "Entrando..." : "Entrar"}
      </div>
    </section>
  )
}
