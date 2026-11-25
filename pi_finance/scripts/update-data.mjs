import fs from "node:fs"
import path from "node:path"
import process from "node:process"
import { fileURLToPath } from "node:url"

const PROJECT_ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..")

const BCRA_BASE = "https://api.bcra.gob.ar/estadisticas/v4.0/Monetarias"
const FIXED_TERM_URL = "https://api.bcra.gob.ar/transparencia/v1.0/PlazosFijos"
const MONOTRIBUTO_URL = "https://www.arca.gob.ar/monotributo/categorias.asp"
const TODAY = new Date().toISOString().slice(0, 10)
const FETCH_TIMEOUT_MS = 30_000
const PAGE_SIZE = 2_000

const SERIES = [
  {
    name: "ICL",
    id: 40,
    from: "2020-06-30",
    output: path.join("icl", "data", "icl.json"),
    minimumRows: 1_500,
    maximumAgeDays: 7,
    build(rows) {
      const daily = Object.fromEntries(rows.map(({ date, value }) => [date, Number(value.toFixed(6))]))
      const dates = Object.keys(daily)

      return {
        source: "BCRA",
        series: "ICL",
        idVariable: this.id,
        lastUpdate: dates.at(-1),
        daily
      }
    }
  },
  {
    name: "IPC",
    id: 27,
    from: "2023-10-01",
    output: path.join("ipc", "data", "ipc.json"),
    minimumRows: 24,
    maximumAgeDays: 120,
    build(rows) {
      const monthly = {}
      for (const { date, value } of rows) monthly[date.slice(0, 7)] = Number(value.toFixed(1))
      const months = Object.keys(monthly).sort()

      return {
        source: "INDEC",
        series: "IPC Nacional",
        idVariable: this.id,
        lastUpdate: months.at(-1),
        monthly
      }
    }
  },
  {
    name: "UVA",
    id: 31,
    from: "2016-03-31",
    output: path.join("credito-uva", "data", "uva.json"),
    minimumRows: 3_000,
    maximumAgeDays: 7,
    build(rows) {
      const daily = Object.fromEntries(rows.map(({ date, value }) => [date, Number(value.toFixed(2))]))
      const dates = Object.keys(daily)
      return { source: "BCRA", series: "UVA", idVariable: this.id, lastUpdate: dates.at(-1), daily }
    }
  }
]

const sleep = (milliseconds) => new Promise((resolve) => setTimeout(resolve, milliseconds))

async function fetchJsonWithRetry(url, attempts = 4) {
  let lastError

  for (let attempt = 1; attempt <= attempts; attempt += 1) {
    const controller = new AbortController()
    const timeout = setTimeout(() => controller.abort(), FETCH_TIMEOUT_MS)

    try {
      const response = await fetch(url, {
        headers: { Accept: "application/json", "Accept-Language": "es-AR" },
        signal: controller.signal
      })

      if (!response.ok) throw new Error(`BCRA respondió ${response.status} ${response.statusText}`)
      return await response.json()
    } catch (error) {
      lastError = error
      if (attempt < attempts) await sleep(attempt * 1_500)
    } finally {
      clearTimeout(timeout)
    }
  }

  throw lastError
}

async function fetchTextWithRetry(url, attempts = 4) {
  let lastError
  for (let attempt = 1; attempt <= attempts; attempt += 1) {
    const controller = new AbortController()
    const timeout = setTimeout(() => controller.abort(), FETCH_TIMEOUT_MS)
    try {
      const response = await fetch(url, { headers: { Accept: "text/html", "Accept-Language": "es-AR" }, signal: controller.signal })
      if (!response.ok) throw new Error(`La fuente respondió ${response.status} ${response.statusText}`)
      return await response.text()
    } catch (error) {
      lastError = error
      if (attempt < attempts) await sleep(attempt * 1_500)
    } finally {
      clearTimeout(timeout)
    }
  }
  throw lastError
}

