import { fetchJsonFromSources, getIclUrls } from "/finance/shared/data-sources.js"

let ICL_CACHE = null

export async function loadICL() {
  if (ICL_CACHE) return ICL_CACHE

  const { data } = await fetchJsonFromSources(getIclUrls(), { cache: "no-store" })
  if (!data?.daily || typeof data.daily !== "object") throw new Error("icl.json inválido: falta daily")

  const dates = Object.keys(data.daily).sort()
  if (!dates.length) throw new Error("icl.json inválido: daily vacío")

  const min = dates[0]
  const max = dates[dates.length - 1]

  ICL_CACHE = { meta: data, dates, map: data.daily, min, max }
  return ICL_CACHE
}

export function resolveDateAvailable(icl, isoDate) {
  const { dates, min, max } = icl

  if (isoDate <= min) return min
  if (isoDate >= max) return max

  let lo = 0
  let hi = dates.length - 1
  while (lo <= hi) {
    const mid = (lo + hi) >> 1
    const d = dates[mid]
    if (d === isoDate) return d
    if (d < isoDate) lo = mid + 1
    else hi = mid - 1
  }

  return dates[hi]
}

export function resolveAvailableInfo(icl, isoDate) {
  const used = resolveDateAvailable(icl, isoDate)
  return { input: isoDate, used, adjusted: used !== isoDate }
}

export function calcICL(amount, iclFrom, iclTo) {
  const ratio = iclTo / iclFrom
  const updated = amount * ratio
  const accumulated = ratio - 1
  return { ratio, updated, accumulated }
}
