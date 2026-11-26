# KILO-GLOBAL-HARNESS-TEAM
# Version: 0.1.3
# Fecha: 2026-11-26
# F06-LAB-R1/R2: comparación local y fixture descartable; no instalador.
# Exit 0: operación acotada completada; 1: error/bloqueo.
[CmdletBinding()]
param(
    [ValidateSet('Diagnostico','Preparar','Verificar','Retirar','PrepararR2','VerificarR2','RetirarR2')]
    [string]$Modo = 'Diagnostico',
    [string]$Modelo,
    [switch]$ConfirmarKiloCerrado,
    [switch]$ConfirmarPrueba,
    [switch]$ConfirmarRetirada,
    [switch]$ConfirmarRetiradaAuxiliar,
    [switch]$ComprobarMarcador,
    [string]$BaselineDigest,
    [string]$CandidateDigest
)
Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'
$Revision = '86e11637ace4cfa4794946af8b0af34c7173626b'
$Pins = [ordered]@{
    'team/policies/AGENTS.md' = '4e22014ed876874bec688bb690f61ed74d83ecd0'
    'team/agents/team-architect.md' = '71d3cc2d43abd6d315ce76a28a71c92f3490c6dc'
    'team/agents/team-frontend.md' = '96814fa474f785132f8824b2457e80ff31876d9e'
    'team/agents/team-backend.md' = 'a96b40ae489d853e5b4733cd60c8583b296e985c'
    'team/agents/team-data.md' = 'f2c88e23656b5a827d1ebd3ad4bdca9ef019758f'
    'team/agents/team-platform.md' = '8b055c4c45649e678c22216e28ebc4dc2bc79b7d'
    'team/agents/team-research.md' = '214b2df5dd9216304b971f874a40fe87015c9657'
    'team/agents/team-quality.md' = 'b5f6c603e032e349afde41a2ab732188d77415ee'
    'team/agents/team-security.md' = 'e5a166d41a245e791ce0aeaed242e5ab5bec695d'
    'team/agents/team-editorial.md' = 'b2fc0e762574295abf320d4e084fa7eaac6bc1a4'
    'team/skills/team-routing/SKILL.md' = '338c11cd5250f6db110518276beb0b881dc331b6'
    'team/skills/team-task-contract/SKILL.md' = 'c235a205f341c3feb530db30880999feb619663a'
    'team/skills/team-coordination/SKILL.md' = 'bcad80849f1fcc05349421cc95eab51f438cff13'
    'team/skills/team-context-recovery/SKILL.md' = 'dcaaadb986d07ef5c143cde143b82fb06a4f54ab'
    'team/skills/requirements-acceptance/SKILL.md' = '43e1b9d84550b75bc5e44ea5aa0c28bc4049c2f0'
    'team/skills/architecture-decisions/SKILL.md' = 'b4672adb364192aa96c40f507cc9344ea9287c8d'
    'team/skills/implementation-discipline/SKILL.md' = '1901db53f6f515ffc0027edd8fc97fec5e649bc4'
    'team/skills/systematic-debugging/SKILL.md' = '2c116ea30cea465a510b1b20fa73aeec74fea298'
    'team/skills/focused-testing/SKILL.md' = 'f74c83e462adfa26932d9960ce9515a0550f33ef'
    'team/skills/git-workflow/SKILL.md' = '3785c8a7a790c0df7af12cdd1c7668f17c5de3a2'
    'team/skills/tool-mcp-discovery/SKILL.md' = '4718a496055d32868587b67c5eac8fc40a9043a3'
    'team/skills/secure-development/SKILL.md' = '7e63d55058a916cfacf02517b28740ea6b7c3b6e'
    'team/skills/skill-authoring/SKILL.md' = '28e7b30eda8229fdc46ff7b0213dd14a82084207'
    'team/skills/focused-testing/references/quality-baseline.md' = '39ab4c81ea41b8f6d9331996727a5c67aeb38861'
}
$R2Pins = [ordered]@{
    'tests/fixtures/f06-reservation/reservation.mjs' = '4e4ffde9656c6b9604961ce733d86f4910d28fcb'
    'tests/fixtures/f06-reservation/reservation.test.mjs' = '9f87d6702902f07048fcc49e3ba21f1e4c30f1c6'
    'tests/fixtures/f06-reservation/contract.md' = 'eb18a875089fc06ddc6b30d8c997bd445a3fbbff'
}
$Variants = @('baseline','candidate')
$Utf8 = [Text.UTF8Encoding]::new($false,$true)

