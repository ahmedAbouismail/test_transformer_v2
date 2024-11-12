from fastapi import FastAPI, UploadFile, HTTPException, File
from api.v1.endpoints.recipe import router as recipe_router

app = FastAPI()

app.router = recipe_router


@app.get("/")
async def root():
    return {"message": "Recipe Structuring"}