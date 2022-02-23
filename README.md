# Fastapi Social Login

네이버와 카카오 로그인을 fastapi에서 쉽게 이용할 수 있도록 제작했습니다.

# Example

네이버를 기준으로 사용법을 작성하겠습니다.

➕ 둘 이상 oauth client 이용시 service provider의 구분이 필요하므로 요청시 parameter로 provider를 받는 형식으로 예제 구현하였습니다. ( `tutorial.py` 참고)

### 1. requirements 설치
`pip install -r requirements.txt`


### 2. oauth client 인스턴스를 생성한다.

본인의 client_id, client_secret_id, redirect_uri를 넣어서 생성.  
(다른 uri들은 2022.02.24 기준 정상 작동)

```python
naver_client = OAuthClient(
    client_id="<your_client_id>",
    client_secret_id="<your_client_secret_id>",
    redirect_uri="<your_callback_uri>",
    authentication_uri="https://nid.naver.com/oauth2.0",
    resource_uri="https://openapi.naver.com/v1/nid/me",
    verify_uri="https://openapi.naver.com/v1/nid/verify",
)
```


### 3. 각 상황에 맞는 endpoint에 적용

```python
def get_authorization_token(authorization: str = Header(...)) -> str:
    """
    access or refresh token을 받기 위한 예제용 Depends 용 함수
    """
    scheme, _, param = authorization.partition(" ")
    if not authorization or scheme.lower() != "bearer":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return param

@app.get("/login")
async def login_naver(oauth_client=Depends(naver_client)):
    state = secrets.token_urlsafe(32) # 임의의 난수 토큰
    login_url = oauth_client.get_oauth_login_url(state=state)
    return RedirectResponse(login_url)


@app.get("/callback")
async def callback(
    code: str, state: Optional[str] = None, oauth_client=Depends(naver_client)
):
    token_response = await oauth_client.get_tokens(code, state)

    return {"response": token_response}


@app.get("/refresh")
async def callback(
    oauth_client=Depends(naver_client),
    refresh_token: str = Depends(get_authorization_token),
):
    token_response = await oauth_client.refresh_access_token(
        refresh_token=refresh_token
    )

    return {"response": token_response}


@app.get("/user", dependencies=[Depends(login_required)])
async def get_user(
    oauth_client=Depends(get_oauth_client),
    access_token: str = Depends(get_authorization_token),
):
    user_info = await oauth_client.get_user_info(access_token=access_token)
    return {"user": user_info}

```
