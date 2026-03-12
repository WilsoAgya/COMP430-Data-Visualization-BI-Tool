import { Area, AreaChart, CartesianGrid, XAxis } from "recharts"
import DashboardFilters from "@/components/dashboard/dashboard-filters"
import {
  mockChartData,
  mockStockCard,
  mockTickers,
} from "@/components/data/mock-data"

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

const chartConfig = {
  high: { label: "High Price", color: "var(--chart-1)" },
  low: { label: "Low Price", color: "var(--chart-2)" },
} satisfies ChartConfig

function App() {

  return (
      <main className="bg-background text-foreground min-h-screen px-4 py-10">
        <div className="mx-auto flex h-full w-full max-w-5xl flex-col gap-6">
          <header className="space-y-2">
            <h1 className="text-3xl font-semibold tracking-tight">BI Tool & Data Warehouse</h1>
            <p className="text-muted-foreground text-sm">A data visualization tool for COMP430</p>
          </header>

          <DashboardFilters
              tickers={mockTickers}
              onSelectTicker={(ticker) => console.log(ticker)}
          />

          <Tabs defaultValue="stock-info" className="w-full">
            <TabsList>
              <TabsTrigger value="stock-info">Stock Data</TabsTrigger>
              <TabsTrigger value="charts">Chart</TabsTrigger>
              <TabsTrigger value="news">News</TabsTrigger>
            </TabsList>

            <TabsContent value="stock-info">
              <StockCard {...mockStockCard} />
            </TabsContent>

            <TabsContent value="charts">
              <Card>
                <CardHeader>
                  <CardTitle>Example for stock</CardTitle>
                  <CardDescription>Graphs probably gonna be useful</CardDescription>
                </CardHeader>
                <CardContent>
                  <ChartContainer config={chartConfig} className="min-h-[280px] w-full">
                    <AreaChart data={mockChartData} margin={{ left: 12, right: 12 }}>
                      <CartesianGrid vertical={false} />
                      <XAxis dataKey="month" tickLine={false} axisLine={false} tickMargin={8} interval={0} />
                      <ChartTooltip content={<ChartTooltipContent indicator="line" />} />
                      <ChartLegend content={<ChartLegendContent />} />
                      <Area dataKey="high" type="bump" fill="var(--color-high)" fillOpacity={0.25} stroke="var(--color-high)" strokeWidth={2} />
                      <Area dataKey="low" type="bump" fill="var(--color-low)" fillOpacity={0.35} stroke="var(--color-low)" strokeWidth={2} />
                    </AreaChart>
                  </ChartContainer>
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
