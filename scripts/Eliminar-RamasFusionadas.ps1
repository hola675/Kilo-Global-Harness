#Requires -Version 7.0
# component_version: 1.0.0
# last_modified: 2026-11-23
<#
.SYNOPSIS
  Elimina SOLO ramas remotas work/* con PR fusionado a main y HEAD comprobado.
.DESCRIPTION
  Simulación por defecto. Para borrar: -Aplicar -ConfirmarBorrado.
  Protege main, PR abiertos, commits posteriores al PR, worktrees y cambios
  locales. GitHub CLI autenticado y git son requisitos; no solicita secretos.
  No elimina ramas locales salvo -EliminarLocales, y solo si coinciden con
  el HEAD remoto protegido y no están abiertas en un worktree.
#>
[CmdletBinding()]
param(
    [switch]$Aplicar,
    [switch]$ConfirmarBorrado,
    [switch]$EliminarLocales
)
$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest

$Repo = 'hola675/Kilo-Global-Harness'
$Root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path

if ($Aplicar -and -not $ConfirmarBorrado) {
    throw 'Borrado requiere conjuntamente -Aplicar -ConfirmarBorrado.'
}
foreach ($Tool in @('git','gh')) {
    if (-not (Get-Command $Tool -CommandType Application -ErrorAction SilentlyContinue)) {
        throw "$Tool no encontrado. Instala y autentica GitHub CLI antes de continuar."
    }
}
$Origin = (& git -C $Root remote get-url origin | Out-String).Trim()
if ($LASTEXITCODE -ne 0 -or $Origin -notmatch '(?i)^(?:https://github[.]com/|git@github[.]com:|ssh://git@github[.]com/)(hola675/Kilo-Global-Harness)(?:[.]git)?/?$') {
    throw 'El origen no corresponde exactamente a hola675/Kilo-Global-Harness.'
}
$Current = (& git -C $Root branch --show-current | Out-String).Trim()
if ($LASTEXITCODE -ne 0 -or $Current -cne 'main') {
    throw 'Ejecuta únicamente en el worktree de main.'
}
$Dirty = @(& git -C $Root status --porcelain)
if ($LASTEXITCODE -ne 0 -or $Dirty.Count -gt 0) {
    throw 'Hay cambios locales; resolverlos sin descartarlos antes de limpiar ramas.'
}
& gh auth status *> $null
if ($LASTEXITCODE -ne 0) { throw 'gh auth status no tiene sesión de GitHub válida.' }

# Consultar refs reales, no confiar en ramas remotas cacheadas.
$Refs = @(& git -C $Root ls-remote --heads origin 'refs/heads/work/*')
if ($LASTEXITCODE -ne 0) { throw 'No se pudo consultar las ramas remotas reales.' }
$Worktrees = @(& git -C $Root worktree list --porcelain)
if ($LASTEXITCODE -ne 0) { throw 'No se pudo inventariar worktrees.' }

$Report = [System.Collections.Generic.List[object]]::new()
foreach ($Line in $Refs) {
    if ($Line -notmatch '^([a-fA-F0-9]{40})\s+refs/heads/(work/[a-zA-Z0-9._/-]+)$') {
        throw 'Referencia work/* de formato inesperado: cancelación preventiva.'
    }
    $Sha = $Matches[1].ToLowerInvariant()
    $Name = $Matches[2]
    if ($Name -eq 'main' -or $Name -notlike 'work/*') { continue }

    $Status = 'BLOQUEADA'
    $Detail = ''
    $PrNumber = $null

    $PrJson = (& gh pr list --repo $Repo --state all --head $Name --json 'number,state,mergedAt,headRefOid,baseRefName' --limit 100 | Out-String)
    if ($LASTEXITCODE -ne 0) {
        $Detail = 'Consulta GitHub PR fallida'
    } else {
        $Prs = @(ConvertFrom-Json -InputObject $PrJson)
        $Open = @($Prs | Where-Object { $_.state -eq 'OPEN' })
        $Verified = @($Prs | Where-Object {
            $_.state -eq 'MERGED' -and $_.mergedAt -and
            $_.baseRefName -eq 'main' -and
            $_.headRefOid -eq $Sha
        })
        $InUse = @($Worktrees | Where-Object { $_ -ceq ('branch refs/heads/' + $Name) })
        & git -C $Root show-ref --verify --quiet ('refs/heads/' + $Name)
        $LocalExists = ($LASTEXITCODE -eq 0)
        $LocalHead = if ($LocalExists) {
            (& git -C $Root rev-parse ('refs/heads/' + $Name) | Out-String).Trim().ToLowerInvariant()
        } else { $null }

        if ($Open.Count -gt 0) {
            $Detail = 'PR abierto; preservar rama'
        } elseif ($InUse.Count -gt 0) {
            $Detail = 'Rama utilizada por otro worktree'
        } elseif ($LocalExists -and $LocalHead -ne $Sha) {
            $Detail = 'Rama local diverge; preservar hasta reconciliar'
        } elseif ($Verified.Count -eq 0) {
            $Detail = 'Sin PR fusionado a main con HEAD remoto idéntico'
        } else {
            $PrNumber = $Verified[0].number
            $Status = if ($Aplicar) { 'ELIMINAR' } else { 'SIMULACION' }
            $Detail = "PR #$PrNumber fusionado; HEAD exacto"
            if ($Aplicar) {
                # Lease atómica: si la rama cambia desde la consulta, NO borrar.
                $Lease = "--force-with-lease=refs/heads/$($Name):$Sha"
                $DeleteRef = ":refs/heads/$Name"
                & git -C $Root push $Lease origin $DeleteRef
                if ($LASTEXITCODE -ne 0) {
                    $Status = 'ERROR'
                    $Detail = 'Git rechazó eliminación o cambió el HEAD'
                } else {
                    $Status = 'ELIMINADA'
                    if ($EliminarLocales -and $LocalExists -and $LocalHead -eq $Sha) {
                        # PR squash no es ancestro Git; borrar local solo con
                        # igualdad SHA, PR fusionado y worktree desocupado.
                        & git -C $Root branch -D -- $Name
                        if ($LASTEXITCODE -ne 0) { $Detail += '; rama local NO eliminada' }
                        else { $Detail += '; rama local eliminada' }
                    }
                }
            }
        }
    }
    $Report.Add([pscustomobject]@{
        Rama = $Name
        Estado = $Status
        PR = $PrNumber
        Motivo = $Detail
    })
}

$Report | Format-Table -AutoSize -Wrap
if ($Aplicar) {
    & git -C $Root fetch --prune origin
    if ($LASTEXITCODE -ne 0) { throw 'Limpieza remota aplicada, pero falló fetch --prune.' }
    Write-Host 'Ramas remotas restantes:' -ForegroundColor Cyan
    & git -C $Root branch -r
} else {
    Write-Host 'SIMULACIÓN: no se ha eliminado ninguna rama.' -ForegroundColor Yellow
    Write-Host 'Para aplicar: -Aplicar -ConfirmarBorrado (opcional: -EliminarLocales).' -ForegroundColor Yellow
}
