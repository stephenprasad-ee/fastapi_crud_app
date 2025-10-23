# app.py
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.responses import PlainTextResponse
# from fastapi.responses import Response

import json
from pydantic import BaseModel
import logging
from pythonjsonlogger import jsonlogger
from datetime import datetime
from typing import List, Dict


# ---------------------------------------------------------------------------------------
# Use below code to format JSON responses by adding -
#   ', response_class=PrettyJSONResponse'
# to the function call AFTER uncommenting below lines (19 to 25)
# example: [Line 98] @app.get("/health", response_class=PrettyJSONResponse )
# ---------------------------------------------------------------------------------------

class PrettyJSONResponse(JSONResponse):

    def render(self, content: any) -> bytes:
        return json.dumps(
            content,
            ensure_ascii=False,
            indent=4  # pretty print with 4 spaces
        ).encode("utf-8")


# ---------------------
# Setup JSON Logging
# ---------------------
logger = logging.getLogger("crud_api")
logHandler = logging.StreamHandler()
formatter = jsonlogger.JsonFormatter('%(asctime)s %(levelname)s %(message)s')
logHandler.setFormatter(formatter)
logger.addHandler(logHandler)
logger.setLevel(logging.INFO)

# ---------------------
# FastAPI App
# ---------------------
app = FastAPI(title="CRUD API with FastAPI", version="1.1")


# ---------------------------------------------------
# Adding code to send all responses in formatted JSON
# ---------------------------------------------------
# @app.middleware("http")
# async def json_formatter_middleware(request: Request, call_next):
#     response = await call_next(request)
#     if response.media_type == "application/json":
#         content = await response.body()
#         parsed = json.loads(content)
#         formatted_content = json.dumps(parsed, indent=4)
#         return Response(content=formatted_content,
# media_type="application/json")
#     return response
# ---------------------------------------------------

# ---------------------
# In-memory "database"
# ---------------------
items_db: Dict[int, dict] = {}
current_id = 0

# ---------------------
# Pydantic Models
# ---------------------


class Item(BaseModel):

    name: str
    description: str = None
    price: float
    quantity: int


class ItemResponse(Item):

    id: int

# ---------------------
# Exception Handlers
# ---------------------


@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):

    logger.error(f"Unhandled error: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"message": "Internal Server Error"}
    )

# ---------------------
# Base Endpoint
# ---------------------

# @app.get("/", response_class=PrettyJSONResponse)
# async def root():
#     help_text = [
#         "Welcome to the Steve's FastAPI CRUD API! with Swagger built-in!",
#         "===============================================================",
#         "Available Endpoints:",
#         "--------------------",
#         "1. Health Check - GET /health",
#         "2. Create Item - POST /items/ with JSON body { ... }",
#         "3. List All Items - GET /items/",
#         "4. Get Item by ID - GET /items/{item_id}",
#         "5. Update Item - PUT /items/{item_id} with JSON body { ... }",
#         "6. Delete Item - DELETE /items/{item_id}",
#     ]
#     return {"help": help_text}


@app.get("/", response_class=PlainTextResponse)
async def root():
    help_text = """
Welcome to the Steve's FastAPI CRUD API! with Swagger built-in!
================================

Available Endpoints:
-------------------
1. Health Check
   GET /health
   Returns the health status of the API with timestamp.

2. Create Item
   POST /items/
   JSON Body Example:
   {
       "name": "Sample Item",
       "description": "A description",
       "price": 10.5,
       "quantity": 2
   }

3. List All Items
   GET /items/
   Returns a list of all items.

4. Get Item by ID
   GET /items/{item_id}
   Replace {item_id} with the integer ID of the item.

5. Update Item by ID
   PUT /items/{item_id}
   JSON Body Example:
   {
       "name": "Updated Item",
       "description": "Updated description",
       "price": 15.0,
       "quantity": 3
   }

6. Delete Item by ID
   DELETE /items/{item_id}
   Replace {item_id} with the integer ID of the item.
"""
    return help_text.strip()


# ---------------------
# Health Check Endpoint
# ---------------------


@app.get("/health", response_class=PrettyJSONResponse)
async def health_check():
    logger.info("Health check requested")
    return {
        "status": "Healthy",
        "timestamp": datetime.utcnow().isoformat()
    }

# ---------------------
# CRUD Endpoints
# ---------------------


@app.post(
        "/items/",
        response_model=ItemResponse,
        response_class=PrettyJSONResponse
        )
async def create_item(item: Item):
    global current_id
    current_id += 1
    items_db[current_id] = item.dict()
    logger.info(
        "Item created",
        extra={"item_id": current_id, "item": item.dict()})
    return {**item.dict(), "id": current_id}


@app.get(
        "/items/",
        response_model=List[ItemResponse],
        response_class=PrettyJSONResponse
        )
async def list_items():
    logger.info("Listing all items", extra={"total_items": len(items_db)})
    return [{"id": item_id, **item} for item_id, item in items_db.items()]


@app.get(
        "/items/{item_id}",
        response_model=ItemResponse,
        response_class=PrettyJSONResponse
        )
async def get_item(item_id: int):
    item = items_db.get(item_id)
    if not item:
        logger.warning("Item not found", extra={"item_id": item_id})
        raise HTTPException(status_code=404, detail="Item not found")
    logger.info("Item retrieved", extra={"item_id": item_id})
    return {"id": item_id, **item}


@app.put(
        "/items/{item_id}",
        response_model=ItemResponse,
        response_class=PrettyJSONResponse
        )
async def update_item(item_id: int, updated_item: Item):
    if item_id not in items_db:
        logger.warning("Item not found for update", extra={"item_id": item_id})
        raise HTTPException(status_code=404, detail="Item not found")
    items_db[item_id] = updated_item.dict()
    logger.info(
        "Item updated",
        extra={"item_id": item_id, "item": updated_item.dict()}
        )
    return {"id": item_id, **updated_item.dict()}


@app.delete(
        "/items/{item_id}",
        response_model=dict,
        response_class=PrettyJSONResponse
        )
async def delete_item(item_id: int):
    if item_id not in items_db:
        logger.warning(
            "Item not found for deletion",
            extra={"item_id": item_id}
            )
        raise HTTPException(status_code=404, detail="Item not found")
    del items_db[item_id]
    logger.info("Item deleted", extra={"item_id": item_id})
    return {"message": f"Item {item_id} deleted successfully"}


# Use the following command to execute uvicorn locally with reload option:
# uvicorn app:app --reload
