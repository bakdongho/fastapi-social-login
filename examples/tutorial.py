from typing import Optional
import uvicorn
import logging
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi import FastAPI, Request
from starlette.templating import Jinja2Templates
from fastapi_oauth_client import OAuthClient

app = FastAPI()


templates = Jinja2Templates(directory="templates")


naver_client = OAuthClient(
    client_id="your_client_id",
    client_secret="your_client_secret_id",
    redirect_uri="http://127.0.0.1:8000/callback/naver",
    authentication_url="https://nid.naver.com/oauth2.0",
    resource_url="https://openapi.naver.com/v1/nid/me",
)

kakao_client = OAuthClient(
    client_id="your_client_id",
    client_secret="your_client_secret_id",
    redirect_uri="http://127.0.0.1:8000/callback/kakao",
    authentication_url="https://kauth.kakao.com/oauth",
    resource_url="https://kapi.kakao.com/v2/user/me",
)


@app.get("/", response_class=HTMLResponse)
async def login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@app.get("/login/naver")
async def login_naver():
    login_url = naver_client.get_oauth_login_url(state="test")
    print(login_url)
    return RedirectResponse(login_url)


@app.get("/login/kakao")
async def login_kakao():
    login_url = kakao_client.get_oauth_login_url(state="test")
    print(login_url)
    return RedirectResponse(login_url)


@app.get("/callback/naver")
async def callback(code: str, state: Optional[str] = None):
    token_response = await naver_client.get_tokens(code, state)

    return {"response": token_response}


@app.get("/callback/kakao")
async def callback(code: str, state: Optional[str] = None):
    token_response = await kakao_client.get_tokens(code, state)

    return {"response": token_response}
