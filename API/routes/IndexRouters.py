from fastapi import APIRouter
from controllers import AnalizadorController as analysis

router = APIRouter()

router.include_router(analysis.router, prefix='', tags=['Compilar'])
