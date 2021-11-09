from fastapi import APIRouter
from shared.models import RequestModel
from ANALIZADOR import grammar as gramatica
from ANALIZADOR.GENERAL.Arbol import Arbol
from ANALIZADOR.GENERAL.generator import Generador
import sys

router = APIRouter()


@router.post('/Compilar')
async def analysis(req: RequestModel):
        sys.setrecursionlimit(10**6)
        h = gramatica.parse(req.Contenido)
        genAux = Generador()
        genAux.limpiar()
        generador = genAux.get_instance()
        ast = Arbol(h)
        ast.ejecutar()
        consola = generador.get_code()
        gramatica.start = ""
        return {"consola": consola, "Simbolo": [], "Errores": ast.errors, "AST": ""}
    
@router.get('/Prueba')
async def analysis():
    return {"prueba": "hola"}
