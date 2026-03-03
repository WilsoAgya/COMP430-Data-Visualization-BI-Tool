import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "./ui/card"
import StockInfoItem from "./ui/stock-info-item"

interface StockCardProps {
  stockName: string
  stockSymbol: string
  ask: number
  lastSale: number
  open: number
  close: number
  high: number
  low: number
  exchange: string
  marketCap: number
  peRatio: number
  week52High: number
  week52Low: number
  volume: number
  avgVolume: number
  marginReq: number
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
          <StockInfoItem label="Ask" value={`$${props.ask.toFixed(2)}`} />
          <StockInfoItem label="Last Sale" value={`$${props.lastSale.toFixed(2)}`} />
          <StockInfoItem label="Open" value={`$${props.open.toFixed(2)}`} />
          <StockInfoItem label="Close" value={`$${props.close.toFixed(2)}`} />
          <StockInfoItem label="High" value={`$${props.high.toFixed(2)}`} />
          <StockInfoItem label="Low" value={`$${props.low.toFixed(2)}`} />
          <StockInfoItem label="Exchange" value={props.exchange} />
          <StockInfoItem label="Market Cap" value={`$${(props.marketCap / 1e9).toFixed(2)}B`} />
          <StockInfoItem label="P/E Ratio" value={props.peRatio.toFixed(2)} />
          <StockInfoItem label="52W High" value={`$${props.week52High.toFixed(2)}`} />
          <StockInfoItem label="52W Low" value={`$${props.week52Low.toFixed(2)}`} />
          <StockInfoItem label="Volume" value={`${(props.volume / 1e3).toFixed(2)}K`} />
          <StockInfoItem label="Avg Volume" value={`${(props.avgVolume / 1e6).toFixed(2)}M`} />
          <StockInfoItem label="Margin req." value={`${props.marginReq.toFixed(2)}%`} />
        </div>
      </CardContent>
    </Card>
  )
}
