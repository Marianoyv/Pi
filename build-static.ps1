$ErrorActionPreference = "Stop"

$projectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$pythonPath = Join-Path $projectRoot ".venv\Scripts\python.exe"

if (-not (Test-Path -LiteralPath $pythonPath)) {
    throw "No se encontro el entorno local en .venv. Instala requirements.txt antes de generar el sitio."
}

Push-Location $projectRoot
try {
    & $pythonPath manage.py check --settings=pi_development.settings.static_export
    if ($LASTEXITCODE -ne 0) { throw "La configuracion del sitio no es valida." }
    if (-not (Get-Command node -ErrorAction SilentlyContinue)) { throw "Node.js es necesario para verificar los scripts antes de publicar." }
    foreach ($script in Get-ChildItem -LiteralPath (Join-Path $projectRoot "static/web/js") -Filter "*.js" -File) {
        node --check $script.FullName
        if ($LASTEXITCODE -ne 0) { throw "JavaScript invalido: $($script.Name)" }
    }
    foreach ($script in Get-ChildItem -LiteralPath (Join-Path $projectRoot "pi_finance") -Filter "*.js" -File -Recurse) {
        node --check $script.FullName
        if ($LASTEXITCODE -ne 0) { throw "JavaScript invalido en Pi Finance: $($script.FullName)" }
    }
    node pi_finance/scripts/test-calculators.mjs
    if ($LASTEXITCODE -ne 0) { throw "Las pruebas de Pi Finance fallaron." }
    node --test tests/*.test.cjs
    if ($LASTEXITCODE -ne 0) { throw "Las pruebas de JavaScript fallaron." }
    & $pythonPath manage.py test pi_development.web.test_static_export --settings=pi_development.settings.static_export
    if ($LASTEXITCODE -ne 0) { throw "Las pruebas del sitio fallaron." }
    & $pythonPath manage.py validate_editorial --settings=pi_development.settings.static_export
    if ($LASTEXITCODE -ne 0) {
        throw "La validacion editorial fallo. El sitio no se genero."
    }
    & $pythonPath manage.py build_editorial_index --settings=pi_development.settings.static_export
    if ($LASTEXITCODE -ne 0) {
        throw "No se pudo actualizar la memoria editorial."
    }
    & $pythonPath manage.py export_static --settings=pi_development.settings.static_export
    if ($LASTEXITCODE -ne 0) {
        throw "La generacion estatica fallo."
    }
    & $pythonPath scripts/check_static_release.py
    if ($LASTEXITCODE -ne 0) { throw "La verificacion final del sitio generado fallo." }
}
finally {
    Pop-Location
}