async function fetchSeries(series) {
  const rows = []
  let offset = 0

  while (true) {
    const query = new URLSearchParams({
      Desde: series.from,
      Hasta: TODAY,
      Limit: String(PAGE_SIZE),
      Offset: String(offset)
    })
    const payload = await fetchJsonWithRetry(`${BCRA_BASE}/${series.id}?${query}`)
    const page = payload?.results?.[0]?.detalle
    const count = Number(payload?.metadata?.resultset?.count)

    if (!Array.isArray(page)) throw new Error(`${series.name}: formato inesperado en la respuesta del BCRA`)

    rows.push(...page)
    offset += page.length

    if (page.length === 0 || !Number.isFinite(count) || offset >= count) break
  }

  const cleanRows = rows
    .map((row) => ({ date: String(row?.fecha || "").slice(0, 10), value: Number(row?.valor) }))
    .filter(({ date, value }) => /^\d{4}-\d{2}-\d{2}$/.test(date) && Number.isFinite(value) && value > 0)
    .sort((a, b) => a.date.localeCompare(b.date))

  const uniqueRows = [...new Map(cleanRows.map((row) => [row.date, row])).values()]
  validateSeries(series, uniqueRows)
  return uniqueRows
}

function daysBetween(olderISO, newerISO) {
  return Math.floor((Date.parse(`${newerISO}T00:00:00Z`) - Date.parse(`${olderISO}T00:00:00Z`)) / 86_400_000)
}

function validateSeries(series, rows) {
  if (rows.length < series.minimumRows) {
    throw new Error(`${series.name}: se recibieron sólo ${rows.length} registros; no se publicará nada`)
  }

  const first = rows[0]?.date
  const latest = rows.at(-1)?.date
  const age = daysBetween(latest, TODAY)

  if (!first || !latest || age < 0 || age > series.maximumAgeDays) {
    throw new Error(`${series.name}: fecha más reciente sospechosa (${latest || "sin fecha"}); no se publicará nada`)
  }
}

function writeIfChanged(relativeFile, payload) {
  const absoluteFile = path.resolve(PROJECT_ROOT, relativeFile)
  const nextContent = `${JSON.stringify(payload, null, 2)}\n`
  const previousContent = fs.existsSync(absoluteFile) ? fs.readFileSync(absoluteFile, "utf8") : ""

  if (previousContent === nextContent) return false

  fs.mkdirSync(path.dirname(absoluteFile), { recursive: true })
  fs.writeFileSync(absoluteFile, nextContent, "utf8")
  return true
}

function normalizeText(value) {
  return String(value || "")
    .replace(/<[^>]+>/g, " ")
    .replace(/&nbsp;|&#160;/gi, " ")
    .replace(/&oacute;/gi, "ó").replace(/&iacute;/gi, "í").replace(/&aacute;/gi, "á")
    .replace(/&eacute;/gi, "é").replace(/&uacute;/gi, "ú").replace(/&ntilde;/gi, "ñ")
    .replace(/&deg;/gi, "°").replace(/&amp;/gi, "&")
    .replace(/\s+/g, " ").trim()
}

function parseArgentineNumber(value) {
  const normalized = normalizeText(value).replace(/\s*m\s*2$/i, "").replace(/[^\d,.-]/g, "").replace(/\./g, "").replace(",", ".")
  const number = Number(normalized)
  return Number.isFinite(number) ? number : null
}

async function updateFixedTerms() {
  const payload = await fetchJsonWithRetry(FIXED_TERM_URL)
  const rows = payload?.results
  if (!Array.isArray(rows) || rows.length < 100) throw new Error("Plazos fijos: respuesta incompleta del BCRA")
  const termDays = { 1: 30, 2: 60, 3: 90, 4: 180, 5: 360 }
  const offers = rows
    .filter((row) => /TRADICIONAL/i.test(String(row.nombreCompleto || row.nombreCorto || "")) && !/UVA|DOLAR|DÓLAR|EURO/i.test(String(row.nombreCompleto || "")))
    .map((row) => ({
      bank: normalizeText(row.descripcionEntidad),
      bankCode: String(row.codigoEntidad || ""),
      product: normalizeText(row.nombreCompleto || row.nombreCorto),
      channel: normalizeText(row.canalConstitucion),
      minimumAmount: Number(row.montoMinimoInvertir) || 0,
      minimumDays: termDays[Number(row.plazoMinimoInvertirDias)] || Number(row.plazoMinimoInvertirDias) || null,
      tea: Number(row.tasaEfectivaAnualMinima),
      date: String(row.fechaInformacion || "").slice(0, 10)
    }))
    .filter((row) => row.bank && row.minimumDays === 30 && Number.isFinite(row.tea) && row.tea >= 0 && row.tea <= 500)

  const byBank = new Map()
  for (const offer of offers) {
    const current = byBank.get(offer.bankCode || offer.bank)
    if (!current || offer.tea > current.tea) byBank.set(offer.bankCode || offer.bank, offer)
  }
  const banks = [...byBank.values()].sort((a, b) => b.tea - a.tea || a.bank.localeCompare(b.bank, "es"))
  if (banks.length < 20) throw new Error(`Plazos fijos: sólo se obtuvieron ${banks.length} bancos válidos`)
  const lastUpdate = banks.map((row) => row.date).filter(Boolean).sort().at(-1)
  return writeIfChanged(path.join("comparador-plazos-fijos", "data", "plazos-fijos.json"), {
    source: "BCRA - Régimen de Transparencia",
    lastUpdate,
    methodology: "Mejor TEA mínima informada por cada entidad para depósitos tradicionales con plazo mínimo de 30 días.",
    banks
  })
}

function extractCell(rowHtml, titlePattern) {
  for (const match of rowHtml.matchAll(/<(?:th|td)\b([^>]*)>([\s\S]*?)<\/(?:th|td)>/gi)) {
    const title = match[1].match(/data-title="([^"]+)"/i)?.[1] || ""
    if (titlePattern.test(normalizeText(title))) return normalizeText(match[2])
  }
  return ""
}

