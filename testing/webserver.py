from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles   # Used for serving static files


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

# Example route: return a static HTML page
@app.get("/", response_class=HTMLResponse)
def get_html() -> HTMLResponse:
  with open("index.html") as html:
    return HTMLResponse(content=html.read())


@app.get("/custom", response_class=HTMLResponse)
async def custom_page():
    return """
    <html>
        <head><title>Custom Page</title></head>
        <body>
            <h1>Hello from Custom Page!</h1>
            <p>This is served at /custom</p>
        </body>
    </html>
    """

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=6543)

