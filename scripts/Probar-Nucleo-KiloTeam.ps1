# KILO-GLOBAL-HARNESS-TEAM
# Version: 0.2.0
# Fecha: 2026-11-24
# Prueba temporal F04. No es el instalador de distribucion.
# Exit: 0 operacion completada; 1 bloqueo/error. No eleva privilegios.
[CmdletBinding()]
param(
    [ValidateSet('Diagnostico','Preparar','Verificar','Retirar')]
    [string]$Modo = 'Diagnostico',
    [switch]$ConfirmarKiloCerrado,
    [switch]$ConfirmarPrueba,
    [switch]$ConfirmarRetirada,
    [string]$MarcadorRecibido
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

function Assert-Directory([string]$Path) {
    $Dir = [IO.DirectoryInfo]::new([IO.Path]::GetFullPath($Path))
    while ($null -ne $Dir) {
        $Item = Get-Item -LiteralPath $Dir.FullName -Force
        if (-not $Item.PSIsContainer -or ($Item.Attributes -band [IO.FileAttributes]::ReparsePoint)) {
            throw "Directorio no seguro: $($Dir.FullName)"
        }
        $Dir = $Dir.Parent
    }
}

function Assert-File([string]$Path) {
    Assert-Directory (Split-Path -Parent $Path)
    $Item = Get-Item -LiteralPath $Path -Force
    if ($Item.PSIsContainer -or ($Item.Attributes -band [IO.FileAttributes]::ReparsePoint)) {
        throw "Archivo no seguro: $Path"
    }
}

function Get-Hash([string]$Path) {
    Assert-File $Path
    (Get-FileHash -LiteralPath $Path -Algorithm SHA256).Hash
}

function Get-BytesHash([byte[]]$Bytes) {
    [Convert]::ToHexString([Security.Cryptography.SHA256]::HashData($Bytes))
}

function Write-New([string]$Path, [byte[]]$Bytes) {
    Assert-Directory (Split-Path -Parent $Path)
    $Stream = [IO.File]::Open($Path, [IO.FileMode]::CreateNew, [IO.FileAccess]::Write, [IO.FileShare]::None)
    try {
        $Stream.Write($Bytes, 0, $Bytes.Length)
        $Stream.Flush($true)
    } finally {
        $Stream.Dispose()
    }
}

function Assert-Absent([string]$Path) {
    if (Test-Path -LiteralPath $Path) { throw "Colision: $Path" }
}

function Get-State {
    Assert-File $StateFile
    $State = Get-Content -LiteralPath $StateFile -Raw | ConvertFrom-Json -AsHashtable
    if ($State.id -cne 'kilo-team-f04-probe-v1' -or $State.root -cne $GlobalDir -or $State.policyVersion -cnotin @('0.14.0','0.15.0')) {
        throw 'Registro de propiedad incompatible.'
    }
    foreach ($Key in @('originalHash','policyHash','overlayHash','sourceHash')) {
        if ($State[$Key] -cnotmatch '^[0-9A-F]{64}$') { throw "Hash invalido: $Key" }
    }
    if ($State.marker -cnotmatch '^KTEAM-CORE-[0-9a-f]{32}$') { throw 'Marcador invalido.' }
    $State
}

function Get-Status([string]$Path, [string]$Expected) {
    if (-not (Test-Path -LiteralPath $Path)) { return 'ABSENT' }
    if ((Get-Hash $Path) -ceq $Expected) { return 'MATCH' }
    'DRIFT'
}

try {
    if (-not $IsWindows -or $PSVersionTable.PSVersion.Major -lt 7) { throw 'Requiere Windows y PowerShell 7.' }
    if (-not $env:LOCALAPPDATA -or -not $env:APPDATA) { throw 'Rutas de usuario no disponibles.' }
    if ($env:XDG_CONFIG_HOME -or $env:KILO_CONFIG_DIR -or $env:KILO_CONFIG -or $env:KILO_CONFIG_CONTENT) {
        throw 'Overrides de configuracion en PowerShell. Revisar antes de probar.'
    }
    $GlobalDir = [IO.Path]::GetFullPath((Join-Path $HOME '.config\kilo'))
    $PolicyFile = Join-Path $GlobalDir 'AGENTS.md'
    $OverlayFile = Join-Path $GlobalDir 'kilo.json'
    $OriginalFile = Join-Path $GlobalDir 'kilo.jsonc'
    $ProfileFile = Join-Path $env:APPDATA 'Kilo Desktop\plugins\kilo.core\agent\runtime\config\kilo\AGENTS.md'
    $ClaudeFile = Join-Path $HOME '.claude\CLAUDE.md'
    $StateDir = Join-Path $env:LOCALAPPDATA 'KiloTeam-F04-Lab'
    $StateFile = Join-Path $StateDir 'ownership.json'
    $SourceFile = Join-Path (Split-Path -Parent $PSScriptRoot) 'team\policies\AGENTS.md'
    Assert-Directory $GlobalDir
    Assert-Directory $env:LOCALAPPDATA
    if (Test-Path -LiteralPath $StateDir) { Assert-Directory $StateDir }

    if ($Modo -eq 'Diagnostico') {
        $HasState = Test-Path -LiteralPath $StateFile -PathType Leaf
        [pscustomobject]@{
            Modo = $Modo
            Global = $GlobalDir
            Registro = $StateFile
            RegistroExiste = $HasState
            OriginalExiste = Test-Path -LiteralPath $OriginalFile -PathType Leaf
            OverlayExiste = Test-Path -LiteralPath $OverlayFile
            PoliticaExiste = Test-Path -LiteralPath $PolicyFile
            PerfilInstruccionesExiste = Test-Path -LiteralPath $ProfileFile
            ClaudeInstruccionesExiste = Test-Path -LiteralPath $ClaudeFile
        } | Format-List
        if ($HasState) {
            $State = Get-State
            [pscustomobject]@{
                Original = Get-Status $OriginalFile $State.originalHash
                Overlay = Get-Status $OverlayFile $State.overlayHash
                Politica = Get-Status $PolicyFile $State.policyHash
            } | Format-List
        }
        exit 0
    }

    if ($Modo -eq 'Preparar') {
        if (-not $ConfirmarKiloCerrado -or -not $ConfirmarPrueba) { throw 'Requiere autorizacion explicita y cierre de Kilo.' }
        foreach ($Path in @($StateFile,$PolicyFile,$OverlayFile,$ProfileFile,$ClaudeFile)) { Assert-Absent $Path }
        foreach ($Name in @('opencode.json','opencode.jsonc','config.json','config')) { Assert-Absent (Join-Path $GlobalDir $Name) }
        $OriginalHash = Get-Hash $OriginalFile
        try {
            $Existing = Get-Content -LiteralPath $OriginalFile -Raw | ConvertFrom-Json -AsHashtable
        } catch { throw 'JSONC existente no interpretable; no se modificara.' }
        if ($Existing -isnot [Collections.IDictionary] -or @($Existing.Keys) -contains 'instructions') {
            throw 'JSONC existente incompatible; no se modificara.'
        }
        Remove-Variable Existing
        $SourceHash = Get-Hash $SourceFile
        $Policy = [IO.File]::ReadAllText($SourceFile)
        if ($Policy -notmatch '(?m)^Versión del archivo: 0\.15\.0 \|') { throw 'Version del candidato inesperada.' }
        $Marker = 'KTEAM-CORE-' + [guid]::NewGuid().ToString('N')
        $NL = [Environment]::NewLine
        $Policy += $NL + $NL + '## Control temporal F04 (solo evaluacion)' + $NL + "Al solicitar KTEAM-F04-LOAD, devuelve este marcador desde las instrucciones cargadas: $Marker" + $NL
        $PolicyBytes = [Text.Encoding]::UTF8.GetBytes($Policy)
        $Overlay = [ordered]@{ '$schema' = 'https://app.kilo.ai/config.json'; instructions = @($PolicyFile.Replace('\','/')) }
        $OverlayBytes = [Text.Encoding]::UTF8.GetBytes(($Overlay | ConvertTo-Json -Depth 4))
        $State = [ordered]@{
            id = 'kilo-team-f04-probe-v1'; root = $GlobalDir; policyVersion = '0.15.0'
            originalHash = Get-BytesHash ([IO.File]::ReadAllBytes($OriginalFile))
            policyHash = Get-BytesHash $PolicyBytes
            overlayHash = Get-BytesHash $OverlayBytes; sourceHash = $SourceHash
            marker = $Marker; createdUtc = [DateTime]::UtcNow.ToString('o')
        }
        if ($State.originalHash -cne $OriginalHash -or (Get-Hash $OriginalFile) -cne $OriginalHash -or (Get-Hash $SourceFile) -cne $SourceHash) { throw 'Cambio durante preparacion.' }
        if (-not (Test-Path -LiteralPath $StateDir)) { New-Item -ItemType Directory -Path $StateDir | Out-Null }
        Assert-Directory $StateDir
        # Registro previo a toda mutacion de configuracion. Si falla una creacion,
        # conservarlo para diagnostico; Retirar verifica cada archivo presente.
        Write-New $StateFile ([Text.Encoding]::UTF8.GetBytes(($State | ConvertTo-Json -Depth 4)))
        Write-New $PolicyFile $PolicyBytes
        Write-New $OverlayFile $OverlayBytes
        if ((Get-Hash $OriginalFile) -cne $OriginalHash -or
            (Get-Hash $PolicyFile) -cne $State.policyHash -or
            (Get-Hash $OverlayFile) -cne $State.overlayHash) { throw 'Integridad posterior no coincide; conservar registro.' }
        Write-Host 'F04_PREPARADO. Solo usar Kilo en el laboratorio durante la prueba.'
        Write-Host "Registro persistente: $StateFile"
        exit 0
    }

    $StateHash = Get-Hash $StateFile
    $State = Get-State
    $OriginalStatus = Get-Status $OriginalFile $State.originalHash
    $OverlayStatus = Get-Status $OverlayFile $State.overlayHash
    $PolicyStatus = Get-Status $PolicyFile $State.policyHash
    if ($Modo -eq 'Verificar') {
        $MarkerStatus = if (-not $MarcadorRecibido) { 'NOT_RUN' } elseif ($MarcadorRecibido -ceq $State.marker) { 'MATCH' } else { 'MISMATCH' }
        $Passed = $OriginalStatus -eq 'MATCH' -and $OverlayStatus -eq 'MATCH' -and $PolicyStatus -eq 'MATCH' -and $MarkerStatus -eq 'MATCH'
        [pscustomobject]@{
            Original = $OriginalStatus; Overlay = $OverlayStatus; Politica = $PolicyStatus
            Marcador = $MarkerStatus
            Resultado = if ($Passed) { 'PASS_LOAD_REPORTED' } else { 'NOT_VERIFIED' }
        } | Format-List
        if (-not $Passed) { exit 1 }
        exit 0
    }

    if (-not $ConfirmarKiloCerrado -or -not $ConfirmarRetirada) { throw 'Requiere autorizacion explicita de retirada y cierre de Kilo.' }
    if ($OriginalStatus -ne 'MATCH' -or $OverlayStatus -eq 'DRIFT' -or $PolicyStatus -eq 'DRIFT') { throw 'Deriva detectada. No retirar ni sobrescribir; revisar.' }
    if ((Get-Hash $StateFile) -cne $StateHash -or (Get-Hash $OriginalFile) -cne $State.originalHash) { throw 'Registro/original cambiado.' }
    # Retirada selectiva, tambien permite recuperar preparacion interrumpida.
    foreach ($Owned in @(
        @{ Path = $OverlayFile; Hash = $State.overlayHash },
        @{ Path = $PolicyFile; Hash = $State.policyHash }
    )) {
        if (Test-Path -LiteralPath $Owned.Path) {
            if ((Get-Hash $Owned.Path) -cne $Owned.Hash) { throw 'Archivo temporal cambiado.' }
            Remove-Item -LiteralPath $Owned.Path -ErrorAction Stop
        }
    }
    if ((Test-Path -LiteralPath $OverlayFile) -or (Test-Path -LiteralPath $PolicyFile) -or
        (Get-Hash $OriginalFile) -cne $State.originalHash -or (Get-Hash $StateFile) -cne $StateHash) { throw 'Retirada incompleta; conservar registro.' }
    Remove-Item -LiteralPath $StateFile -ErrorAction Stop
    Write-Host 'F04_RETIRADO: temporales ausentes, original intacto, registro retirado.'
    exit 0
} catch {
    Write-Error -Message ("F04_BLOCKED: " + $_.Exception.Message) -ErrorAction Continue
    exit 1
}
