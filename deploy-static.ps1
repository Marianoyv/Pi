$ErrorActionPreference = "Stop"

$projectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$buildScript = Join-Path $projectRoot "build-static.ps1"

Push-Location $projectRoot
try {
    & $buildScript
    if ($LASTEXITCODE -ne 0) {
        throw "La generacion estatica fallo; no se inicio el deploy."
    }
    if (-not (Get-Command firebase -ErrorAction SilentlyContinue)) {
        throw "No se encontro Firebase CLI. Instala o habilita la herramienta antes de publicar."
    }
    firebase deploy --only hosting --project pidevelopment
    if ($LASTEXITCODE -ne 0) {
        throw "Firebase Hosting no pudo completar el deploy."
    }
}
finally {
    Pop-Location
}
