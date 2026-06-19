import './Tabs.css'

export default function Tabs({ secciones, activa, onCambiar }) {
  return (
    <nav className="tabs">
      {secciones.map((seccion) => (
        <button
          key={seccion.id}
          className={`tabs__boton ${activa === seccion.id ? 'tabs__boton--activo' : ''}`}
          onClick={() => onCambiar(seccion.id)}
        >
          {seccion.etiqueta}
        </button>
      ))}
    </nav>
  )
}
