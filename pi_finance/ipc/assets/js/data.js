import { fetchJsonFromSources, getIpcUrls } from "/finance/shared/data-sources.js"

export async function loadIPC() {
  const { data: json } = await fetchJsonFromSources(getIpcUrls(), { cache: "no-store" })
  if (!json || typeof json !== "object") throw new Error("bad_json")

  if (!json.monthly || typeof json.monthly !== "object") {
    throw new Error("missing_monthly")
  }

  const cleanMonthly = {}
  const ymRegex = /^\d{4}-\d{2}$/

  for (const [ym, val] of Object.entries(json.monthly)) {
    if (!ymRegex.test(ym)) continue
    const num = Number(val)
    if (!Number.isFinite(num)) continue
    cleanMonthly[ym] = num
  }

  const months = Object.keys(cleanMonthly).sort()
  if (!months.length) {
    throw new Error("empty_monthly")
  }

  return {
    source: json.source || "INDEC",
    series: json.series || "IPC Nacional",
    monthly: cleanMonthly,
    lastUpdate: json.lastUpdate || months[months.length - 1]
  }
}
