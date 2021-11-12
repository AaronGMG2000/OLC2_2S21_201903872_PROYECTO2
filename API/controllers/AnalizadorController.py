from fastapi import APIRouter
from shared.models import RequestModel
from ANALIZADOR import grammar as gramatica
from ANALIZADOR.GENERAL.Arbol import Arbol
from ANALIZADOR.GENERAL.generator import Generador
from OPTIMIZADOR import grammar as Optimizador
import sys

router = APIRouter()


@router.post('/Compilar')
async def analysis(req: RequestModel):
    try:
        sys.setrecursionlimit(10**6)
        h = gramatica.parse(req.Contenido)
        genAux = Generador()
        genAux.limpiar()
        generador = genAux.get_instance()
        ast = Arbol(h)
        ast.ejecutar()
        consola = generador.get_code()
        gramatica.start = ""
        return {"consola": consola, "Simbolo": ast.Lista_Simbolo, "Errores": ast.errors, "AST": ""}
    except Exception as e:
        print(e)
        return{"consola": str(e), "Simbolo":[], "Errores": [], "AST": ""}
    
    
@router.get('/Prueba')
async def analysis():
    return {"prueba": "hola"}


@router.post('/Mirilla')
async def analysis(req: RequestModel):
    try:
        opti = Optimizador.parse(req.Contenido)
        opti.Mirilla()
        return {'consola': opti.get_code(), 'mirilla': opti.rules}
    except Exception as e:
        print(e)
        return {'consola': str(e), 'mirilla': []}