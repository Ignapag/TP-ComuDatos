const BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

async function manejarRespuesta(respuesta) {
  if (!respuesta.ok) {
    const error = await respuesta.json().catch(() => ({}))
    throw new Error(error.detail || `Error ${respuesta.status}`)
  }
  return respuesta.json()
}

export async function procesarImagen({ archivo, resolucion, bitsPorCanal, comprimir }) {
  const formData = new FormData()
  formData.append('archivo', archivo)
  formData.append('resolucion', resolucion)
  formData.append('bits_por_canal', bitsPorCanal)
  formData.append('comprimir', comprimir)

  const respuesta = await fetch(`${BASE_URL}/imagen/procesar`, {
    method: 'POST',
    body: formData,
  })
  return manejarRespuesta(respuesta)
}

export async function codificarTexto(metodo, texto) {
  const respuesta = await fetch(`${BASE_URL}/codificar/${metodo}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ texto }),
  })
  return manejarRespuesta(respuesta)
}

export async function decodificarTexto(codigoBinario, codigos) {
  const respuesta = await fetch(`${BASE_URL}/codificar/decodificar`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ codigo_binario: codigoBinario, codigos }),
  })
  return manejarRespuesta(respuesta)
}
