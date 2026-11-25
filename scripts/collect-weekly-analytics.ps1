$ErrorActionPreference = "Stop"

$projectRoot = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
$pythonPath = Join-Path $projectRoot ".venv\Scripts\python.exe"
$credentialPath = Join-Path $projectRoot "credentials\analytics-reader.json"
$runDate = Get-Date -Format "yyyy-MM-dd"
$weeklyRoot = Join-Path $projectRoot "analytics\weekly"
$runRoot = Join-Path $weeklyRoot $runDate
$sevenDayOutput = Join-Path $runRoot "7d"
$twentyEightDayOutput = Join-Path $runRoot "28d"
$sevenDayGa4Output = Join-Path $sevenDayOutput "ga4"
$twentyEightDayGa4Output = Join-Path $twentyEightDayOutput "ga4"
$sevenDaySearchOutput = Join-Path $sevenDayOutput "search-console"
$twentyEightDaySearchOutput = Join-Path $twentyEightDayOutput "search-console"

if (-not (Test-Path -LiteralPath $pythonPath)) {
    throw "No se encontro .venv\Scripts\python.exe."
}
if (-not (Test-Path -LiteralPath $credentialPath)) {
    throw "No se encontro la credencial de solo lectura en credentials\analytics-reader.json."
}

New-Item -ItemType Directory -Path $runRoot -Force | Out-Null
$env:GOOGLE_APPLICATION_CREDENTIALS = $credentialPath
$env:GA4_PROPERTY_ID = "342133855"
$env:SEARCH_CONSOLE_SITE_URL = "https://pidevelopment.web.app/"

Push-Location $projectRoot
try {
    & $pythonPath manage.py import_analytics --days 7 --output-dir $sevenDayGa4Output --skip-search-console
    if ($LASTEXITCODE -ne 0) { throw "Fallo la importacion de GA4 de 7 dias." }

    & $pythonPath manage.py import_analytics --days 28 --output-dir $twentyEightDayGa4Output --skip-search-console
    if ($LASTEXITCODE -ne 0) { throw "Fallo la importacion de GA4 de 28 dias." }

    $searchConsoleStatus = "available"
    & $pythonPath manage.py import_analytics --days 7 --output-dir $sevenDaySearchOutput --skip-ga4
    if ($LASTEXITCODE -ne 0) {
        $searchConsoleStatus = "unavailable"
        Write-Warning "Search Console no esta disponible para la cuenta de servicio. El informe semanal continuara solo con GA4."
    }
    else {
        & $pythonPath manage.py import_analytics --days 28 --output-dir $twentyEightDaySearchOutput --skip-ga4
        if ($LASTEXITCODE -ne 0) {
            $searchConsoleStatus = "partial"
            Write-Warning "Search Console de 28 dias fallo. Se conservara la ventana de 7 dias."
        }
    }
}
finally {
    Pop-Location
}

$metadata = [ordered]@{
    generated_on = $runDate
    ga4_status = "available"
    search_console_status = $searchConsoleStatus
    seven_day_ga4_summary = (Join-Path $sevenDayGa4Output "summary.md")
    twenty_eight_day_ga4_summary = (Join-Path $twentyEightDayGa4Output "summary.md")
    seven_day_search_summary = if (Test-Path -LiteralPath (Join-Path $sevenDaySearchOutput "summary.md")) { Join-Path $sevenDaySearchOutput "summary.md" } else { $null }
    twenty_eight_day_search_summary = if (Test-Path -LiteralPath (Join-Path $twentyEightDaySearchOutput "summary.md")) { Join-Path $twentyEightDaySearchOutput "summary.md" } else { $null }
    seven_day_data = $sevenDayOutput
    twenty_eight_day_data = $twentyEightDayOutput
}
$metadata | ConvertTo-Json | Set-Content -LiteralPath (Join-Path $weeklyRoot "latest-data.json") -Encoding utf8

Write-Output "Weekly analytics ready: $runRoot"
