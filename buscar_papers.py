from scholarly import scholarly
import time 

def buscar_papers(consulta, max_resultados=5):
    """
    Busca papers académicos en Google Scholarly.

    Args:
        consulta(str): Término de búsqueda (ej: "machine learning")
        max_resultados(int):Número máximo de resultados a devolver.

    Returns:
        list: Lista de Diccionarios con información de Papers.

    """
    print(f"\n Buscando... 👁️‍🗨️")
    print(f"Puede tardar hasta que el clima se congele... ☃️")

    resultados = []
    try:
        busqueda = scholarly.search_pubs(consulta)
        for i in range(max_resultados):
            try:
                paper = next(busqueda)
                info_paper={
                    'titulo': paper.get('bib',{}).get('title', 'sin título'),
                    'autores': paper.get('bib',{}).get('author', 'sin autor'),
                    'año': paper.get('bib',{}).get('pub_year', 'sin año'),
                    'revista': paper.get('bib',{}).get('veneu', 'sin nombre'),
                    'resumen': paper.get('bib',{}).get('abstract', 'sin resumen'),
                    'citacion': paper.get('citations', 0),
                    'url': paper.get('pub_url', paper.get('eprint_url', 'sin url')),

                }
                resultados.append(info_paper)
                time.sleep(1)
            except StopIteration:
                print(f"\Sólo se obtuvieron {len(resultados)}")
                break
            except Exception as e:
                print(f"Error {e}")
                continue
            print(f"\n Búsqueda Completada.")
            return resultados
    except Exception as e:
        print(f"Error {e}")
        return []
    

def formato_resultado(paper, numero):
    """
    Formatea la información de un paper para mostrarla más bonito.

    Args:
        paper (dict): Diccionario con la info del paper.
        numero (int): Número del paper en la lista.

    Returns:
        str: Texto formateado.
    """

    if isinstance(paper['autores'], list):
        autores: ','.join(paper['autores'])
    else:
        autores = paper['autores']

    resumen = paper['resumen']
    if len(resumen)>300:
        resumen = resumen[:300]+"..."
    texto = f"""
{'-'*60}
PAPER #{numero}
{'-'*60}
TITULO: {paper['titulo']}
{'-'*60}
Autor: {autores}
{'-'*60}
Revista: {paper['revista']}
{'-'*60}
Cita: {paper['citacion']}
{'-'*60}
Resumen: {resumen}
{'-'*60}
URL: {paper['url']}
""" 
    return texto

def mostrar_resultados(resultados):
    """

    Muestra todos los resultados de forma organizada.

    Args:
        resultados (list): Lista de papers encontrados.
    """

    if not resultados:
        print("No hay resultados")
        return
    print(f"Resultadoos")
    for i, paper in enumerate(resultados, 1):
        print(formato_resultado(paper, i))

def resumen_paper(resultados):
    """

    Crea un resumen de texto de todos los Papers para pasarlo al Agente.

    Args:
        resultados (list): Lista de papers.

    Returns: 
        str: Resumen de texto en todos los papers.
    
    """

    if not resultados:
        return "No se encuentran papers"
    resumen_texto = f"Se encuentran {len(resultados)}"
    for i, paper in enumerate(resultados, 1):
        autores = ','.join(paper['autores']) if isinstance(paper['autores'], list) else paper ['autores']
        resumen_texto += f"""
        Paper {i}:
        - Título: {paper['titulo']}
        - Autores: {paper['autores']} 
        - Año: {paper['año']}
        - Revista: {paper['revista']}
        - Resumen: {paper['resumen'][:200]}
        - Citación: {paper['citacion']}
        - URL: {paper['url']}

"""