const ESPACIO_X = 64
const ESPACIO_Y = 64
const RADIO = 20

function calcularLayout(nodo, profundidad, contexto) {
  if (!nodo) return null
  if (!nodo.izquierda && !nodo.derecha) {
    const x = contexto.siguienteX
    contexto.siguienteX += 1
    return { ...nodo, x, y: profundidad, hijos: [] }
  }
  const hijos = [
    calcularLayout(nodo.izquierda, profundidad + 1, contexto),
    calcularLayout(nodo.derecha, profundidad + 1, contexto),
  ].filter(Boolean)
  const x = hijos.reduce((acc, h) => acc + h.x, 0) / hijos.length
  return { ...nodo, x, y: profundidad, hijos }
}

function aplanar(nodoLayout, lista = []) {
  if (!nodoLayout) return lista
  lista.push(nodoLayout)
  nodoLayout.hijos.forEach((hijo) => aplanar(hijo, lista))
  return lista
}

function obtenerAristas(nodoLayout, lista = []) {
  if (!nodoLayout) return lista
  nodoLayout.hijos.forEach((hijo, indice) => {
    lista.push({ desde: nodoLayout, hasta: hijo, etiqueta: indice === 0 ? '0' : '1' })
    obtenerAristas(hijo, lista)
  })
  return lista
}

export default function ArbolCodigos({ arbol }) {
  if (!arbol) {
    return <p className="vacio">Codificá un texto para ver el árbol</p>
  }

  const contexto = { siguienteX: 0 }
  const layout = calcularLayout(arbol, 0, contexto)
  const nodos = aplanar(layout)
  const conexiones = obtenerAristas(layout)

  const maxX = Math.max(...nodos.map((n) => n.x))
  const maxY = Math.max(...nodos.map((n) => n.y))
  const ancho = (maxX + 1) * ESPACIO_X + RADIO * 2
  const alto = (maxY + 1) * ESPACIO_Y + RADIO * 2

  function coordenada(nodo) {
    return { cx: nodo.x * ESPACIO_X + RADIO, cy: nodo.y * ESPACIO_Y + RADIO }
  }

  return (
    <div className="arbol-codigos">
      <svg width={ancho} height={alto} viewBox={`0 0 ${ancho} ${alto}`}>
        {conexiones.map((conexion, indice) => {
          const desde = coordenada(conexion.desde)
          const hasta = coordenada(conexion.hasta)
          return (
            <g key={indice}>
              <line x1={desde.cx} y1={desde.cy} x2={hasta.cx} y2={hasta.cy} stroke="#94a3b8" strokeWidth="1.5" />
              <text x={(desde.cx + hasta.cx) / 2 + 6} y={(desde.cy + hasta.cy) / 2} fontSize="11" fill="#64748b">
                {conexion.etiqueta}
              </text>
            </g>
          )
        })}
        {nodos.map((nodo) => {
          const { cx, cy } = coordenada(nodo)
          const esHoja = nodo.simbolo !== null && nodo.simbolo !== undefined
          return (
            <g key={nodo.id}>
              <circle cx={cx} cy={cy} r={RADIO} fill={esHoja ? '#ffffff' : '#2563eb'} stroke="#2563eb" strokeWidth="2" />
              <text
                x={cx}
                y={cy + 4}
                textAnchor="middle"
                fontSize="11"
                fontWeight="600"
                fill={esHoja ? '#1e3a8a' : '#ffffff'}
              >
                {esHoja ? (nodo.simbolo === ' ' ? '␣' : nodo.simbolo) : nodo.frecuencia}
              </text>
            </g>
          )
        })}
      </svg>
    </div>
  )
}
