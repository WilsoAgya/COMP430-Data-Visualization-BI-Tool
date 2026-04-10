import TickerSearch from "./ticker-search"
import type { TickerOption } from "@/lib/ticker-api"

type DashboardFiltersProps = {
  onSelectTicker: (ticker: TickerOption) => void
}

export default function DashboardFilters({ onSelectTicker }: DashboardFiltersProps) {
  return (
    <div className="bg-card rounded-xl border p-4">
      <TickerSearch onSelectTicker={onSelectTicker} />
    </div>
  )
}
