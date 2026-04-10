export type TickerOption = {
  symbol: string
  companyName: string
}

export async function searchTickers(query: string, limit = 8): Promise<TickerOption[]> {
  const url = new URL("/api/tickers", window.location.origin)
  url.searchParams.set("q", query)
  url.searchParams.set("limit", String(limit))

  const response = await fetch(url.toString())

  if (!response.ok) {
    throw new Error("Failed to search tickers")
  }

  return (await response.json()) as TickerOption[]
}
