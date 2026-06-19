function formatearBytes(bytes) {
  if (!bytes) return '—'
  const unidades = ['B', 'KB', 'MB']
  let valor = bytes
  let i = 0
  while (valor >= 1024 && i < unidades.length - 1) {
    valor /= 1024
    i += 1
  }
  return `${valor.toFixed(1)} ${unidades[i]}`
}

export default function ComparadorImagenes({ previewOriginal, resultado, tamanoOriginalArchivo }) {
  const reduccion =
    resultado && tamanoOriginalArchivo
      ? (100 - (resultado.tamano_digitalizado_bytes / tamanoOriginalArchivo) * 100).toFixed(1)
      : null

  return (
    <div className="comparador">
      <div className="comparador__panel panel">
        <h3>Original</h3>
        <div className="comparador__lienzo">
          {previewOriginal ? (
            <img src={previewOriginal} alt="Imagen original" />
          ) : (
            <p className="vacio">Cargá una imagen para comenzar</p>
          )}
        </div>
        <p className="comparador__tamano">Tamaño: {formatearBytes(tamanoOriginalArchivo)}</p>
      </div>

      <div className="comparador__panel panel">
        <h3>Digitalizada</h3>
        <div className="comparador__lienzo">
          {resultado ? (
            <img
              src={resultado.imagen_digitalizada_base64}
              alt="Imagen digitalizada"
              className="comparador__imagen-pixelada"
            />
          ) : (
            <p className="vacio">Procesá la imagen para ver el resultado</p>
          )}
        </div>
        <p className="comparador__tamano">
          Tamaño: {resultado ? formatearBytes(resultado.tamano_digitalizado_bytes) : '—'}
          {reduccion !== null && <span className="comparador__reduccion"> ({reduccion}% menos)</span>}
        </p>
      </div>
    </div>
  )
}
