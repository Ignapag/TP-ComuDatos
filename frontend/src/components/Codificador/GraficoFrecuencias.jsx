export default function GraficoFrecuencias({ simbolos }) {
  if (!simbolos?.length) {
    return <p className="vacio">Sin datos</p>
  }

  const maxFrecuencia = Math.max(...simbolos.map((s) => s.frecuencia))

  return (
    <div className="grafico-frecuencias">
      {simbolos.map((info) => (
        <div className="grafico-frecuencias__barra-contenedor" key={info.simbolo}>
          <div
            className="grafico-frecuencias__barra"
            style={{ height: `${(info.frecuencia / maxFrecuencia) * 100}%` }}
            title={`${info.simbolo}: ${info.frecuencia}`}
          />
          <span className="grafico-frecuencias__etiqueta">{info.simbolo === ' ' ? '␣' : info.simbolo}</span>
        </div>
      ))}
    </div>
  )
}
