import { useState } from 'react'
import { procesarImagen } from '../../api/client.js'
import Controles from './Controles.jsx'
import ComparadorImagenes from './ComparadorImagenes.jsx'
import './ImagenDigitalizador.css'

export default function ImagenDigitalizador() {
  const [archivo, setArchivo] = useState(null)
  const [previewOriginal, setPreviewOriginal] = useState(null)
  const [resolucion, setResolucion] = useState(500)
  const [bitsPorCanal, setBitsPorCanal] = useState(24)
  const [comprimir, setComprimir] = useState(false)
  const [resultado, setResultado] = useState(null)
  const [cargando, setCargando] = useState(false)
  const [error, setError] = useState(null)

  function manejarArchivo(event) {
    const seleccionado = event.target.files?.[0]
    if (!seleccionado) return
    setArchivo(seleccionado)
    setResultado(null)
    setError(null)
    setPreviewOriginal(URL.createObjectURL(seleccionado))
  }

  async function manejarProcesar() {
    if (!archivo) {
      setError('Primero cargá una imagen')
      return
    }
    setCargando(true)
    setError(null)
    try {
      const data = await procesarImagen({ archivo, resolucion, bitsPorCanal, comprimir })
      setResultado(data)
    } catch (err) {
      setError(err.message)
    } finally {
      setCargando(false)
    }
  }

  return (
    <section className="digitalizador">
      <div className="digitalizador__panel panel">
        <div className="digitalizador__carga">
          <label className="boton boton--secundario">
            Cargar imagen
            <input type="file" accept="image/*" onChange={manejarArchivo} hidden />
          </label>
          {archivo && <span className="digitalizador__nombre-archivo">{archivo.name}</span>}
        </div>

        <Controles
          resolucion={resolucion}
          onResolucion={setResolucion}
          bitsPorCanal={bitsPorCanal}
          onBitsPorCanal={setBitsPorCanal}
          comprimir={comprimir}
          onComprimir={setComprimir}
          onProcesar={manejarProcesar}
          cargando={cargando}
          deshabilitado={!archivo}
        />

        {error && <p className="mensaje-error">{error}</p>}
      </div>

      <ComparadorImagenes
        previewOriginal={previewOriginal}
        resultado={resultado}
        tamanoOriginalArchivo={archivo?.size}
      />
    </section>
  )
}
