import { MoonIcon, SunIcon } from "lucide-react"
import { Label } from "../ui/label"
import { Switch } from "../ui/switch"
import { useEffect, useState } from "react"

function getInitialDarkMode() {
  if (typeof window === "undefined") {
    return false
  }

  const storedTheme = window.localStorage.getItem("theme")
  if (storedTheme === "dark") return true
  if (storedTheme === "light") return false

  return window.matchMedia("(prefers-color-scheme: dark)").matches
}

export default function ThemeSelector() {
  const [isDarkMode, setIsDarkMode] = useState(getInitialDarkMode)

  useEffect(() => {
    document.documentElement.classList.toggle("dark", isDarkMode)
    window.localStorage.setItem("theme", isDarkMode ? "dark" : "light")
  }, [isDarkMode])
  return (
    <div className="bg-card flex items-center gap-2 rounded-lg border px-3 py-2">
      <div className="text-muted-foreground flex items-center gap-1 text-xs">
        <SunIcon className="h-3.5 w-3.5" />
        <MoonIcon className="h-3.5 w-3.5" />
      </div>
      <Label htmlFor="dark-mode">Dark mode</Label>
      <Switch id="dark-mode" checked={isDarkMode} onCheckedChange={setIsDarkMode} />
    </div>
  )
}
