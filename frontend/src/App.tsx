import { useEffect, useState } from "react"
import { Navigate, Route, Routes, useNavigate, useParams } from "react-router-dom"
import { Area, AreaChart, CartesianGrid, XAxis, YAxis } from "recharts"

import DashboardFilters from "@/components/dashboard/dashboard-filters"
import NewsTab from "@/components/dashboard/news-tab"
import Footer from "@/components/layout/footer"
import StockCard from "@/components/stock-card"
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import {
  ChartContainer,
  ChartLegend,
  ChartLegendContent,
  ChartTooltip,
  ChartTooltipContent,
} from "@/components/ui/chart"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { fetchStockHistory, type StockRange, type StockHistory } from "@/lib/stock-api"
import { searchTickers, type TickerOption } from "@/lib/ticker-api"

import type { ChartConfig } from "@/components/ui/chart"

const chartConfig = {
  high: { label: "High Price", color: "var(--chart-1)" },
  low: { label: "Low Price", color: "var(--chart-2)" },
} satisfies ChartConfig

const defaultTicker = { symbol: "AAPL", companyName: "Apple Inc." }
const chartRanges: StockRange[] = ["1M", "3M", "6M", "1Y"]

function formatChartLabel(date: string) {
  return new Intl.DateTimeFormat("en-US", {
    month: "short",
    day: "numeric",
  }).format(new Date(date))
}

function formatTooltipDate(date: string) {
  return new Intl.DateTimeFormat("en-US", {
    month: "short",
    day: "numeric",
    year: "numeric",
  }).format(new Date(date))
}

function getChartDomain(history: StockHistory[]) {
  if (!history.length) {
    return [0, 100] as const
  }

  const lows = history.map((point) => point.low)
  const highs = history.map((point) => point.high)
  const min = Math.min(...lows)
  const max = Math.max(...highs)
  const range = max - min
  const padding = range === 0 ? Math.max(min * 0.05, 1) : range * 0.1

  return [Math.max(0, min - padding), max + padding] as const
}

function buildStockCardData(
  ticker: { symbol: string; companyName: string },
  history: StockHistory[]
) {
  const firstPoint = history[0] ?? null
  const latestPoint = history.at(-1) ?? null
  const allHighs = history.map((point) => point.high)
  const allLows = history.map((point) => point.low)

  return {
    stockName: ticker.companyName,
    stockSymbol: ticker.symbol,
    ask: latestPoint?.close ?? null,
    lastSale: latestPoint?.close ?? null,
    open: firstPoint?.close ?? null,
    close: latestPoint?.close ?? null,
    high: latestPoint?.high ?? null,
    low: latestPoint?.low ?? null,
    exchange: "NASDAQ/NYSE",
    marketCap: null,
    peRatio: null,
    week52High: allHighs.length ? Math.max(...allHighs) : null,
    week52Low: allLows.length ? Math.min(...allLows) : null,
    volume: null,
    avgVolume: null,
    marginReq: null,
  }
}

