from fastapi import FastAPI
from warthunder.api import router as warthunder_router
#from caixa.api import router as caixa_router

app = FastAPI()

app.include_router(warthunder_router, prefix="/warthunder", tags=["War Thunder"])
#app.include_router(caixa_router, prefix="/caixa", tags=["Caixa"])
