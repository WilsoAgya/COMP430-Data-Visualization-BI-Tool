import { useMemo, useState } from "react"

import { Input } from "@/components/ui/input"

interface Ticker {
    symbol: string
    companyName: string
}

interface TickerSearchProps {
    tickers: Ticker[]
    onSelectTicker: (ticker: Ticker) => void
}

export default function TickerSearch({ tickers, onSelectTicker }: TickerSearchProps) {
    const [query, setQuery] = useState("")

    const filteredTickers = useMemo(() => {
        const value = query.toLowerCase()

        return tickers.filter((ticker) => {
            return (
                ticker.symbol.toLowerCase().includes(value) ||
                ticker.companyName.toLowerCase().includes(value)
            )
        })
    }, [query, tickers])

    return (
        <div className="relative w-full max-w-md">
            <Input
                value={query}
                placeholder="Search ticker or company"
                onChange={(event) => setQuery(event.target.value)}
            />

            {query.length > 0 ? (
                <div className="bg-card absolute top-full left-0 right-0 z-50 mt-2 rounded-md border shadow-lg">
                    {filteredTickers.slice(0, 5).map((ticker) => (
                        <button
                            key={ticker.symbol}
                            type="button"
                            className="hover:bg-accent block w-full px-3 py-2 text-left"
                            onClick={() => {
                                setQuery(ticker.symbol)
                                onSelectTicker(ticker)
                            }}
                        >
                            {ticker.symbol} - {ticker.companyName}
                        </button>
                    ))}
                </div>
            ) : null}
        </div>
    )

}
