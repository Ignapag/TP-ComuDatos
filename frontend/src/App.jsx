import { useState } from 'react'
import Tabs from './components/Tabs.jsx'
import ImagenDigitalizador from './components/ImagenDigitalizador/ImagenDigitalizador.jsx'
import Codificador from './components/Codificador/Codificador.jsx'
import './styles/shared.css'
import './App.css'

const SECCIONES = [
  { id: 'imagen', etiqueta: 'Digitalización de imágenes' },
  { id: 'codificacion', etiqueta: 'Codificación de datos' },
]

export default function App() {
  const [seccionActiva, setSeccionActiva] = useState('imagen')

  return (
    <div className="app">
      <header className="app__header">
        <h1>Comunicación de Datos · TP Integrador</h1>
        <p>UTN La Plata · Comisión S33</p>
      </header>

      <Tabs secciones={SECCIONES} activa={seccionActiva} onCambiar={setSeccionActiva} />

      <main className="app__main">
        {seccionActiva === 'imagen' && <ImagenDigitalizador />}
        {seccionActiva === 'codificacion' && <Codificador />}
      </main>
    </div>
  )
}