function Assert-Directory([string]$Path) {
    $Dir = [IO.DirectoryInfo]::new([IO.Path]::GetFullPath($Path))
    while ($null -ne $Dir) {
        $Item = Get-Item -LiteralPath $Dir.FullName -Force
        if (-not $Item.PSIsContainer -or ($Item.Attributes -band [IO.FileAttributes]::ReparsePoint)) { throw 'Directorio inseguro o enlace; preservar.' }
        $Dir = $Dir.Parent
    }
}
function Assert-File([string]$Path) {
    Assert-Directory (Split-Path -Parent $Path)
    $Item = Get-Item -LiteralPath $Path -Force
    if ($Item.PSIsContainer -or ($Item.Attributes -band [IO.FileAttributes]::ReparsePoint)) { throw 'Archivo inseguro o enlace; preservar.' }
}
function Get-Sha256([byte[]]$Bytes) {
    [Convert]::ToHexString([Security.Cryptography.SHA256]::HashData($Bytes))
}
function Get-FileDigest([string]$Path) {
    Assert-File $Path
    (Get-FileHash -LiteralPath $Path -Algorithm SHA256).Hash
}
function Get-PinnedBytes([string]$Relative, $ExpectedPins = $Pins) {
    $Path = Join-Path $Repo $Relative
    Assert-File $Path
    # Git blob SHA-1 identifica la revisión pública; SHA-256 protege los archivos locales.
    # Normalizar CRLF de checkout Windows; no aceptar BOM, otro encoding o cambios semánticos.
    $Raw = [IO.File]::ReadAllBytes($Path)
    $Text = $Utf8.GetString($Raw).Replace("`r`n","`n")
    $Bytes = $Utf8.GetBytes($Text)
    $Header = [Text.Encoding]::ASCII.GetBytes("blob $($Bytes.Length)" + [char]0)
    $Blob = [Convert]::ToHexString([Security.Cryptography.SHA1]::HashData([byte[]]($Header + $Bytes))).ToLowerInvariant()
    if ($Blob -cne $ExpectedPins[$Relative]) { throw "Fuente distinta de revisión fijada: $Relative" }
    return ,$Bytes
}
function Write-New([string]$Path,[byte[]]$Bytes) {
    Assert-Directory (Split-Path -Parent $Path)
    $Stream = [IO.File]::Open($Path,[IO.FileMode]::CreateNew,[IO.FileAccess]::Write,[IO.FileShare]::None)
    try { $Stream.Write($Bytes,0,$Bytes.Length); $Stream.Flush($true) } finally { $Stream.Dispose() }
}
function Assert-Absent([string]$Parent,[string]$Name) {
    Assert-Directory $Parent
    if (@(Get-ChildItem -LiteralPath $Parent -Force | Where-Object Name -IEQ $Name).Count -ne 0) { throw "Colisión de entrada conocida: $Name" }
}
function Get-Payloads([string]$Model,[string]$Marker) {
    if ($Model -cnotmatch '^[A-Za-z0-9_.-]+/[A-Za-z0-9_.:/+-]+$' -or $Marker -cnotmatch '^KTEAM-F06-[0-9a-f]{32}$') { throw 'Modelo/marcador inválido.' }
    $Files = [ordered]@{}
    $Policy = $Utf8.GetString((Get-PinnedBytes 'team/policies/AGENTS.md'))
    # El mismo marcador y política en ambas variantes; no usar el marcador para inferir variante.
    $Policy += "`n`n## Control temporal F06 (solo laboratorio)`nAl solicitar KTEAM-F06-LOAD, devuelve el marcador desde instrucciones cargadas sin leer archivos: $Marker`n"
    $Config = [ordered]@{ '$schema'='https://app.kilo.ai/config.json'; model=$Model; subagent_model=$Model }
    $ConfigBytes = $Utf8.GetBytes(($Config | ConvertTo-Json -Depth 4 -Compress))
    $Fixture = $Utf8.GetBytes("F06-FIXTURE: inventario ficticio de tres cajas.`nSolo lectura; no modificar archivos ni consultar red.`n")
    foreach ($Variant in $Variants) {
        $Files["$Variant/AGENTS.md"] = $Utf8.GetBytes($Policy)
        $Files["$Variant/kilo.jsonc"] = $ConfigBytes
        $Files["$Variant/fixture.txt"] = $Fixture
        foreach ($Source in $Pins.Keys) {
            if ($Source.StartsWith('team/agents/')) {
                $Rel = $Source.Substring('team/agents/'.Length)
                $Files["$Variant/.kilo/agents/$Rel"] = Get-PinnedBytes $Source
            } elseif ($Variant -ceq 'candidate' -and $Source.StartsWith('team/skills/')) {
                $Rel = $Source.Substring('team/skills/'.Length)
                $Files["$Variant/.kilo/skills/$Rel"] = Get-PinnedBytes $Source
            }
        }
    }
    return $Files
}
function Get-Dirs($Files) {
    $Dirs = [Collections.Generic.HashSet[string]]::new([StringComparer]::Ordinal)
    foreach ($Rel in $Files.Keys) {
        $Parent = [IO.Path]::GetDirectoryName($Rel).Replace('\','/')
        while ($Parent) {
            [void]$Dirs.Add($Parent)
            $Parent = [IO.Path]::GetDirectoryName($Parent)
            if ($Parent) { $Parent = $Parent.Replace('\','/') }
        }
    }
    return @($Dirs | Sort-Object { ($_ -split '/').Count }, { $_ })
}
function Get-AuxiliaryStatus([string]$Variant) {
    $Path = Join-Path $Root "$Variant/.kilo/.gitignore"
    if (-not (Test-Path -LiteralPath $Path)) { return 'ABSENT' }
    Assert-File $Path
    $Expected = @('node_modules','package.json','package-lock.json','pnpm-lock.yaml','bun.lock','yarn.lock','.gitignore','agent-manager.json')
    $Actual = [IO.File]::ReadAllLines($Path)
    if ($Actual.Count -ne $Expected.Count) { throw 'Auxiliar distinto de plantilla auditada; preservar.' }
    for ($i=0; $i -lt $Expected.Count; $i++) {
        if ($Actual[$i] -cne $Expected[$i]) { throw 'Auxiliar distinto de plantilla auditada; preservar.' }
    }
    return 'MATCH_TEMPLATE'
}
function Assert-Tree($Files) {
    $Dirs = @(Get-Dirs $Files)
    foreach ($Dir in @('') + $Dirs) {
        $Path = if ($Dir) { Join-Path $Root $Dir } else { $Root }
        Assert-Directory $Path
        foreach ($Item in Get-ChildItem -LiteralPath $Path -Force) {
            $Rel = if ($Dir) { "$Dir/$($Item.Name)" } else { $Item.Name }
            if ($Item.Attributes -band [IO.FileAttributes]::ReparsePoint) { throw 'Entrada enlazada; preservar.' }
            if ($Rel -ceq 'ownership.json' -or $Rel -cin $Files.Keys) {
                if ($Item.PSIsContainer) { throw 'Tipo de entrada inesperado.' }
            } elseif ($Rel -cin $Dirs) {
                if (-not $Item.PSIsContainer) { throw 'Tipo de directorio inesperado.' }
            } elseif ($Rel -cin @('baseline/.kilo/.gitignore','candidate/.kilo/.gitignore')) {
                if ($Item.PSIsContainer -or (Get-AuxiliaryStatus ($Rel.Split('/')[0])) -cne 'MATCH_TEMPLATE') { throw 'Auxiliar no reconocido.' }
            } else { throw "Entrada no administrada: $Rel; preservar." }
        }
    }
}
function Get-State {
    Assert-File $StateFile
    $State = [IO.File]::ReadAllText($StateFile) | ConvertFrom-Json -AsHashtable
    if ($State -isnot [Collections.IDictionary] -or $State.Count -ne 6 -or
        $State.id -cne 'kilo-team-f06-lab-v1' -or $State.root -cne $Root -or $State.revision -cne $Revision -or
        $State.files -isnot [Collections.IDictionary]) { throw 'Registro incompatible; preservar.' }
    $Files = Get-Payloads $State.model $State.marker
    if ($Files.Count -ne 38 -or $State.files.Count -ne $Files.Count) { throw 'Inventario de registro inesperado.' }
    foreach ($Rel in $Files.Keys) {
        if (-not $State.files.Contains($Rel) -or $State.files[$Rel] -cne (Get-Sha256 $Files[$Rel])) { throw "Registro/fuente no coincide: $Rel" }
    }
    return [pscustomobject]@{ State=$State; Files=$Files }
}
function Confirm-Integrity($Record, $Extension = $null) {
    $TreeFiles = [ordered]@{}
    foreach ($Rel in $Record.Files.Keys) { $TreeFiles[$Rel] = $Record.Files[$Rel] }
    if ($null -ne $Extension) {
        foreach ($Rel in $Extension.Keys) {
            if ($TreeFiles.Contains($Rel)) { throw 'Solape de extensión.' }
            $TreeFiles[$Rel] = $Extension[$Rel]
        }
    }
    Assert-Tree $TreeFiles
    foreach ($Rel in $Record.Files.Keys) {
        if ((Get-FileDigest (Join-Path $Root $Rel)) -cne $Record.State.files[$Rel]) { throw "Deriva: $Rel; preservar." }
    }
    foreach ($Variant in $Variants) { Write-Host "$Variant auxiliar: $(Get-AuxiliaryStatus $Variant)" }
    Write-Host "MATCH: $($Record.Files.Count) archivos protegidos (integridad local, no runtime)."
}
function Get-R2Payload {
    $Files = [ordered]@{}
    foreach ($Variant in $Variants) {
        foreach ($Source in $R2Pins.Keys) {
            $Name = [IO.Path]::GetFileName($Source)
            $Files["$Variant/r2/$Name"] = Get-PinnedBytes $Source $R2Pins
        }
    }
    $Hashes = [ordered]@{}
    foreach ($Rel in $Files.Keys) { $Hashes[$Rel] = Get-Sha256 $Files[$Rel] }
    $State = [ordered]@{ id = 'kilo-team-f06-r2-reservation-v1'; revision = $Revision; files = $Hashes }
    $Files['r2-ownership.json'] = $Utf8.GetBytes(($State | ConvertTo-Json -Depth 4 -Compress))
    return $Files
}
function Confirm-R2($Record, $Extra) {
    Confirm-Integrity $Record $Extra
    $Digests = [ordered]@{}
    foreach ($Rel in $Extra.Keys) {
        $Digest = Get-FileDigest (Join-Path $Root $Rel)
        $Expected = Get-Sha256 $Extra[$Rel]
        if ($Rel -cin @('baseline/r2/reservation.mjs','candidate/r2/reservation.mjs')) {
            $Digests[$Rel] = $Digest
            $Status = if ($Digest -ceq $Expected) { 'BASELINE' } else { 'CHANGED_UNREVIEWED' }
            Write-Host "$Rel : $Status $Digest"
        } elseif ($Digest -cne $Expected) {
            throw "Deriva protegida R2: $Rel; preservar."
        }
    }
    Write-Host 'R2_PROTECTED_MATCH: 4 archivos y registro; no certifica código ni autor.'
    return $Digests
}
function Invoke-R2($Record) {
    if ($ComprobarMarcador -or $Modelo -or $ConfirmarRetiradaAuxiliar) { throw 'Parámetro incompatible con R2.' }
    $Extra = Get-R2Payload
    if ($Extra.Count -ne 7) { throw 'Inventario R2 inesperado.' }
    $R2State = Join-Path $Root 'r2-ownership.json'
    if ($Modo -eq 'PrepararR2') {
        if (-not $ConfirmarKiloCerrado -or -not $ConfirmarPrueba) { throw 'Requiere autorización R2 y cierre de Kilo.' }
        if ($ConfirmarRetirada -or $BaselineDigest -or $CandidateDigest) { throw 'Parámetro incompatible con preparación.' }
        Confirm-Integrity $Record
        Assert-Absent $Root 'r2-ownership.json'
        foreach ($Variant in $Variants) { Assert-Absent (Join-Path $Root $Variant) 'r2' }
        Write-New $R2State $Extra['r2-ownership.json']
        foreach ($Variant in $Variants) {
            $Path = Join-Path $Root "$Variant/r2"
            New-Item -ItemType Directory -Path $Path -ErrorAction Stop | Out-Null
            Assert-Directory $Path
        }
        foreach ($Rel in $Extra.Keys) {
            if ($Rel -ceq 'r2-ownership.json') { continue }
            Write-New (Join-Path $Root $Rel) $Extra[$Rel]
        }
        [void](Confirm-R2 $Record $Extra)
        Write-Host 'F06_R2_PREPARADO'
        return
    }
    $Digests = Confirm-R2 $Record $Extra
    if ($Modo -eq 'VerificarR2') {
        if ($ConfirmarPrueba -or $ConfirmarRetirada -or $BaselineDigest -or $CandidateDigest) { throw 'Parámetro incompatible con verificación.' }
        Write-Host 'PASS_INTEGRIDAD_LOCAL_F06_R2 (código mutable no revisado)'
        return
    }
    if ($Modo -cne 'RetirarR2' -or -not $ConfirmarKiloCerrado -or -not $ConfirmarRetirada -or $ConfirmarPrueba) { throw 'Retirada R2 requiere autorización expresa y cierre.' }
    $Approved = @{ baseline = $BaselineDigest; candidate = $CandidateDigest }
    foreach ($Variant in $Variants) {
        $Rel = "$Variant/r2/reservation.mjs"
        $Expected = Get-Sha256 $Extra[$Rel]
        if ($Digests[$Rel] -cne $Expected) {
            if ($Approved[$Variant] -cnotmatch '^[A-F0-9]{64}$' -or $Approved[$Variant] -cne $Digests[$Rel]) { throw "Código R2 modificado sin huella revisada autorizada: $Variant." }
        } elseif ($Approved[$Variant] -and $Approved[$Variant] -cne $Expected) { throw 'Huella autorizada no coincide.' }
    }
    foreach ($Rel in $Extra.Keys) {
        if ($Rel -ceq 'r2-ownership.json') { continue }
        $Path = Join-Path $Root $Rel
        $Expected = if ($Digests.Contains($Rel)) { $Digests[$Rel] } else { Get-Sha256 $Extra[$Rel] }
        if ((Get-FileDigest $Path) -cne $Expected) { throw "Deriva durante retirada R2: $Rel; preservar." }
        Remove-Item -LiteralPath $Path -ErrorAction Stop
    }
    foreach ($Variant in $Variants) {
        $Path = Join-Path $Root "$Variant/r2"
        Assert-Directory $Path
        if (@(Get-ChildItem -LiteralPath $Path -Force).Count -ne 0) { throw 'Directorio R2 no vacío; preservar.' }
        [IO.Directory]::Delete($Path,$false)
    }
    if ((Get-FileDigest $R2State) -cne (Get-Sha256 $Extra['r2-ownership.json'])) { throw 'Registro R2 cambió; preservar.' }
    Remove-Item -LiteralPath $R2State -ErrorAction Stop
    Confirm-Integrity $Record
    Write-Host 'F06_R2_RETIRADO'
}
function Assert-KnownCollisions {
    # F04 histórico retira ownership.json pero conserva su directorio contenedor.
    # Solo tolerar la carpeta regular, vacía y sin enlaces; no modificarla.
    $F04Entries = @(Get-ChildItem -LiteralPath $env:LOCALAPPDATA -Force | Where-Object Name -IEQ 'KiloTeam-F04-Lab')
    if ($F04Entries.Count -gt 0) {
        if ($F04Entries.Count -ne 1 -or $F04Entries[0].Name -cne 'KiloTeam-F04-Lab' -or
            -not $F04Entries[0].PSIsContainer -or
            ($F04Entries[0].Attributes -band [IO.FileAttributes]::ReparsePoint)) { throw 'Entrada F04 insegura; preservar.' }
        Assert-Directory $F04Entries[0].FullName
        if (@(Get-ChildItem -LiteralPath $F04Entries[0].FullName -Force).Count -ne 0) {
            throw 'F04 contiene entradas; preservar y revisar registro mediante procedimiento histórico.'
        }
        Write-Host 'F04_EMPTY_CONTAINER: directorio histórico vacío, conservado.'
    }
    Assert-Absent $env:LOCALAPPDATA 'KiloTeam-F05-Lab'
    # Revisar únicamente rutas/nombres conocidos, sin leer configuraciones ni credenciales.
    $Homes = @(
        (Join-Path $HOME '.config/kilo'),
        (Join-Path $env:APPDATA 'Kilo Desktop/plugins/kilo.core/agent/runtime/config/kilo'),
        (Join-Path $HOME '.agents'),
        (Join-Path $HOME '.claude')
    )
    $AgentFiles = @($Pins.Keys | Where-Object { $_.StartsWith('team/agents/') } | ForEach-Object { [IO.Path]::GetFileName($_) })
    $SkillNames = @($Pins.Keys | Where-Object { $_ -match '^team/skills/([^/]+)/SKILL\.md$' } | ForEach-Object { $_.Split('/')[2] })
    foreach ($HomePath in $Homes) {
        if (-not (Test-Path -LiteralPath $HomePath)) { continue }
        Assert-Directory $HomePath
        foreach ($Instr in @('AGENTS.md','CLAUDE.md')) { Assert-Absent $HomePath $Instr }
        foreach ($Name in @('agents','agent','skills','skill')) {
            $Dir = Join-Path $HomePath $Name
            if (-not (Test-Path -LiteralPath $Dir)) { continue }
            foreach ($Entry in @($AgentFiles + $SkillNames)) { Assert-Absent $Dir $Entry }
        }
    }
    # No preparar bajo ancestros con proyecto/configuración visible; no leer archivos ajenos.
    $Ancestor = [IO.DirectoryInfo]::new($env:LOCALAPPDATA)
    while ($null -ne $Ancestor) {
        foreach ($Name in @('.git','.kilo','.kilocode','.agents','.claude','AGENTS.md','CLAUDE.md','kilo.json','kilo.jsonc')) {
            # .agents/.claude del HOME ya se revisan arriba; otros descubrimientos requieren control de sesión.
            if ($Ancestor.FullName -ieq [IO.Path]::GetFullPath($HOME) -and $Name -cin @('.agents','.claude')) { continue }
            Assert-Absent $Ancestor.FullName $Name
        }
        $Ancestor = $Ancestor.Parent
    }
}
try {
    if (-not $IsWindows -or $PSVersionTable.PSVersion.Major -lt 7) { throw 'Requiere Windows y PowerShell 7.' }
    if (-not $env:LOCALAPPDATA -or -not $env:APPDATA) { throw 'Rutas de usuario ausentes.' }
    Assert-Directory $env:LOCALAPPDATA
    $Root = [IO.Path]::GetFullPath((Join-Path $env:LOCALAPPDATA 'KiloTeam-F06-Lab'))
    $Repo = Split-Path -Parent $PSScriptRoot
    $StateFile = Join-Path $Root 'ownership.json'
    if ($Modo -cin @('PrepararR2','VerificarR2','RetirarR2')) {
        $Record = Get-State
        Invoke-R2 $Record
        exit 0
    }
    if ($BaselineDigest -or $CandidateDigest) { throw 'Huellas R2 no válidas para modo R1.' }
    if ($Modo -eq 'Diagnostico') {
        foreach ($Source in $Pins.Keys) { [void](Get-PinnedBytes $Source) }
        Write-Host "Fuentes fijadas MATCH: $($Pins.Count) ($Revision)."
        if (-not (Test-Path -LiteralPath $Root)) {
            Assert-Absent $env:LOCALAPPDATA 'KiloTeam-F06-Lab'
            Write-Host 'F06_AUSENTE'
        } else {
            $Record = Get-State
            Confirm-Integrity $Record
            Write-Host 'F06_PRESENTE'
        }
        exit 0
    }
    if ($Modo -eq 'Preparar') {
        if (-not $ConfirmarKiloCerrado -or -not $ConfirmarPrueba) { throw 'Requiere autorización de prueba y cierre ordenado de Kilo.' }
        if ($env:XDG_CONFIG_HOME -or $env:KILO_CONFIG_DIR -or $env:KILO_CONFIG -or $env:KILO_CONFIG_CONTENT) { throw 'Overrides presentes; revisar antes de preparar.' }
        Assert-Absent $env:LOCALAPPDATA 'KiloTeam-F06-Lab'
        Assert-KnownCollisions
        $Marker = 'KTEAM-F06-' + [guid]::NewGuid().ToString('N')
        $Files = Get-Payloads $Modelo $Marker
        if ($Files.Count -ne 38) { throw 'Cantidad inesperada de archivos.' }
        $Hashes = [ordered]@{}
        foreach ($Rel in $Files.Keys) { $Hashes[$Rel] = Get-Sha256 $Files[$Rel] }
        $State = [ordered]@{ id='kilo-team-f06-lab-v1'; root=$Root; revision=$Revision; model=$Modelo; marker=$Marker; files=$Hashes }
        # Creación exclusiva del directorio con guardas; registro antes de escribir los workspaces.
        New-Item -ItemType Directory -Path $Root -ErrorAction Stop | Out-Null
        Assert-Directory $Root
        Write-New $StateFile ($Utf8.GetBytes(($State | ConvertTo-Json -Depth 5 -Compress)))
        foreach ($Dir in (Get-Dirs $Files)) {
            New-Item -ItemType Directory -Path (Join-Path $Root $Dir) -ErrorAction Stop | Out-Null
            Assert-Directory (Join-Path $Root $Dir)
        }
        foreach ($Rel in $Files.Keys) { Write-New (Join-Path $Root $Rel) $Files[$Rel] }
        Confirm-Integrity (Get-State)
        foreach ($Variant in $Variants) { Write-Host "$Variant : $(Join-Path $Root $Variant)" }
        Write-Host 'F06_PREPARADO (sin certificación de carga).'
        exit 0
    }
    $Record = Get-State
    Confirm-Integrity $Record
    if ($Modo -eq 'Verificar') {
        if ($ComprobarMarcador) {
            foreach ($Variant in $Variants) {
                $Reported = Read-Host "Marcador de $Variant (no compartir en informes)" -MaskInput
                if ($Reported -cne $Record.State.marker) { throw "Marcador $Variant no coincide; no inferir carga." }
                Write-Host "$Variant : PASS_LOAD_REPORTED (política, no catálogo ni comportamiento)"
            }
        }
        Write-Host 'PASS_INTEGRIDAD_LOCAL_F06'
        exit 0
    }
    if (-not $ConfirmarKiloCerrado -or -not $ConfirmarRetirada) { throw 'Retirada requiere confirmación expresa y Kilo cerrado.' }
    $Aux = @($Variants | Where-Object { (Get-AuxiliaryStatus $_) -ceq 'MATCH_TEMPLATE' })
    if ($Aux.Count -gt 0 -and -not $ConfirmarRetiradaAuxiliar) { throw 'Se requiere confirmación de retirada de auxiliares reconocidos.' }
    # Revalidar todo antes de mutar. No adoptar hashes nuevos ni borrar recursivamente.
    Confirm-Integrity $Record
    foreach ($Rel in $Record.Files.Keys) {
        $Path = Join-Path $Root $Rel
        if ((Get-FileDigest $Path) -cne $Record.State.files[$Rel]) { throw "Deriva durante retirada: $Rel" }
        Remove-Item -LiteralPath $Path -ErrorAction Stop
    }
    foreach ($Variant in $Aux) {
        if ((Get-AuxiliaryStatus $Variant) -cne 'MATCH_TEMPLATE') { throw 'Auxiliar cambió; preservar.' }
        Remove-Item -LiteralPath (Join-Path $Root "$Variant/.kilo/.gitignore") -ErrorAction Stop
    }
    foreach ($Dir in @(Get-Dirs $Record.Files | Sort-Object { ($_ -split '/').Count } -Descending)) {
        $Path = Join-Path $Root $Dir
        Assert-Directory $Path
        if (@(Get-ChildItem -LiteralPath $Path -Force).Count -ne 0) { throw 'Directorio no vacío; preservar.' }
        [IO.Directory]::Delete($Path,$false)
    }
    Assert-Directory $Root
    if (@(Get-ChildItem -LiteralPath $Root -Force).Count -ne 1) { throw 'Raíz contiene entradas inesperadas; preservar registro.' }
    Assert-File $StateFile
    Remove-Item -LiteralPath $StateFile -ErrorAction Stop
    [IO.Directory]::Delete($Root,$false)
    Assert-Absent $env:LOCALAPPDATA 'KiloTeam-F06-Lab'
    Write-Host 'F06_RETIRADO'
    exit 0
} catch {
    Write-Error -Message $_.Exception.Message -ErrorAction Continue
    Write-Host 'F06_BLOCKED: conservar registro y archivos; no limpiar manualmente ni repetir preparación.'
    exit 1
}
