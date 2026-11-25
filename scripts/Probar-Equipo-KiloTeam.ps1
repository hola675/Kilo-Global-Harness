# KILO-GLOBAL-HARNESS-TEAM
# Version: 0.4.0
# Fecha: 2026-11-24
# F05.3/F05.4: laboratorio temporal y extensiones editorial/desarrollo. No es instalador global.
# Exit 0: operacion completada en su alcance; 1: bloqueo/error.
[CmdletBinding()]
param(
    [ValidateSet('Diagnostico','Preparar','Verificar','Retirar','PrepararEdicion','VerificarEdicion','RetirarEdicion','PrepararDesarrollo','VerificarDesarrollo','RetirarDesarrollo')]
    [string]$Modo = 'Diagnostico',
    [string]$Modelo,
    [switch]$ConfirmarKiloCerrado,
    [switch]$ConfirmarPrueba,
    [switch]$ConfirmarRetirada,
    [switch]$ConfirmarRetiradaAuxiliar,
    [switch]$ComprobarMarcador,
    [string]$HuellaAprobada
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
    if ($Item.PSIsContainer -or ($Item.Attributes -band [IO.FileAttributes]::ReparsePoint)) { throw "Archivo no seguro: $Path" }
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
    $Stream = [IO.File]::Open($Path,[IO.FileMode]::CreateNew,[IO.FileAccess]::Write,[IO.FileShare]::None)
    try { $Stream.Write($Bytes,0,$Bytes.Length); $Stream.Flush($true) }
    finally { $Stream.Dispose() }
}
function Assert-Absent([string]$Parent,[string]$Name) {
    Assert-Directory $Parent
    if (@(Get-ChildItem -LiteralPath $Parent -Force | Where-Object Name -EQ $Name).Count -ne 0) {
        throw "Colision: $Parent\$Name"
    }
}
function Get-AuxiliaryStatus {
    # Plantilla de Config.ensureGitignore del CLI 7.8.27 auditado.
    # Solo esta ruta y contenido; no asumir propiedad de un archivo ajeno.
    if (-not (Test-Path -LiteralPath $AuxiliaryFile)) { return 'ABSENT' }
    Assert-File $AuxiliaryFile
    $Expected = @('node_modules','package.json','package-lock.json','pnpm-lock.yaml','bun.lock','yarn.lock','.gitignore','agent-manager.json')
    $Actual = [IO.File]::ReadAllLines($AuxiliaryFile)
    if ($Actual.Count -ne $Expected.Count) { throw 'Plantilla .kilo/.gitignore distinta; preservar y revisar.' }
    for ($i = 0; $i -lt $Expected.Count; $i++) {
        if ($Actual[$i] -cne $Expected[$i]) { throw 'Plantilla .kilo/.gitignore distinta; preservar y revisar.' }
    }
    'MATCH_TEMPLATE'
}
function Assert-Tree([switch]$PermitirAuxiliar,[switch]$PermitirEdicion,[switch]$PermitirDesarrollo) {
    $RootNames = @('ownership.json','workspace')
    $WorkspaceNames = @('AGENTS.md','kilo.jsonc','fixture.txt','.kilo')
    if ($PermitirEdicion) { $RootNames += 'editing-ownership.json'; $WorkspaceNames += 'messages-f05.json' }
    if ($PermitirDesarrollo) { $RootNames += 'development-ownership.json'; $WorkspaceNames += $DevNames }
    # Solo directorios conocidos; no recorrer arboles ajenos ni enlaces.
    foreach ($Entry in @(
        @{Dir=$Root; Names=$RootNames},
        @{Dir=$Workspace; Names=$WorkspaceNames},
        @{Dir=(Join-Path $Workspace '.kilo'); Names=@('agents')},
        @{Dir=(Join-Path $Workspace '.kilo\agents'); Names=$AgentNames}
    )) {
        if (-not (Test-Path -LiteralPath $Entry.Dir)) { continue }
        Assert-Directory $Entry.Dir
        foreach ($Item in Get-ChildItem -LiteralPath $Entry.Dir -Force) {
            if ($PermitirAuxiliar -and $Entry.Dir -ceq (Join-Path $Workspace '.kilo') -and $Item.Name -ceq '.gitignore') {
                if ($Item.PSIsContainer -or ($Item.Attributes -band [IO.FileAttributes]::ReparsePoint)) { throw 'Auxiliar no seguro.' }
                if ((Get-AuxiliaryStatus) -cne 'MATCH_TEMPLATE') { throw 'Auxiliar cambiado durante verificacion.' }
                continue
            }
            if ($Item.Name -cnotin $Entry.Names -or ($Item.Attributes -band [IO.FileAttributes]::ReparsePoint)) {
                throw "Entrada no administrada o enlace: $($Item.FullName)"
            }
        }
    }
}
function Get-State {
    Assert-File $StateFile
    $S = Get-Content -LiteralPath $StateFile -Raw | ConvertFrom-Json -AsHashtable
    if ($S.id -cne 'kilo-team-f05-lab-v1' -or $S.root -cne $Root -or $S.policyVersion -cnotin @('0.16.0','0.17.0') -or $S.agentVersion -cne '0.2.0') {
        throw 'Registro incompatible.'
    }
    if ($S.marker -cnotmatch '^KTEAM-F05-[0-9a-f]{32}$' -or $S.files -isnot [Collections.IDictionary] -or $S.files.Count -ne $RelativeFiles.Count) {
        throw 'Registro de propiedad invalido.'
    }
    foreach ($Rel in $RelativeFiles) {
        if (-not $S.files.Contains($Rel) -or $S.files[$Rel] -cnotmatch '^[0-9A-F]{64}$') { throw "Hash invalido: $Rel" }
    }
    $S
}
function Get-Status([string]$Path,[string]$Expected) {
    if (-not (Test-Path -LiteralPath $Path)) { return 'ABSENT' }
    if ((Get-Hash $Path) -ceq $Expected) { return 'MATCH' }
    'DRIFT'
}
function Get-EditFixture([switch]$Target) {
    if ($Target) {
        return (@(
            '{',
            '  "RESERVATION_PENDING": "Solicitud de reserva enviada. Aún no se ha confirmado el resultado.",',
            '  "INSUFFICIENT_STOCK": "No se reservó ningún producto porque no hay existencias suficientes de {sku}.",',
            '  "RETRYABLE_CONFLICT": "Conflicto técnico: no se pudo confirmar el resultado de la reserva."',
            '}'
        ) -join "`n")
    }
    return (@(
        '{',
        '  "RESERVATION_PENDING": "¡Compra realizada con éxito!",',
        '  "INSUFFICIENT_STOCK": "Error al ejecutar transacción para {sku}",',
        '  "RETRYABLE_CONFLICT": "Error crítico. Vuelva a comprar el producto"',
        '}'
    ) -join "`n")
}
function Get-EditBaselineHash {
    Get-BytesHash ([Text.Encoding]::UTF8.GetBytes((Get-EditFixture) + "`n"))
}
function Get-EditState([string]$ParentHash) {
    Assert-File $EditStateFile
    $E = Get-Content -LiteralPath $EditStateFile -Raw | ConvertFrom-Json -AsHashtable
    if ($E -isnot [Collections.IDictionary] -or $E.Count -ne 5 -or
        $E.id -cne 'kilo-team-f05-editorial-v1' -or $E.parentHash -cne $ParentHash -or
        $E.relativePath -cne 'messages-f05.json' -or $E.owner -cne 'team-editorial' -or
        $E.baseline -cne (Get-EditBaselineHash)) {
        throw 'Registro editorial incompatible; preservar.'
    }
    $E
}
function Get-EditStatus {
    if (-not (Test-Path -LiteralPath $EditFixture)) { throw 'Fixture editorial ausente; preservar registro.' }
    $Actual = Get-Hash $EditFixture
    if ($Actual -ceq (Get-EditBaselineHash)) { return 'BASELINE' }
    # Solo resultados exactos autorizados, UTF-8 sin BOM, LF o CRLF, salto final opcional.
    $Target = Get-EditFixture -Target
    foreach ($Sep in @("`n","`r`n")) {
        $Text = $Target.Replace("`n",$Sep)
        foreach ($Suffix in @('',$Sep)) {
            if ($Actual -ceq (Get-BytesHash ([Text.Encoding]::UTF8.GetBytes($Text + $Suffix)))) { return 'EXPECTED_EDIT' }
        }
    }
    throw 'Fixture editorial distinto del baseline o resultado autorizado; preservar.'
}
function Get-DevSeed {
    $Seeds = [ordered]@{}
    foreach ($Name in $DevNames) {
        if ($DevOwners[$Name] -ceq 'protected') {
            $Source = Join-Path $Repo "tests\fixtures\f05-development\$Name"
            Assert-File $Source
            $Seeds[$Name] = [IO.File]::ReadAllBytes($Source)
        } else {
            $Prefix = if ($Name.EndsWith('.ps1')) { '#' } else { '//' }
            $Seeds[$Name] = [Text.Encoding]::UTF8.GetBytes("$Prefix F05 placeholder; owner=$($DevOwners[$Name]); NOT_IMPLEMENTED`n")
        }
    }
    return $Seeds
}
function Get-DevState([string]$ParentHash,$Seeds) {
    Assert-File $DevStateFile
    $D = Get-Content -LiteralPath $DevStateFile -Raw | ConvertFrom-Json -AsHashtable
    if ($D -isnot [Collections.IDictionary] -or $D.Count -ne 3 -or
        $D.id -cne 'kilo-team-f05-development-v1' -or $D.parentHash -cne $ParentHash -or
        $D.files -isnot [Collections.IDictionary] -or $D.files.Count -ne $DevNames.Count) {
        throw 'Registro de desarrollo incompatible; preservar.'
    }
    foreach ($Name in $DevNames) {
        if (-not $D.files.Contains($Name) -or $D.files[$Name] -cne (Get-BytesHash $Seeds[$Name])) {
            throw "Baseline de desarrollo incompatible: $Name"
        }
    }
    $D
}
function Get-DevSnapshot([string]$ParentHash,[string]$RegistryHash,$D) {
    $Snapshot = [ordered]@{}
    foreach ($Name in $DevNames) {
        $Path = Join-Path $Workspace $Name
        $Hash = Get-Hash $Path
        $IsBaseline = $Hash -ceq $D.files[$Name]
        if ($DevOwners[$Name] -ceq 'protected' -and -not $IsBaseline) { throw "Contrato o prueba protegida cambiada: $Name" }
        $Snapshot[$Name] = $Hash
    }
    $Lines = @($ParentHash,$RegistryHash)
    foreach ($Name in $DevNames) { $Lines += "$Name=$($Snapshot[$Name])" }
    $Digest = Get-BytesHash ([Text.Encoding]::UTF8.GetBytes(($Lines -join "`n")))
    [pscustomobject]@{ hashes=$Snapshot; digest=$Digest }
}
function Assert-KnownCollisions {
    # Preflight limitado a rutas conocidas; no leer configuracion, auth ni tokens.
    if (Test-Path -LiteralPath (Join-Path $env:LOCALAPPDATA 'KiloTeam-F04-Lab\ownership.json')) {
        throw 'Registro F04 presente. Retirar mediante su procedimiento historico.'
    }
    $Locations = @(
        (Join-Path $HOME '.config\kilo'),
        (Join-Path $env:APPDATA 'Kilo Desktop\plugins\kilo.core\agent\runtime\config\kilo')
    )
    foreach ($Location in $Locations) {
        if (-not (Test-Path -LiteralPath $Location)) { continue }
        Assert-Directory $Location
        Assert-Absent $Location 'AGENTS.md'
        foreach ($Name in @('agent','agents')) {
            $Dir = Join-Path $Location $Name
            if (-not (Test-Path -LiteralPath $Dir)) { continue }
            foreach ($Agent in $AgentNames) { Assert-Absent $Dir $Agent }
        }
    }
    $Claude = Join-Path $HOME '.claude'
    if (Test-Path -LiteralPath $Claude) {
        Assert-Absent $Claude 'CLAUDE.md'
        $Dir = Join-Path $Claude 'agents'
        if (Test-Path -LiteralPath $Dir) {
            foreach ($Agent in $AgentNames) { Assert-Absent $Dir $Agent }
        }
    }
}

