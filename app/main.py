from fastapi import FastAPI
from app.api.v1.endpoints.recipe import router as recipe_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.router = recipe_router
app.add_middleware(
    CORSMiddleware,
    allow_origins="*",
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Recipe Structuring"}
