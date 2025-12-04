import ollama
import buscar_papers
import buscar_papers, formato_resultado, mostrar_resultados, resumen_paper

instrucciones = """ 
Eres un asistente experto en investigación académica y científica.

Tus funciones principales son:
1. Ayudar a buscar y analizar literatura científica.
2. Generar citas bibliográficas en formato APA e IEEE.
3. Resumir papers y artículos académicos.
4. Ayudar a estructurar proyectos de investigación.
5. Explicar conceptos científicos de forma clara.

Formato de Citas:
*APA: Apellido, A.A. (Año). Título de Artículos. Nombre de la Revista, Volumen (número), Páginas.
*IEEE: [#] A.A. Apellido, "Título de Artículo", Nombre de la Revista, Vol x No. y, pp. ZZ- Mes año.

Sé preciso, académico y proporciona fuentes cuando sea posible.
"""

historial = []

def chat(mensaje_user):
    mensajes = [
        {'role': 'system', 'content': instrucciones}
    ]
    
    mensajes.extend(historial)
    mensajes.append({'role': 'user', 'content': mensaje_user})

    try:
        respuesta = ollama.chat(
            model='gemma3:1b',
            messages=mensajes,
            stream=False
        )

        texto_respuesta = respuesta['message']['content']

        # Guardar en historial
        historial.append({'role': 'user', 'content': mensaje_user})
        historial.append({'role': 'assistant', 'content': texto_respuesta})

        return texto_respuesta

    except Exception as e:
        return f"Error: {e}"


while True:
    mensaje = input("Tu 😊: ").strip()

    if mensaje.lower() == 'salir':
        print("\nNos vemos. 😑")
        break

    if mensaje.lower() == 'limpiar':
        historial.clear()
        print("Historial limpiado.\n")
        continue

    if not mensaje:
        continue

    if mensaje.lower().startswith('buscar'):
        termino = mensaje[7:].strip()

        if not termino:
            print("Se debe especificar que buscar. Ejemeplo: IA.")
            continue
        resultados = buscar_papers(termino, max_resultados = 5)

        if resultados:
            ultimo_resultado = resultados(resultados)
            resumen = resumen_paper(resultados)
            pregunta = f"Buscar '{termino}'"
            respuesta = chat(pregunta, contexto_extra = resumen)
            print(f"\n Análisis: {respuesta}")
            print("-"*60)
        else:
            print("No se encontró nada.")
    else:
        contexto: None
        if ultimo_resultado and any(palabra in mensaje.lower()for palabra in ['paper', 'artículo', 'cita', 'referencia', 'estos', 'resultados'])
        contexto = resumen_paper(ultimo_resultado)
    respuesta = chat(mensaje)
    print(f"\n🐔 Agent:\n{respuesta}\n")
    print("-" * 60)