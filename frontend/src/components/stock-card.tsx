import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "./ui/card"
import StockInfoItem from "./ui/stock-info-item"

interface StockCardProps {
  stockName: string
  stockSymbol: string
  ask: number | null
  lastSale: number | null
  open: number | null
  close: number | null
  high: number | null
  low: number | null
  exchange: string | null
  marketCap: number | null
  peRatio: number | null
  week52High: number | null
  week52Low: number | null
  volume: number | null
  avgVolume: number | null
  marginReq: number | null
}

function formatCurrency(value: number | null) {
  return value === null ? "N/A" : `$${value.toFixed(2)}`
}

function formatCompact(value: number | null, divisor: number, suffix: string) {
  return value === null ? "N/A" : `${(value / divisor).toFixed(2)}${suffix}`
}

function formatPercent(value: number | null) {
  return value === null ? "N/A" : `${value.toFixed(2)}%`
}

function formatPlain(value: number | null) {
  return value === null ? "N/A" : value.toFixed(2)
}

export default function StockCard(props: StockCardProps) {
  return (
    <Card>
      <CardHeader>
        <CardTitle>{props.stockName}</CardTitle>
        <CardDescription>{props.stockSymbol}</CardDescription>
      </CardHeader>
      <CardContent>
        <div className="stock-card flex grid grid-cols-4 gap-4">
          <StockInfoItem label="Ask" value={formatCurrency(props.ask)} />
          <StockInfoItem label="Last Sale" value={formatCurrency(props.lastSale)} />
          <StockInfoItem label="Open" value={formatCurrency(props.open)} />
          <StockInfoItem label="Close" value={formatCurrency(props.close)} />
          <StockInfoItem label="High" value={formatCurrency(props.high)} />
          <StockInfoItem label="Low" value={formatCurrency(props.low)} />
          <StockInfoItem label="Exchange" value={props.exchange ?? "N/A"} />
          <StockInfoItem label="Market Cap" value={formatCompact(props.marketCap, 1e9, "B")} />
          <StockInfoItem label="P/E Ratio" value={formatPlain(props.peRatio)} />
          <StockInfoItem label="52W High" value={formatCurrency(props.week52High)} />
          <StockInfoItem label="52W Low" value={formatCurrency(props.week52Low)} />
          <StockInfoItem label="Volume" value={formatCompact(props.volume, 1e3, "K")} />
          <StockInfoItem label="Avg Volume" value={formatCompact(props.avgVolume, 1e6, "M")} />
          <StockInfoItem label="Margin req." value={formatPercent(props.marginReq)} />
        </div>
      </CardContent>
    </Card>
  )
}
