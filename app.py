import os
from fastapi import FastAPI, HTTPException
import serpapi
from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()
API_KEY = os.getenv("SERPAPI_KEY")

app = FastAPI()


class SearchShopping(BaseModel):
    query: str


@app.post("/search_shopping/")
async def search_shopping(params: SearchShopping):
    params = {
        "engine": "google_shopping",
        "q": params.query,
        "api_key": API_KEY
    }

    search = serpapi.search(params)
    shopping_results = search["shopping_results"]
    return shopping_results


@app.post("/product_details/")
async def product_details(product_id: str):
    params = {
        "engine": "google_product",
        "product_id": product_id,
        "gl": "us",
        "hl": "en",
        "api_key": API_KEY
    }

    try:
        search = serpapi.search(params)
        product_results = search.get("product_results", {})
        return {"product_results": product_results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
