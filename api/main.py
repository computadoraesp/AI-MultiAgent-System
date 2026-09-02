# Source Generated with Decompyle++
# File: main.cpython-312.pyc (Python 3.12)

from fastapi import FastAPI
from api.routes.execute_route import router as execute_router
from api.routes.openai_route import router as openai_router
app = FastAPI(title = 'AI MultiAgent System', version = '1.0.0')
root = (lambda : {
'status': 'running',
'system': 'AI MultiAgent System' })()
app.include_router(execute_router)
app.include_router(openai_router)