try {
    if (-not $IsWindows -or $PSVersionTable.PSVersion.Major -lt 7) { throw 'Requiere Windows y PowerShell 7.' }
    if (-not $env:LOCALAPPDATA -or -not $env:APPDATA) { throw 'Rutas de usuario no disponibles.' }
    Assert-Directory $env:LOCALAPPDATA
    $Root = [IO.Path]::GetFullPath((Join-Path $env:LOCALAPPDATA 'KiloTeam-F05-Lab'))
    $Workspace = Join-Path $Root 'workspace'
    $StateFile = Join-Path $Root 'ownership.json'
    $AuxiliaryFile = Join-Path $Workspace '.kilo\.gitignore'
    $EditStateFile = Join-Path $Root 'editing-ownership.json'
    $EditFixture = Join-Path $Workspace 'messages-f05.json'
    $Repo = Split-Path -Parent $PSScriptRoot
    $Roles = @('architect','frontend','backend','data','platform','research','quality','security','editorial')
    $AgentNames = @($Roles | ForEach-Object { "team-$_.md" })
    $RelativeFiles = @('AGENTS.md','kilo.jsonc','fixture.txt') + @($AgentNames | ForEach-Object { ".kilo/agents/$_" })
    $DevStateFile = Join-Path $Root 'development-ownership.json'
    $DevOwners = [ordered]@{
        'f05-contract.md'='protected'
        'f05-acceptance.test.mjs'='protected'
        'f05-data.mjs'='team-data'
        'f05-service.mjs'='team-backend'
        'f05-view.mjs'='team-frontend'
        'f05-run.ps1'='team-platform'
    }
    $DevNames = @($DevOwners.Keys)

    if ($Modo -eq 'Preparar') {
        if (-not $ConfirmarKiloCerrado -or -not $ConfirmarPrueba) { throw 'Requiere autorizacion de prueba y confirmacion de Kilo cerrado.' }
        if ($Modelo -cnotmatch '^[^/\s]+/[^\s]+$') { throw 'Indicar referencia providerID/modelID autorizada; no hay modelo por defecto.' }
        if ($env:XDG_CONFIG_HOME -or $env:KILO_CONFIG_DIR -or $env:KILO_CONFIG -or $env:KILO_CONFIG_CONTENT) { throw 'Overrides presentes en PowerShell; revisar antes de preparar.' }
        Assert-Absent $env:LOCALAPPDATA 'KiloTeam-F05-Lab'
        Assert-KnownCollisions
        $Files = [ordered]@{}
        foreach ($Name in $AgentNames) {
            $Source = Join-Path $Repo "team\agents\$Name"
            Assert-File $Source
            $Bytes = [IO.File]::ReadAllBytes($Source)
            $Text = [Text.Encoding]::UTF8.GetString($Bytes)
            if ($Text -notmatch '(?m)^Versión del archivo: 0\.2\.0 \|' -or $Text -notmatch '(?m)^mode: subagent\s*$' -or $Text -match '(?m)^model:') { throw "Candidato incompatible: $Name" }
            $Files[".kilo/agents/$Name"] = $Bytes
        }
        $Source = Join-Path $Repo 'team\policies\AGENTS.md'
        Assert-File $Source
        $Policy = [IO.File]::ReadAllText($Source)
        if ($Policy -notmatch '(?m)^Versión del archivo: 0\.17\.0 \|') { throw 'Version de politica inesperada.' }
        $Marker = 'KTEAM-F05-' + [guid]::NewGuid().ToString('N')
        $NL = [Environment]::NewLine
        $Policy += $NL + $NL + '## Control temporal F05 (solo evaluacion)' + $NL + "Al solicitar KTEAM-F05-LOAD, devuelve este marcador desde las instrucciones cargadas, sin leer archivos: $Marker" + $NL
        $Files['AGENTS.md'] = [Text.Encoding]::UTF8.GetBytes($Policy)
        $Config = [ordered]@{ '$schema'='https://app.kilo.ai/config.json'; model=$Modelo; subagent_model=$Modelo }
        $Files['kilo.jsonc'] = [Text.Encoding]::UTF8.GetBytes(($Config | ConvertTo-Json -Depth 4))
        $Files['fixture.txt'] = [Text.Encoding]::UTF8.GetBytes('F05-DISCOVERY-FIXTURE: inventario ficticio de tres cajas.' + $NL + 'No modificar en F05.3.' + $NL)
        $Hashes = [ordered]@{}
        foreach ($Rel in $RelativeFiles) { $Hashes[$Rel] = Get-BytesHash $Files[$Rel] }
        $State = [ordered]@{ id='kilo-team-f05-lab-v1'; root=$Root; policyVersion='0.17.0'; agentVersion='0.2.0'; marker=$Marker; files=$Hashes }
        # Directorio exclusivo. Registro previo a escritura de workspace.
        New-Item -ItemType Directory -Path $Root | Out-Null
        Write-New $StateFile ([Text.Encoding]::UTF8.GetBytes(($State | ConvertTo-Json -Depth 5)))
        foreach ($Dir in @($Workspace,(Join-Path $Workspace '.kilo'),(Join-Path $Workspace '.kilo\agents'))) {
            New-Item -ItemType Directory -Path $Dir | Out-Null
            Assert-Directory $Dir
        }
        foreach ($Rel in $RelativeFiles) { Write-New (Join-Path $Workspace $Rel) $Files[$Rel] }
        Assert-Tree
        foreach ($Rel in $RelativeFiles) {
            if ((Get-Status (Join-Path $Workspace $Rel) $Hashes[$Rel]) -cne 'MATCH') { throw "Integridad posterior: $Rel" }
        }
        Write-Host "F05_PREPARADO_LOCAL: $Workspace"
        Write-Host 'Configuracion global no modificada por este script. Runtime NOT_RUN.'
        exit 0
    }

    if (-not (Test-Path -LiteralPath $Root)) {
        if ($Modo -eq 'Diagnostico') { Write-Host 'F05_AUSENTE: sin laboratorio en ruta conocida.'; exit 0 }
        throw 'Laboratorio ausente.'
    }
    if ($Modo -in @('VerificarEdicion','RetirarEdicion')) { Assert-Tree -PermitirAuxiliar -PermitirEdicion }
    elseif ($Modo -in @('VerificarDesarrollo','RetirarDesarrollo')) { Assert-Tree -PermitirAuxiliar -PermitirDesarrollo }
    else { Assert-Tree -PermitirAuxiliar }
    $AuxiliaryStatus = Get-AuxiliaryStatus
    $StateHash = Get-Hash $StateFile
    $State = Get-State
    $Results = [ordered]@{}
    foreach ($Rel in $RelativeFiles) { $Results[$Rel] = Get-Status (Join-Path $Workspace $Rel) $State.files[$Rel] }

    if ($Modo -in @('PrepararDesarrollo','VerificarDesarrollo','RetirarDesarrollo')) {
        if (@($Results.Values | Where-Object { $_ -cne 'MATCH' }).Count -ne 0) { throw 'Baseline original incompleto o cambiado; preservar.' }
        if ($ComprobarMarcador) { throw 'No repetir marcador en fase desarrollo.' }
        $Results.GetEnumerator() | Format-Table Key,Value -AutoSize
        $Seeds = Get-DevSeed
        if ($Modo -eq 'PrepararDesarrollo') {
            if (-not $ConfirmarKiloCerrado -or -not $ConfirmarPrueba) { throw 'Requiere autorizacion de prueba y cierre de Kilo.' }
            Assert-Absent $Root 'development-ownership.json'
            foreach ($Name in $DevNames) { Assert-Absent $Workspace $Name }
            $Baseline = [ordered]@{}
            foreach ($Name in $DevNames) { $Baseline[$Name] = Get-BytesHash $Seeds[$Name] }
            $D = [ordered]@{ id='kilo-team-f05-development-v1'; parentHash=$StateHash; files=$Baseline }
            Write-New $DevStateFile ([Text.Encoding]::UTF8.GetBytes(($D | ConvertTo-Json -Depth 4)))
            foreach ($Name in $DevNames) { Write-New (Join-Path $Workspace $Name) $Seeds[$Name] }
            Assert-Tree -PermitirAuxiliar -PermitirDesarrollo
            $D = Get-DevState $StateHash $Seeds
            foreach ($Name in $DevNames) {
                if ((Get-Hash (Join-Path $Workspace $Name)) -cne $D.files[$Name]) { throw "Preparacion incompleta: $Name" }
                Write-Host "$($Name): BASELINE; propietario: $($DevOwners[$Name])"
            }
            foreach ($Rel in $RelativeFiles) {
                if ((Get-Status (Join-Path $Workspace $Rel) $State.files[$Rel]) -cne 'MATCH') { throw "Baseline cambiado: $Rel" }
            }
            if ((Get-Hash $StateFile) -cne $StateHash) { throw 'Registro original cambiado.' }
            Write-Host 'PASS_F05_DESARROLLO_PREPARADO; runtime NOT_RUN.'
            exit 0
        }
        $DevStateHash = Get-Hash $DevStateFile
        $D = Get-DevState $StateHash $Seeds
        $Snap = Get-DevSnapshot $StateHash $DevStateHash $D
        foreach ($Name in $DevNames) {
            $Status = if ($Snap.hashes[$Name] -ceq $D.files[$Name]) { 'BASELINE' } else { 'CHANGED_UNREVIEWED' }
            Write-Host "$($Name): $Status; propietario: $($DevOwners[$Name]); SHA256: $($Snap.hashes[$Name])"
        }
        if ((Get-Hash $StateFile) -cne $StateHash -or (Get-Hash $DevStateFile) -cne $DevStateHash) { throw 'Registro cambiado.' }
        if ($Modo -eq 'VerificarDesarrollo') {
            Write-Host "Huella de revision: $($Snap.digest)"
            Write-Host 'PASS_F05_INTEGRIDAD_DESARROLLO; codigo no ejecutado ni aceptado.'
            exit 0
        }
        if (-not $ConfirmarKiloCerrado -or -not $ConfirmarRetirada -or $HuellaAprobada -cnotmatch '^[0-9A-F]{64}$' -or
            $HuellaAprobada -cne $Snap.digest) { throw 'Requiere cierre, retirada y huella exacta revisada; preservar.' }
        Assert-Tree -PermitirAuxiliar -PermitirDesarrollo
        $Again = Get-DevSnapshot $StateHash $DevStateHash $D
        if ($Again.digest -cne $Snap.digest -or (Get-Hash $StateFile) -cne $StateHash -or (Get-Hash $DevStateFile) -cne $DevStateHash) { throw 'Estado cambiado; preservar.' }
        foreach ($Name in $DevNames) {
            $Path = Join-Path $Workspace $Name
            if ((Get-Hash $Path) -cne $Snap.hashes[$Name]) { throw "Archivo cambiado: $Name" }
            Remove-Item -LiteralPath $Path -ErrorAction Stop
        }
        if ((Get-Hash $DevStateFile) -cne $DevStateHash) { throw 'Registro de desarrollo cambiado; preservar.' }
        Remove-Item -LiteralPath $DevStateFile -ErrorAction Stop
        Assert-Tree -PermitirAuxiliar
        Write-Host 'F05_DESARROLLO_RETIRADO; baseline original conservado.'
        exit 0
    }

    if ($Modo -in @('PrepararEdicion','VerificarEdicion','RetirarEdicion')) {
        if (@($Results.Values | Where-Object { $_ -cne 'MATCH' }).Count -ne 0) { throw 'Baseline original incompleto o cambiado; preservar.' }
        if ($ComprobarMarcador) { throw 'No repetir marcador en fase editorial.' }
        $Results.GetEnumerator() | Format-Table Key,Value -AutoSize
        if ($Modo -eq 'PrepararEdicion') {
            if (-not $ConfirmarKiloCerrado -or -not $ConfirmarPrueba) { throw 'Requiere autorizacion de prueba y cierre de Kilo.' }
            Assert-Absent $Root 'editing-ownership.json'
            Assert-Absent $Workspace 'messages-f05.json'
            $E = [ordered]@{ id='kilo-team-f05-editorial-v1'; parentHash=$StateHash; relativePath='messages-f05.json'; owner='team-editorial'; baseline=(Get-EditBaselineHash) }
            Write-New $EditStateFile ([Text.Encoding]::UTF8.GetBytes(($E | ConvertTo-Json -Depth 3)))
            Write-New $EditFixture ([Text.Encoding]::UTF8.GetBytes((Get-EditFixture) + "`n"))
            Assert-Tree -PermitirAuxiliar -PermitirEdicion
            $null = Get-EditState $StateHash
            if ((Get-EditStatus) -cne 'BASELINE' -or (Get-Hash $StateFile) -cne $StateHash) { throw 'Preparacion editorial incompleta.' }
            foreach ($Rel in $RelativeFiles) {
                if ((Get-Status (Join-Path $Workspace $Rel) $State.files[$Rel]) -cne 'MATCH') { throw "Baseline cambiado: $Rel" }
            }
            Write-Host 'messages-f05.json: BASELINE; propietario: team-editorial'
            Write-Host 'PASS_F05_EDICION_PREPARADA; runtime NOT_RUN.'
            exit 0
        }
        $EditStateHash = Get-Hash $EditStateFile
        $null = Get-EditState $StateHash
        $EditStatus = Get-EditStatus
        Write-Host "messages-f05.json: $EditStatus"
        if ($Modo -eq 'VerificarEdicion') {
            if ($EditStatus -cne 'EXPECTED_EDIT') { throw 'Edicion esperada no realizada.' }
            if ((Get-Hash $EditStateFile) -cne $EditStateHash -or (Get-Hash $StateFile) -cne $StateHash) { throw 'Registro cambiado.' }
            Write-Host 'PASS_F05_EDICION_VERIFICADA; no acredita autor, herramientas ni permisos.'
            exit 0
        }
        if (-not $ConfirmarKiloCerrado -or -not $ConfirmarRetirada) { throw 'Requiere cierre y retirada editorial autorizada.' }
        $EditHash = Get-Hash $EditFixture
        if ((Get-EditStatus) -cne $EditStatus -or (Get-Hash $EditFixture) -cne $EditHash -or
            (Get-Hash $EditStateFile) -cne $EditStateHash -or (Get-Hash $StateFile) -cne $StateHash) { throw 'Estado editorial cambiado; preservar.' }
        Remove-Item -LiteralPath $EditFixture -ErrorAction Stop
        if ((Get-Hash $EditStateFile) -cne $EditStateHash) { throw 'Registro editorial cambiado; preservar.' }
        Remove-Item -LiteralPath $EditStateFile -ErrorAction Stop
        Assert-Tree -PermitirAuxiliar
        Write-Host 'F05_EDICION_RETIRADA; baseline original conservado.'
        exit 0
    }

    if ($Modo -in @('Diagnostico','Verificar')) {
        $Results.GetEnumerator() | Format-Table Key,Value -AutoSize
        $Complete = @($Results.Values | Where-Object { $_ -cne 'MATCH' }).Count -eq 0
        $MarkerStatus = 'NOT_RUN'
        if ($Modo -eq 'Verificar' -and $ComprobarMarcador) {
            $Received = Read-Host 'Marcador devuelto por Code (no compartirlo en Git ni chat externo)'
            $MarkerStatus = if ($Received -ceq $State.marker) { 'MATCH' } else { 'MISMATCH' }
        }
        Write-Host "Workspace: $Workspace"
        Write-Host "Auxiliar .kilo/.gitignore: $AuxiliaryStatus (no incluido en propiedad)"
        Write-Host "Integridad: $(if ($Complete) {'MATCH'} else {'INCOMPLETE_OR_DRIFT'}); Marcador: $MarkerStatus"
        if (-not $Complete -or $MarkerStatus -eq 'MISMATCH') { throw 'Verificacion incompleta o deriva.' }
        if ($MarkerStatus -eq 'MATCH') { Write-Host 'PASS_LOAD_REPORTED (no certifica descubrimiento ni permisos).' }
        else { Write-Host 'PASS_INTEGRIDAD_LOCAL; runtime NOT_RUN por el script.' }
        exit 0
    }

    if (-not $ConfirmarKiloCerrado -or -not $ConfirmarRetirada) { throw 'Requiere confirmacion de cierre y retirada.' }
    if (@($Results.Values | Where-Object { $_ -eq 'DRIFT' }).Count -ne 0) { throw 'Deriva: conservar registro y archivos, revisar.' }
    if ((Get-Hash $StateFile) -cne $StateHash) { throw 'Registro cambiado.' }
    # No iniciar retirada parcial por un auxiliar sin consentimiento.
    if ($AuxiliaryStatus -eq 'MATCH_TEMPLATE') {
        if (-not $ConfirmarRetiradaAuxiliar) { throw 'Auxiliar no propio presente; requiere ConfirmarRetiradaAuxiliar para retirar la plantilla conocida.' }
        $AuxiliaryHash = Get-Hash $AuxiliaryFile
        if ((Get-AuxiliaryStatus) -cne 'MATCH_TEMPLATE' -or (Get-Hash $AuxiliaryFile) -cne $AuxiliaryHash) { throw 'Auxiliar cambiado; preservar.' }
        Remove-Item -LiteralPath $AuxiliaryFile -ErrorAction Stop
    }
    Assert-Tree
    foreach ($Rel in $RelativeFiles) {
        $Path = Join-Path $Workspace $Rel
        if (Test-Path -LiteralPath $Path) {
            if ((Get-Hash $Path) -cne $State.files[$Rel]) { throw "Archivo cambiado: $Rel" }
            Remove-Item -LiteralPath $Path -ErrorAction Stop
        }
    }
    # Sin borrado recursivo: un directorio no vacio detiene retirada.
    foreach ($Dir in @((Join-Path $Workspace '.kilo\agents'),(Join-Path $Workspace '.kilo'),$Workspace)) {
        if (Test-Path -LiteralPath $Dir) { Assert-Directory $Dir; [IO.Directory]::Delete($Dir,$false) }
    }
    Assert-Tree
    if ((Get-Hash $StateFile) -cne $StateHash) { throw 'Registro cambiado.' }
    Remove-Item -LiteralPath $StateFile -ErrorAction Stop
    [IO.Directory]::Delete($Root,$false)
    Write-Host 'F05_RETIRADO: archivos propios y directorios vacios retirados.'
    exit 0
} catch {
    Write-Error -Message ("F05_BLOCKED: " + $_.Exception.Message) -ErrorAction Continue
    exit 1
}
