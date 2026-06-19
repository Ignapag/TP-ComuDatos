import { useState } from 'react'
import { codificarTexto, decodificarTexto } from '../../api/client.js'
import TablaCodigos from './TablaCodigos.jsx'
import ArbolCodigos from './ArbolCodigos.jsx'
import GraficoFrecuencias from './GraficoFrecuencias.jsx'
import ComparacionMetodos from './ComparacionMetodos.jsx'
import './Codificador.css'

export default function Codificador() {
  const [texto, setTexto] = useState('comunicacion de datos utn la plata')
  const [metodoVisible, setMetodoVisible] = useState('huffman')
  const [resultados, setResultados] = useState(null)
  const [cargando, setCargando] = useState(false)
  const [error, setError] = useState(null)
  const [textoDecodificado, setTextoDecodificado] = useState(null)

  async function manejarCodificar() {
    if (!texto.trim()) {
      setError('Ingresá un texto para codificar')
      return
    }
    setCargando(true)
    setError(null)
    setTextoDecodificado(null)
    try {
      const [huffman, shannonFano] = await Promise.all([
        codificarTexto('huffman', texto),
        codificarTexto('shannon-fano', texto),
      ])
      setResultados({ huffman, shannonFano })
    } catch (err) {
      setError(err.message)
    } finally {
      setCargando(false)
    }
  }

  async function manejarDecodificar() {
    const resultadoActivo = resultados?.[metodoVisible === 'huffman' ? 'huffman' : 'shannonFano']
    if (!resultadoActivo) {
      setError('Primero codificá un texto con este método')
      return
    }
    setCargando(true)
    setError(null)
    try {
      const codigos = Object.fromEntries(resultadoActivo.simbolos.map((s) => [s.simbolo, s.codigo]))
      const data = await decodificarTexto(resultadoActivo.codigo_binario, codigos)
      setTextoDecodificado(data.texto)
    } catch (err) {
      setError(err.message)
    } finally {
      setCargando(false)
    }
  }

  function manejarArchivoTxt(event) {
    const archivo = event.target.files?.[0]
    if (!archivo) return
    const lector = new FileReader()
    lector.onload = () => setTexto(String(lector.result || ''))
    lector.readAsText(archivo)
  }

  const resultadoActivo = resultados?.[metodoVisible === 'huffman' ? 'huffman' : 'shannonFano']

  return (
    <section className="codificador">
      <div className="codificador__cabecera">
        <h2>Codificador · Huffman / Shannon-Fano</h2>
        <div className="codificador__toggle">
          <button
            className={`chip ${metodoVisible === 'huffman' ? 'chip--activo' : ''}`}
            onClick={() => setMetodoVisible('huffman')}
          >
            Huffman
          </button>
          <button
            className={`chip ${metodoVisible === 'shannon-fano' ? 'chip--activo' : ''}`}
            onClick={() => setMetodoVisible('shannon-fano')}
          >
            Shannon-Fano
          </button>
        </div>
      </div>

      <div className="codificador__grid">
        <div className="codificador__columna">
          <div className="panel">
            <h3>Entrada de texto</h3>
            <textarea
              value={texto}
              onChange={(e) => setTexto(e.target.value)}
              rows={4}
              placeholder="Escribí o pegá un texto…"
            />
            <div className="codificador__acciones">
              <button className="boton boton--primario" onClick={manejarCodificar} disabled={cargando}>
                {cargando ? 'Procesando…' : 'Codificar'}
              </button>
              <button className="boton boton--secundario" onClick={manejarDecodificar} disabled={cargando}>
                Decodificar
              </button>
              <label className="boton boton--secundario">
                Cargar .txt
                <input type="file" accept=".txt" onChange={manejarArchivoTxt} hidden />
              </label>
            </div>
            {error && <p className="mensaje-error">{error}</p>}
            {textoDecodificado !== null && (
              <p className="codificador__decodificado">
                Texto decodificado: <strong>{textoDecodificado}</strong>
              </p>
            )}
          </div>

          <div className="panel">
            <h3>Tabla de códigos</h3>
            <TablaCodigos simbolos={resultadoActivo?.simbolos} />
          </div>
        </div>

        <div className="codificador__columna">
          <div className="panel">
            <h3>Árbol de códigos</h3>
            <ArbolCodigos arbol={resultadoActivo?.arbol} />
          </div>

          <div className="panel">
            <h3>Frecuencias</h3>
            <div className="codificador__frecuencias">
              <GraficoFrecuencias simbolos={resultadoActivo?.simbolos} />
              <div className="metricas">
                <div className="metricas__item">
                  <span>Tasa de compresión</span>
                  <strong>{resultadoActivo ? `${resultadoActivo.tasa_compresion}%` : '—'}</strong>
                </div>
                <div className="metricas__item">
                  <span>Long. prom. código</span>
                  <strong>{resultadoActivo ? `${resultadoActivo.longitud_promedio} bits` : '—'}</strong>
                </div>
                <div className="metricas__item">
                  <span>Entropía</span>
                  <strong>{resultadoActivo ? `${resultadoActivo.entropia} bits` : '—'}</strong>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {resultados && <ComparacionMetodos huffman={resultados.huffman} shannonFano={resultados.shannonFano} />}
    </section>
  )
}
