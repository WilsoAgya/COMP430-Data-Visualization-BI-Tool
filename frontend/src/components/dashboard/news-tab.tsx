import { useEffect, useState } from "react"
import { ExternalLink, Newspaper } from "lucide-react"

import { fetchStockNews, type NewsArticle } from "@/lib/news-api"
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"

type NewsTabProps = {
    symbol: string
    companyName: string
}

function formatDate(value: string | null) {
    if (!value) return "Unknown date"

    return new Intl.DateTimeFormat("en-US", {
        dateStyle: "medium",
        timeStyle: "short",
    }).format(new Date(value))
}

export default function NewsTab({ symbol, companyName }: NewsTabProps) {
    const [articles, setArticles] = useState<NewsArticle[]>([])
    const [loading, setLoading] = useState(false)
    const [error, setError] = useState<string | null>(null)

    useEffect(() => {
        let cancelled = false

        async function load() {
            setLoading(true)
            setError(null)

            try {
                const data = await fetchStockNews(symbol, companyName)
                if (!cancelled) setArticles(data)
            } catch (err) {
                if (!cancelled) {
                    setArticles([])
                    setError(err instanceof Error ? err.message : "Failed to load news")
                }
            } finally {
                if (!cancelled) setLoading(false)
            }
        }

        load()

        return () => {
            cancelled = true
        }
    }, [symbol, companyName])

    if (loading) {
        return (
            <Card>
                <CardHeader>
                    <CardTitle>Recent News</CardTitle>
                    <CardDescription>Loading articles for {symbol}</CardDescription>
                </CardHeader>
                <CardContent className="text-sm text-muted-foreground">Loading news...</CardContent>
            </Card>
        )
    }

    if (error) {
        return (
            <Alert variant="destructive">
                <Newspaper />
                <AlertTitle>Could not load news</AlertTitle>
                <AlertDescription>{error}</AlertDescription>
            </Alert>
        )
    }

    if (!articles.length) {
        return (
            <Alert>
                <Newspaper />
                <AlertTitle>No recent articles found</AlertTitle>
                <AlertDescription>No recent news matched {symbol} / {companyName}.</AlertDescription>
            </Alert>
        )
    }

    return (
        <div className="grid gap-4">
            {articles.map((article) => (
                <Card key={article.url} className="overflow-hidden">
                    <div className="grid gap-0 md:grid-cols-[220px_1fr]">
                        <div className="bg-muted aspect-[16/10] overflow-hidden">
                            {article.imageUrl ? (
                                <img
                                    src={article.imageUrl}
                                    alt={article.title}
                                    className="h-full w-full object-cover"
                                />
                            ) : (
                                <div className="flex h-full items-center justify-center text-sm text-muted-foreground">
                                    No image
                                </div>
                            )}
                        </div>

                        <div>
                            <CardHeader className="gap-3">
                                <div className="flex flex-wrap items-center gap-2">
                                    <Badge variant="secondary">{article.sourceName}</Badge>
                                    <Badge variant="outline">{formatDate(article.publishedAt)}</Badge>
                                </div>
                                <CardTitle className="leading-snug">{article.title}</CardTitle>
                                {article.description ? (
                                    <CardDescription className="text-sm leading-6">{article.description}</CardDescription>
                                ) : null}
                            </CardHeader>

                            <CardContent>
                                <Button asChild variant="outline">
                                    <a href={article.url} target="_blank" rel="noreferrer">
                                        Read article
                                        <ExternalLink />
                                    </a>
                                </Button>
                            </CardContent>
                        </div>
                    </div>
                </Card>
            ))}
        </div>
    )
}
