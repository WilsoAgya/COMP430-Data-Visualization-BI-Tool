export type NewsArticle = {
    title: string
    description: string | null
    url: string
    imageUrl: string | null
    sourceName: string
    publishedAt: string | null
}

type NewsApiResponse = {
    status: "ok" | "error"
    message?: string
    articles?: Array<{
        source: { id: string | null; name: string }
        title: string | null
        description: string | null
        url: string | null
        urlToImage: string | null
        publishedAt: string | null
    }>
}

const NEWS_API_KEY = import.meta.env.news_api_key as string | undefined
const NEWS_API_URL = "https://newsapi.org/v2/everything"

export async function fetchStockNews(symbol: string, companyName: string): Promise<NewsArticle[]> {
    if (!NEWS_API_KEY) {
        throw new Error("Missing news_api_key in frontend/.env.local")
    }

    const cleanCompany = companyName
        .replace(/\b(inc|inc\.|corp|corporation|ltd|llc|plc|co|company)\b/gi, "")
        .replace(/\s+/g, " ")
        .trim()

    const from = new Date(Date.now() - 14 * 24 * 60 * 60 * 1000).toISOString().slice(0, 10)
    const query = [`"${symbol}"`, cleanCompany ? `"${cleanCompany}"` : ""].filter(Boolean).join(" OR ")

    const url = new URL(NEWS_API_URL)
    url.searchParams.set("q", query)
    url.searchParams.set("qInTitle", query)
    url.searchParams.set("searchIn", "title,description")
    url.searchParams.set("language", "en")
    url.searchParams.set("sortBy", "publishedAt")
    url.searchParams.set("pageSize", "12")
    url.searchParams.set("from", from)
    url.searchParams.set("apiKey", NEWS_API_KEY)

    const response = await fetch(url.toString())
    const payload = (await response.json()) as NewsApiResponse

    if (!response.ok || payload.status === "error") {
        throw new Error(payload.message || "Failed to fetch news")
    }

    const loweredSymbol = symbol.toLowerCase()
    const loweredCompany = cleanCompany.toLowerCase()

    return (payload.articles || [])
        .filter((a) => a.title && a.url)
        .map((a) => ({
            title: a.title as string,
            description: a.description,
            url: a.url as string,
            imageUrl: a.urlToImage,
            sourceName: a.source?.name || "Unknown source",
            publishedAt: a.publishedAt,
        }))
        .filter((a) => {
            const text = `${a.title} ${a.description ?? ""}`.toLowerCase()
            return text.includes(loweredSymbol) || (loweredCompany && text.includes(loweredCompany))
        })
        .slice(0, 8)
}

