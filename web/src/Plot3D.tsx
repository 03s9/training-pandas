import { useEffect, useRef } from 'react'
import Plotly from 'plotly.js-dist-min'

type Point = Record<string, string | number>
export default function Plot3D({ points }: { points: Point[] }) {
  const ref = useRef<HTMLDivElement>(null)
  useEffect(() => {
    if (!ref.current) return
    const categories = [...new Set(points.map(point => String(point.categoria)))]
    const colors = ['#2563eb', '#0f172a', '#38bdf8', '#f59e0b', '#7c3aed']
    Plotly.newPlot(ref.current, categories.map((category, index) => {
      const rows = points.filter(point => point.categoria === category)
      return {
        type: 'scatter3d', mode: 'markers', name: category,
        x: rows.map(row => Number(row.quantidade)),
        y: rows.map(row => Number(row.preco_unitario)),
        z: rows.map(row => Number(row.avaliacao)),
        text: rows.map(row => String(row.produto)),
        marker: { size: 5, color: colors[index % colors.length], opacity: 0.85 },
        hovertemplate: '%{text}<br>Quantidade: %{x}<br>Preço: R$ %{y}<br>Avaliação: %{z}<extra></extra>',
      }
    }), {
      paper_bgcolor: '#fff', margin: { l: 0, r: 0, t: 0, b: 0 },
      font: { family: 'Work Sans, sans-serif', color: '#334155' },
      scene: {
        xaxis: { title: { text: 'Quantidade' } },
        yaxis: { title: { text: 'Preço unitário' } },
        zaxis: { title: { text: 'Avaliação' } },
      },
    }, { responsive: true, displaylogo: false })
    const node = ref.current
    return () => { Plotly.purge(node) }
  }, [points])
  return <div ref={ref} className="plot3d" role="img" aria-label="Gráfico 3D de quantidade, preço e avaliação por categoria. Os dados também aparecem na tabela abaixo." />
}
