const RESOLUCIONES = [100, 500, 1000]
const PROFUNDIDADES = [1, 8, 24]

export default function Controles({
  resolucion,
  onResolucion,
  bitsPorCanal,
  onBitsPorCanal,
  comprimir,
  onComprimir,
  onProcesar,
  cargando,
  deshabilitado,
}) {
  return (
    <div className="controles">
      <h2 className="controles__titulo">Controles</h2>

      <div className="controles__grupo">
        <label>Resolución (muestreo)</label>
        <div className="controles__opciones">
          {RESOLUCIONES.map((valor) => (
            <button
              key={valor}
              className={`chip ${resolucion === valor ? 'chip--activo' : ''}`}
              onClick={() => onResolucion(valor)}
            >
              {valor}²
            </button>
          ))}
        </div>
      </div>

      <div className="controles__grupo">
        <label>Bits por canal (cuantización)</label>
        <div className="controles__opciones">
          {PROFUNDIDADES.map((valor) => (
            <button
              key={valor}
              className={`chip ${bitsPorCanal === valor ? 'chip--activo' : ''}`}
              onClick={() => onBitsPorCanal(valor)}
            >
              {valor} bits
            </button>
          ))}
        </div>
      </div>

      <label className="controles__checkbox">
        <input type="checkbox" checked={comprimir} onChange={(e) => onComprimir(e.target.checked)} />
        Comprimir resultado (JPEG)
      </label>

      <button className="boton boton--primario" onClick={onProcesar} disabled={deshabilitado || cargando}>
        {cargando ? 'Procesando…' : 'Procesar imagen'}
      </button>
    </div>
  )
}
