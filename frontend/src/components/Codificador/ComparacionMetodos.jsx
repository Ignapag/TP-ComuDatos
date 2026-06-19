export default function ComparacionMetodos({ huffman, shannonFano }) {
  return (
    <div className="panel comparacion">
      <h3>Comparación de métodos</h3>
      <table className="tabla-comparacion">
        <thead>
          <tr>
            <th>Métrica</th>
            <th>Huffman</th>
            <th>Shannon-Fano</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>Bits originales</td>
            <td>{huffman.bits_originales}</td>
            <td>{shannonFano.bits_originales}</td>
          </tr>
          <tr>
            <td>Bits codificados</td>
            <td>{huffman.bits_codificados}</td>
            <td>{shannonFano.bits_codificados}</td>
          </tr>
          <tr>
            <td>Tasa de compresión</td>
            <td>{huffman.tasa_compresion}%</td>
            <td>{shannonFano.tasa_compresion}%</td>
          </tr>
          <tr>
            <td>Longitud promedio</td>
            <td>{huffman.longitud_promedio} bits</td>
            <td>{shannonFano.longitud_promedio} bits</td>
          </tr>
          <tr>
            <td>Entropía</td>
            <td>{huffman.entropia} bits</td>
            <td>{shannonFano.entropia} bits</td>
          </tr>
        </tbody>
      </table>
    </div>
  )
}
