[CmdletBinding()]
param(
    [ValidateRange(1024, 65535)]
    [int]$Port = 8000,
    [switch]$SkipBuild,
    [switch]$NoBrowser,
    [switch]$Stop
)

$ErrorActionPreference = "Stop"

$projectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$distPath = Join-Path $projectRoot "dist"
$buildScript = Join-Path $projectRoot "build-static.ps1"
$statePath = Join-Path $projectRoot ".local-server.pid"
$stdoutPath = Join-Path $projectRoot "local-static-server.log"
$stderrPath = Join-Path $projectRoot "local-static-server-error.log"
$venvPython = Join-Path $projectRoot ".venv\Scripts\python.exe"

function Read-ServerState {
    if (-not (Test-Path -LiteralPath $statePath)) { return $null }
    try {
        return Get-Content -LiteralPath $statePath -Raw | ConvertFrom-Json
    }
    catch {
        return $null
    }
}

function Get-ManagedProcess {
    param($State)

    if (-not $State -or -not $State.pid -or -not $State.startedAtUtc -or -not $State.pythonPath) {
        return $null
    }

    $process = Get-Process -Id ([int]$State.pid) -ErrorAction SilentlyContinue
    if (-not $process) { return $null }

    if (-not $process.Path) { return $null }
    $expectedPath = [System.IO.Path]::GetFullPath([string]$State.pythonPath)
    $actualPath = [System.IO.Path]::GetFullPath([string]$process.Path)
    $expectedStart = if ($State.startedAtUtc -is [DateTime]) {
        $State.startedAtUtc.ToUniversalTime()
    }
    else {
        [DateTime]::Parse(
            [string]$State.startedAtUtc,
            [System.Globalization.CultureInfo]::InvariantCulture,
            [System.Globalization.DateTimeStyles]::RoundtripKind
        ).ToUniversalTime()
    }
    $startDifference = [Math]::Abs(($process.StartTime.ToUniversalTime() - $expectedStart).TotalSeconds)

    if ($actualPath -ne $expectedPath -or $startDifference -gt 5) { return $null }
    return $process
}

function Test-LocalPage {
    param([string]$Url)

    try {
        $response = Invoke-WebRequest -Uri $Url -UseBasicParsing -TimeoutSec 2
        return $response.StatusCode -eq 200 -and $response.Content -match "Pi Development"
    }
    catch {
        return $false
    }
}

function Test-PortInUse {
    param([int]$CandidatePort)

    $client = [System.Net.Sockets.TcpClient]::new()
    try {
        $pending = $client.ConnectAsync("127.0.0.1", $CandidatePort)
        return $pending.Wait(250) -and $client.Connected
    }
    catch {
        return $false
    }
    finally {
        $client.Dispose()
    }
}

function Remove-StaleState {
    if (Test-Path -LiteralPath $statePath) {
        Remove-Item -LiteralPath $statePath -Force
    }
}

Set-Location -LiteralPath $projectRoot

$state = Read-ServerState
$managedProcess = Get-ManagedProcess -State $state

if ($Stop) {
    if ($managedProcess) {
        Stop-Process -Id $managedProcess.Id -Force
        Write-Host "Servidor local detenido (PID $($managedProcess.Id))." -ForegroundColor Green
    }
    elseif ($state) {
        Write-Host "El servidor registrado ya no esta activo." -ForegroundColor Yellow
    }
    else {
        Write-Host "No hay un servidor local administrado por este proyecto." -ForegroundColor Yellow
    }
    Remove-StaleState
    exit 0
}

if (-not $SkipBuild -and $managedProcess) {
    Stop-Process -Id $managedProcess.Id -Force
    $managedProcess.WaitForExit()
    Remove-StaleState
    $managedProcess = $null
    $state = $null
}

if (-not $SkipBuild) {
    if (-not (Test-Path -LiteralPath $buildScript)) {
        throw "No se encontro build-static.ps1."
    }
    Write-Host "Generando y validando dist..." -ForegroundColor Cyan
    & $buildScript
    if ($LASTEXITCODE -ne 0) { throw "La generacion estatica fallo." }
}

if (-not (Test-Path -LiteralPath (Join-Path $distPath "index.html"))) {
    throw "dist/index.html no existe. Ejecuta sin -SkipBuild para generarlo."
}

if ($managedProcess -and (Test-LocalPage -Url ([string]$state.url))) {
    $url = [string]$state.url
    Write-Host "Reutilizando el servidor local: $url" -ForegroundColor Green
    if (-not $NoBrowser) { Start-Process $url }
    exit 0
}

if ($managedProcess) {
    Stop-Process -Id $managedProcess.Id -Force
}
Remove-StaleState

if (-not (Test-Path -LiteralPath $venvPython)) {
    throw "No se encontro .venv\Scripts\python.exe. Instala requirements.txt primero."
}

$pythonPath = (& $venvPython -c "import sys; print(sys._base_executable)").Trim()
if (-not $pythonPath -or -not (Test-Path -LiteralPath $pythonPath)) {
    throw "No se pudo resolver el ejecutable base de Python."
}

$selectedPort = $Port
while (Test-PortInUse -CandidatePort $selectedPort) {
    $selectedPort += 1
    if ($selectedPort -gt [Math]::Min($Port + 99, 65535)) {
        throw "No se encontro un puerto libre entre $Port y $selectedPort."
    }
}

if ($selectedPort -ne $Port) {
    Write-Host "El puerto $Port esta ocupado; se usara $selectedPort." -ForegroundColor Yellow
}

$argumentString = "-m http.server $selectedPort --bind 127.0.0.1 --directory dist"
$server = Start-Process -FilePath $pythonPath `
    -ArgumentList $argumentString `
    -WorkingDirectory $projectRoot `
    -WindowStyle Hidden `
    -RedirectStandardOutput $stdoutPath `
    -RedirectStandardError $stderrPath `
    -PassThru

$url = "http://127.0.0.1:$selectedPort/"
$ready = $false
for ($attempt = 0; $attempt -lt 40; $attempt += 1) {
    if ($server.HasExited) { break }
    if (Test-LocalPage -Url $url) {
        $ready = $true
        break
    }
    Start-Sleep -Milliseconds 250
}

if (-not $ready) {
    $errorOutput = if (Test-Path -LiteralPath $stderrPath) {
        Get-Content -LiteralPath $stderrPath -Raw -ErrorAction SilentlyContinue
    } else { $null }
    $details = if ([string]::IsNullOrWhiteSpace($errorOutput)) { "Sin detalle adicional." } else { $errorOutput.Trim() }
    if (-not $server.HasExited) { Stop-Process -Id $server.Id -Force }
    throw "El servidor local no respondio en $url. $details"
}

@{
    pid = $server.Id
    port = $selectedPort
    url = $url
    pythonPath = $server.Path
    startedAtUtc = $server.StartTime.ToUniversalTime().ToString("o")
} | ConvertTo-Json | Set-Content -LiteralPath $statePath -Encoding UTF8

Write-Host "Proyecto listo: $url" -ForegroundColor Green
Write-Host "Para detenerlo: .\open-local.ps1 -Stop" -ForegroundColor DarkGray

if (-not $NoBrowser) {
    Start-Process $url
}
