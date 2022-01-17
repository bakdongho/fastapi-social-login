from fastapi.responses import HTMLResponse
from fastapi import FastAPI, Request
from starlette.templating import Jinja2Templates
from fastapi_oauth_client import OAuthClient

app = FastAPI()

templates = Jinja2Templates(directory="templates")


oauth_client = OAuthClient(
    client_id="testid",
    client_secret="testsecret",
    redirect_uri="test",
    authentication_url="test",
    resource_url="test",
)


@app.get("/", response_class=HTMLResponse)
async def login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@app.get("/login", response_model=str)
async def login():
    login_url = oauth_client.get_login_url()
    return login_url


# if __name__ == "__main__":
#     uvicorn.run("main:app", port=8000, reload=True)
