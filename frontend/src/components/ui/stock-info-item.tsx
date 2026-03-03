export default function StockInfoItem(props: { label: string; value: string }) {
  return (
    <div className="flex flex-col gap-1">
      <p className="text-sm font-light">{props.label}</p>
      <p className="text-lg font-medium">{props.value}</p>
    </div>
  )
}