function DashboardPage() {
  const navigate = useNavigate()
  const { symbol: rawSymbol } = useParams()
  const symbol = (rawSymbol ?? defaultTicker.symbol).toUpperCase()

  const [stockhistory, setStockhistory] = useState<StockHistory[]>([])
  const [selectedTicker, setSelectedTicker] = useState<TickerOption>({
    symbol,
    companyName: symbol,
  })
  const [selectedRange, setSelectedRange] = useState<StockRange>("6M")
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    setSelectedTicker((current) =>
      current.symbol === symbol ? current : { symbol, companyName: symbol }
    )

    let cancelled = false

    async function loadTickerMetadata() {
      try {
        const tickerMatches = await searchTickers(symbol, 5)
        if (!cancelled) {
          const exactTicker = tickerMatches.find((ticker) => ticker.symbol === symbol)
          if (exactTicker) {
            setSelectedTicker(exactTicker)
          }
        }
      } catch {
        // Ticker metadata is non-blocking for the dashboard route.
      }
    }

    loadTickerMetadata()

    return () => {
      cancelled = true
    }
  }, [symbol])

  useEffect(() => {
    let cancelled = false

    async function loadStockhistory() {
      setLoading(true)
      setError(null)

      try {
        const data = await fetchStockHistory(symbol, selectedRange)
        if (!cancelled) {
          setStockhistory(data)
        }
      } catch (err) {
        if (!cancelled) {
          setStockhistory([])
          setError(err instanceof Error ? err.message : "Failed to load stock data")
        }
      } finally {
        if (!cancelled) {
          setLoading(false)
        }
      }
    }

    loadStockhistory()

    return () => {
      cancelled = true
    }
  }, [selectedRange, symbol])

  const chartData = stockhistory.map((point) => ({
    date: formatChartLabel(point.date),
    fullDate: formatTooltipDate(point.date),
    high: point.high,
    low: point.low,
  }))

  const stockCardData = buildStockCardData(selectedTicker, stockhistory)
  const [chartMin, chartMax] = getChartDomain(stockhistory)

  return (
    <main className="bg-background text-foreground min-h-screen px-4 py-10">
      <div className="mx-auto flex h-full w-full max-w-5xl flex-col gap-6">
        <header className="space-y-2">
          <h1 className="text-3xl font-semibold tracking-tight">BI Tool & Data Warehouse</h1>
          <p className="text-muted-foreground text-sm">A data visualization tool for COMP430</p>
        </header>

        <DashboardFilters onSelectTicker={(ticker) => navigate(`/ticker/${ticker.symbol}`)} />

        <Tabs defaultValue="stock-info" className="w-full">
          <TabsList>
            <TabsTrigger value="stock-info">Stock Data</TabsTrigger>
            <TabsTrigger value="charts">Chart</TabsTrigger>
            <TabsTrigger value="news">News</TabsTrigger>
          </TabsList>

          <TabsContent value="stock-info">
            {loading ? (
              <Card>
                <CardHeader>
                  <CardTitle>Loading {selectedTicker.symbol}</CardTitle>
                  <CardDescription>Fetching stock data from the backend.</CardDescription>
                </CardHeader>
              </Card>
            ) : error ? (
              <Alert variant="destructive">
                <AlertTitle>Could not load stock data</AlertTitle>
                <AlertDescription>{error}</AlertDescription>
              </Alert>
            ) : !stockhistory.length ? (
              <Alert>
                <AlertTitle>No stock data found</AlertTitle>
                <AlertDescription>
                  No rows were returned for {selectedTicker.symbol}.
                </AlertDescription>
              </Alert>
            ) : (
              <StockCard {...stockCardData} />
            )}
          </TabsContent>

          <TabsContent value="charts">
            <Card>
              <CardHeader>
                <div className="flex flex-col gap-4 md:flex-row md:items-start md:justify-between">
                  <div>
                    <CardTitle>{selectedTicker.symbol} price history</CardTitle>
                    <CardDescription>High and low values returned by the backend.</CardDescription>
                  </div>
                  <div className="flex flex-wrap gap-2">
                    {chartRanges.map((range) => (
                      <Button
                        key={range}
                        type="button"
                        size="sm"
                        variant={selectedRange === range ? "default" : "outline"}
                        onClick={() => setSelectedRange(range)}
                      >
                        {range}
                      </Button>
                    ))}
                  </div>
                </div>
              </CardHeader>
              <CardContent>
                {loading ? (
                  <p className="text-muted-foreground text-sm">Loading chart data...</p>
                ) : error ? (
                  <p className="text-destructive text-sm">{error}</p>
                ) : !chartData.length ? (
                  <p className="text-muted-foreground text-sm">No chart data available.</p>
                ) : (
                  <ChartContainer config={chartConfig} className="min-h-[280px] w-full">
                    <AreaChart data={chartData} margin={{ left: 12, right: 12 }}>
                      <CartesianGrid vertical={false} />
                      <YAxis
                        domain={[chartMin, chartMax]}
                        tickLine={false}
                        axisLine={false}
                        tickMargin={12}
                        width={72}
                        tickFormatter={(value: number) => `$${value.toFixed(2)}`}
                      />
                      <XAxis
                        dataKey="date"
                        tickLine={false}
                        axisLine={false}
                        tickMargin={8}
                        minTickGap={24}
                      />
                      <ChartTooltip
                        content={
                          <ChartTooltipContent
                            indicator="line"
                            labelFormatter={(_, payload) => payload?.[0]?.payload.fullDate ?? ""}
                          />
                        }
                      />
                      <ChartLegend content={<ChartLegendContent />} />
                      <Area
                        dataKey="high"
                        type="monotone"
                        fill="var(--color-high)"
                        fillOpacity={0.25}
                        stroke="var(--color-high)"
                        strokeWidth={2}
                      />
                      <Area
                        dataKey="low"
                        type="monotone"
                        fill="var(--color-low)"
                        fillOpacity={0.35}
                        stroke="var(--color-low)"
                        strokeWidth={2}
                      />
                    </AreaChart>
                  </ChartContainer>
                )}
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="news">
            <p className="text-muted-foreground mb-3 text-sm">
              Showing news for {selectedTicker.symbol} - {selectedTicker.companyName}
            </p>
            <NewsTab symbol={selectedTicker.symbol} companyName={selectedTicker.companyName} />
          </TabsContent>
        </Tabs>
      </div>
      <footer className="mx-auto mt-10 w-full max-w-5xl border-t py-6">
        <Footer />
      </footer>
    </main>
  )
}

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<Navigate to={`/ticker/${defaultTicker.symbol}`} replace />} />
      <Route path="/ticker/:symbol" element={<DashboardPage />} />
      <Route path="*" element={<Navigate to={`/ticker/${defaultTicker.symbol}`} replace />} />
    </Routes>
  )
}
