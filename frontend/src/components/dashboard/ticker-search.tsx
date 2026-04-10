import { useEffect, useState } from "react"

import { Input } from "@/components/ui/input"
import { searchTickers, type TickerOption } from "@/lib/ticker-api"

interface TickerSearchProps {
  onSelectTicker: (ticker: TickerOption) => void
}

export default function TickerSearch({ onSelectTicker }: TickerSearchProps) {
  const [query, setQuery] = useState("")
  const [results, setResults] = useState<TickerOption[]>([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [isOpen, setIsOpen] = useState(false)

  useEffect(() => {
    if (!isOpen) {
      return
    }

    let cancelled = false
    const timeoutId = window.setTimeout(async () => {
      setLoading(true)
      setError(null)

      try {
        const data = await searchTickers(query)
        if (!cancelled) {
          setResults(data)
        }
      } catch (err) {
        if (!cancelled) {
          setResults([])
          setError(err instanceof Error ? err.message : "Failed to search tickers")
        }
      } finally {
        if (!cancelled) {
          setLoading(false)
        }
      }
    }, 200)

    return () => {
      cancelled = true
      window.clearTimeout(timeoutId)
    }
  }, [isOpen, query])

  return (
    <div className="relative w-full max-w-md">
      <Input
        value={query}
        placeholder="Search ticker or company"
        onFocus={() => setIsOpen(true)}
        onBlur={() => {
          window.setTimeout(() => setIsOpen(false), 100)
        }}
        onChange={(event) => setQuery(event.target.value)}
      />

      {isOpen ? (
        <div className="bg-card absolute top-full right-0 left-0 z-50 mt-2 rounded-md border shadow-lg">
          {loading ? <p className="text-muted-foreground px-3 py-2 text-sm">Searching...</p> : null}
          {!loading && error ? <p className="text-destructive px-3 py-2 text-sm">{error}</p> : null}
          {!loading && !error && !results.length ? (
            <p className="text-muted-foreground px-3 py-2 text-sm">No matching tickers.</p>
          ) : null}
          {!loading && !error
            ? results.map((ticker) => (
                <button
                  key={ticker.symbol}
                  type="button"
                  className="hover:bg-accent block w-full px-3 py-2 text-left"
                  onMouseDown={(event) => event.preventDefault()}
                  onClick={() => {
                    setQuery(`${ticker.symbol} - ${ticker.companyName}`)
                    setIsOpen(false)
                    onSelectTicker(ticker)
                  }}
                >
                  {ticker.symbol} - {ticker.companyName}
                </button>
              ))
            : null}
        </div>
      ) : null}
    </div>
  )
}
