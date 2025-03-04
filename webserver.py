from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles   # Used for serving static files
import uvicorn
import asyncio

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def home_page():
    with open ("static/index.html") as html:
        return HTMLResponse(content = html.read())

@app.put("/status")
async def change_status(data_from_request: dict):
    newState = data_from_request['SelectedState']
    print(newState)
    
async def ambient_light_controller():
    while True: 
        print("hello world")
        await asyncio.sleep(0.2)

if __name__ == "__main__":
    await ambient_light_controller()
    uvicorn.run("webserver:app", host="0.0.0.0", port=8000, reload=True)