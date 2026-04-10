export type StockHistory = {
  symbol: string
  high: number
  low: number
  close: number
  date: string
}

export type StockRange = "1M" | "3M" | "6M" | "1Y"

export async function fetchStockHistory(
  symbol: string,
  range: StockRange
): Promise<StockHistory[]> {
  const url = new URL(`/api/stocks/${encodeURIComponent(symbol)}`, window.location.origin)
  url.searchParams.set("range", range)

  const response = await fetch(url.toString())

  if (!response.ok) {
    throw new Error(`Failed to load stock data for ${symbol}`)
  }

  const payload = (await response.json()) as StockHistory[]

  return payload
}
