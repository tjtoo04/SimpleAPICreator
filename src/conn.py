#FastAPI Useful Links
#https://stackoverflow.com/questions/67399724/what-is-the-best-way-to-stop-uvicorn-server-programmatically

import os
import signal
from fastapi import FastAPI, HTTPException, Response
from pydantic import BaseModel
from typing import Optional, Union

#The template for all items of the API
class Item(BaseModel, extra='allow'):
    id : int
    category: Optional[str] = None
    value: Union[str, int, float]

items = {1: Item(id=1, category=None, value="hahaah")}

def shutdown():
    os.kill(os.getpid(), signal.SIGTERM)
    return Response(status_code=200, content='Server shutting down...')

app = FastAPI()

#Root
@app.get("/")
async def index() -> dict[str, dict[int, Item]]:
    return {'result': items}

#Querying a specific item from the API
@app.get("/items/{item_ID}")
async def query_item(item_ID: int) -> Item:
    if item_ID not in items:
        raise HTTPException(status_code=404, detail=f"Item with {item_ID = } does not exist")
    return items[item_ID]

#Posting into the API
@app.post('/')
async def add_items(item: Item):
    if item.id in items:
        raise HTTPException(status_code=400, detail=f"Item with {item.id=} already exists.")

    items[item.id] = item
    return {"added": item}

#Updating a specific item of the API
@app.put("/items/{item_ID}")
def update(item_ID:int, category: Optional[str] = None, value: Optional[str] = None) -> dict[str, Item]:
    if item_ID not in items:
        raise HTTPException(status_code=404, detail=f"Item with {item_ID = } does not exist")
    if all(other is None for other in (category, value)):
        raise HTTPException(status_code=400, detail=f"No parameters provided")
    
    item = items[item_ID]
    if value is not None:
        item.value = value
    return {"changed" : item}

#Deleting a specific item from the API
@app.delete("/items/{item_ID}")
def delete_item(item_ID:int) -> dict[str, Item]:
    if item_ID not in items:
        raise HTTPException(status_code=404, detail=f"Item with {item_ID = } does not exist")
    
    deleted_item = items.pop(item_ID)
    return {'deleted': deleted_item}

@app.on_event('shutdown')
async def on_shutdown():
    print('Server shutting down...')

app.add_api_route('/shutdown', shutdown, methods=['GET'])

