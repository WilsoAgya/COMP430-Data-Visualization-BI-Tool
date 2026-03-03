import { Badge } from "../ui/badge"
import ThemeSelector from "./theme-selector"

export default function Footer() {
  return (
    <div className="flex flex-col items-center justify-between gap-4 sm:flex-row">
      <div className="flex flex-col gap-2">
        <p className="text-muted-foreground text-sm">COMP430 Data Visualization BI Tool.</p>
        <div className="flex flex-wrap items-center gap-2">
          <a href="https://github.com/WilsoAgya">
            <Badge variant="secondary">Wilson Agyapong</Badge>
          </a>
          <a href="https://github.com/harryrai" target="_blank">
            <Badge variant="secondary">Harry Rai</Badge>
          </a>
          <a href="https://github.com/jakobupton" target="_blank">
            <Badge variant="secondary">Jakob Upton</Badge>
          </a>
          <a href="https://github.com/pragti-duggal" target="_blank">
            <Badge variant="secondary">Pragti Duggal</Badge>
          </a>
          <a href="https://github.com/Gurv-Chahal" target="_blank">
            <Badge variant="secondary">Gurveer Chahal</Badge>
          </a>
        </div>
      </div>
      <ThemeSelector />
    </div>
  )
}
