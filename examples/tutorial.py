import secrets
from typing import Optional
import uvicorn
import logging
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi import Depends, FastAPI, Query, Request
from starlette.templating import Jinja2Templates
from fastapi_oauth_client import OAuthClient

app = FastAPI()


templates = Jinja2Templates(directory="templates")


naver_client = OAuthClient(
    client_id="your_client_id",
    client_secret="your_client_secret_id",
    redirect_uri="http://127.0.0.1:8000/callback?provider=naver",
    authentication_url="https://nid.naver.com/oauth2.0",
    resource_url="https://openapi.naver.com/v1/nid/me",
)

kakao_client = OAuthClient(
    client_id="your_client_id",
    client_secret="your_client_secret_id",
    redirect_uri="http://127.0.0.1:8000/callback?provider=kakao",
    authentication_url="https://kauth.kakao.com/oauth",
    resource_url="https://kapi.kakao.com/v2/user/me",
)

def get_oauth_client(provider=Query(...,regex='naver|kakao')):
    if provider == "naver":
        return naver_client
    elif provider == "kakao":
        return kakao_client


@app.get("/", response_class=HTMLResponse)
async def login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@app.get("/login")
async def login_naver(oauth_client = Depends(get_oauth_client)):
    state = secrets.token_urlsafe(32)
    login_url = oauth_client.get_oauth_login_url(state=state)
    print(login_url)
    return RedirectResponse(login_url)


@app.get("/callback")
async def callback(code: str, state: Optional[str] = None, oauth_client = Depends(get_oauth_client)):
    token_response = await oauth_client.get_tokens(code, state)

    return {"response": token_response}
