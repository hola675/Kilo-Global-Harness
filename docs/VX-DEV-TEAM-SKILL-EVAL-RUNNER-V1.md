# Dev Team Skill Eval Runner V1

El runner **no invoca modelos**. Convierte los cuatro registries de evals en casos reproducibles y puntúa observaciones reales.

## Generar plantilla

```powershell
python tools/dev_team_skill_eval_runner.py --repo-root . \
  --write-template artifacts/dev-team-skill-eval-observations.json
```

## Captura runtime

Para cada caso, registrar qué skills seleccionó realmente Kilo:

- `capture_status = OBSERVED`
- `selected_skills = [...]`

Si no se ejecutó, queda `PENDING`.

## Puntuar

```powershell
python tools/dev_team_skill_eval_runner.py --repo-root . \
  --observations artifacts/dev-team-skill-eval-observations.json \
  --report artifacts/dev-team-skill-eval-report.json
```

Un caso negativo pasa si la skill evaluada no fue seleccionada. El runner no convierte ausencia de observación en PASS.