async function updateMonotributo() {
  const html = await fetchTextWithRetry(MONOTRIBUTO_URL)
  const effectiveDate = normalizeText(html.match(/Valores de aplicación desde el\s*([^<]+)/i)?.[1] || "")
  const categories = []
  for (const match of html.matchAll(/<tr[^>]*>[\s\S]*?data-title="Categoría"[^>]*>\s*([A-K])\s*<\/th>([\s\S]*?)<\/tr>/gi)) {
    const row = match[0]
    categories.push({
      category: match[1],
      maxAnnualRevenue: parseArgentineNumber(extractCell(row, /Ingresos brutos/i)),
      activity: extractCell(row, /^Actividad$/i),
      maxArea: parseArgentineNumber(extractCell(row, /Superficie afectada/i)),
      maxEnergy: parseArgentineNumber(extractCell(row, /Energía eléctrica/i)),
      maxAnnualRent: parseArgentineNumber(extractCell(row, /Alquileres devengados/i)),
      maxUnitPrice: parseArgentineNumber(extractCell(row, /Precio (?:máximo unitario|unitario máximo)/i)),
      integratedTaxServices: parseArgentineNumber(extractCell(row, /Impuesto integrado.*Locaciones/i)),
      integratedTaxGoods: parseArgentineNumber(extractCell(row, /Impuesto integrado.*Venta de cosas/i)),
      sipa: parseArgentineNumber(extractCell(row, /Aportes al SIPA/i)),
      health: parseArgentineNumber(extractCell(row, /Aportes obra social/i)),
      totalServices: parseArgentineNumber(extractCell(row, /Total.*Locaciones/i)),
      totalGoods: parseArgentineNumber(extractCell(row, /Total.*Venta de cosas/i))
    })
  }
  if (categories.length !== 11 || categories.some((row) => !row.maxAnnualRevenue || !row.totalServices || !row.totalGoods)) {
    throw new Error(`Monotributo: no se pudo validar la tabla oficial (${categories.length} categorías)`)
  }
  return writeIfChanged(path.join("monotributo", "data", "categorias.json"), {
    source: "ARCA",
    sourceUrl: MONOTRIBUTO_URL,
    effectiveDate,
    fetchedAt: TODAY,
    categories
  })
}

async function main() {
  let changedFiles = 0

  for (const series of SERIES) {
    const rows = await fetchSeries(series)
    const payload = series.build(rows)
    const changed = writeIfChanged(series.output, payload)
    changedFiles += Number(changed)
    console.log(`${series.name}: ${rows.length} registros, última fecha ${rows.at(-1).date}, ${changed ? "actualizado" : "sin cambios"}`)
  }

  const fixedTermsChanged = await updateFixedTerms()
  changedFiles += Number(fixedTermsChanged)
  console.log(`Plazos fijos: ${fixedTermsChanged ? "actualizados" : "sin cambios"}`)

  const monotributoChanged = await updateMonotributo()
  changedFiles += Number(monotributoChanged)
  console.log(`Monotributo: ${monotributoChanged ? "actualizado" : "sin cambios"}`)

  console.log(changedFiles ? `Listo: ${changedFiles} archivo(s) actualizado(s).` : "Listo: los datos ya estaban al día.")
}

main().catch((error) => {
  console.error(error?.message || error)
  process.exit(1)
})
