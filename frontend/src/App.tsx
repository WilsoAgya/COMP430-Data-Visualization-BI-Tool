import { Area, AreaChart, CartesianGrid, XAxis } from "recharts"

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"

import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import {
  ChartContainer,
  ChartLegend,
  ChartLegendContent,
  ChartTooltip,
  ChartTooltipContent,
} from "@/components/ui/chart"
import type { ChartConfig } from "@/components/ui/chart"
import Footer from "./components/layout/footer"
import StockCard from "./components/stock-card"
const chartData = [
  { month: "Jan", high: 180, low: 84 },
  { month: "Feb", high: 120, low: 30 },
  { month: "Mar", high: 160, low: 140 },
  { month: "Apr", high: 30, low: 20 },
  { month: "May", high: 90, low: 50 },
  { month: "Jun", high: 15, low: 10 },
  { month: "Jul", high: 150, low: 70 },
  { month: "Aug", high: 200, low: 120 },
  { month: "Sep", high: 170, low: 100 },
  { month: "Oct", high: 80, low: 40 },
  { month: "Nov", high: 110, low: 60 },
  { month: "Dec", high: 190, low: 130 },
]

const chartConfig = {
  high: {
    label: "High Price",
    color: "var(--chart-1)",
  },
  low: {
    label: "Low Price",
    color: "var(--chart-2)",
  },
} satisfies ChartConfig

function App() {
  return (
    <main className="bg-background text-foreground min-h-screen px-4 py-10">
      <div className="mx-auto flex h-full w-full max-w-5xl flex-col gap-6">
        <header className="space-y-2">
          <div className="flex flex-wrap items-center justify-between gap-3"></div>
          <h1 className="text-3xl font-semibold tracking-tight">BI Tool & Data Warehouse</h1>
          <p className="text-muted-foreground text-sm">A data visualization tool for COMP430</p>
        </header>

        <Tabs defaultValue="stock-info" className="w-full">
          <TabsList>
            <TabsTrigger value="stock-info">Stock Data</TabsTrigger>
            <TabsTrigger value="charts">Chart</TabsTrigger>
            <TabsTrigger value="news">News</TabsTrigger>
          </TabsList>

          <TabsContent value="stock-info">
            <StockCard
              stockName="Alphabet Inc."
              stockSymbol="GOOG"
              ask={135.67}
              lastSale={134.89}
              open={133.5}
              close={134.2}
              high={136.0}
              low={132.8}
              exchange="NASDAQ"
              marketCap={1.5e12}
              peRatio={25.3}
              week52High={150.0}
              week52Low={120.0}
              volume={2e6}
              avgVolume={1.5e6}
              marginReq={50}
            />
          </TabsContent>

          <TabsContent value="charts">
            <Card>
              <CardHeader>
                <CardTitle>Example for stock</CardTitle>
                <CardDescription>Graphs probablty gonna be useful</CardDescription>
              </CardHeader>
              <CardContent>
                <ChartContainer config={chartConfig} className="min-h-[280px] w-full">
                  <AreaChart data={chartData} margin={{ left: 12, right: 12 }}>
                    <CartesianGrid vertical={false} />
                    <XAxis
                      dataKey="month"
                      tickLine={false}
                      axisLine={false}
                      tickMargin={8}
                      interval={0}
                    />
                    <ChartTooltip content={<ChartTooltipContent indicator="line" />} />
                    <ChartLegend content={<ChartLegendContent />} />
                    <Area
                      dataKey="high"
                      type="bump"
                      fill="var(--color-high)"
                      fillOpacity={0.25}
                      stroke="var(--color-high)"
                      strokeWidth={2}
                    />
                    <Area
                      dataKey="low"
                      type="bump"
                      fill="var(--color-low)"
                      fillOpacity={0.35}
                      stroke="var(--color-low)"
                      strokeWidth={2}
                    />
                  </AreaChart>
                </ChartContainer>
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="news">
            <Card>
              <CardHeader>
                <CardTitle>Alphabet Inc.</CardTitle>
                <CardDescription>GOOG</CardDescription>
              </CardHeader>
              <CardContent>
                <p className="text-muted-foreground">no news!</p>
              </CardContent>
            </Card>
          </TabsContent>
        </Tabs>
      </div>
      <footer className="mx-auto mt-10 w-full max-w-5xl border-t py-6">
        <Footer />
      </footer>
    </main>
  )
}

export default App
