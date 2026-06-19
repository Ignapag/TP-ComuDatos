import ImagenDigitalizador from './components/ImagenDigitalizador/ImagenDigitalizador.jsx'
import './styles/shared.css'
import './App.css'

export default function App() {
  return (
    <div className="app">
      <header className="app__header">
        <h1>Comunicación de Datos · TP Integrador</h1>
        <p>UTN La Plata · Comisión S33</p>
      </header>

      <main className="app__main">
        <ImagenDigitalizador />
      </main>
    </div>
  )
}
