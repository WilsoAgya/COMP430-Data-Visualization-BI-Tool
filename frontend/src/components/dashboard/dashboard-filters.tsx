import { useState } from "react"
import { Button } from "@/components/ui/button"
import TickerSearch from "./ticker-search"

type DashboardFiltersProps = {
    tickers: { symbol: string; companyName: string }[]
    onSelectTicker: (ticker: { symbol: string; companyName: string }) => void
}

const ranges = ["1M", "3M", "6M", "1Y"]

export default function DashboardFilters({
                                             tickers,
                                             onSelectTicker,
                                         }: DashboardFiltersProps) {
    const [selectedRange, setSelectedRange] = useState("6M")

    return (
        <div className="bg-card flex flex-col gap-4 rounded-xl border p-4">
            <TickerSearch tickers={tickers} onSelectTicker={onSelectTicker} />

            <div className="flex flex-wrap gap-2">
                {ranges.map((range) => (
                    <Button
                        key={range}
                        type="button"
                        variant={selectedRange === range ? "default" : "outline"}
                        onClick={() => setSelectedRange(range)}
                    >
                        {range}
                    </Button>
                ))}
            </div>
        </div>
    )
}
