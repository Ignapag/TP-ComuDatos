export default function TablaCodigos({ simbolos }) {
  if (!simbolos?.length) {
    return <p className="vacio">Codificá un texto para ver la tabla</p>
  }

  return (
    <table className="tabla-codigos">
      <thead>
        <tr>
          <th>Símbolo</th>
          <th>Frec.</th>
          <th>Código</th>
        </tr>
      </thead>
      <tbody>
        {simbolos.map((info) => (
          <tr key={info.simbolo}>
            <td>{info.simbolo === ' ' ? '␣' : `'${info.simbolo}'`}</td>
            <td>{info.frecuencia}</td>
            <td className="tabla-codigos__codigo">{info.codigo}</td>
          </tr>
        ))}
      </tbody>
    </table>
  )
}
