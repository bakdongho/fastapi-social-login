from urllib import parse
from typing import Optional
from wsgiref import headers

import aiohttp
import ssl
import certifi

from .exceptions import InvalidToken


class OAuthClient:
    def __init__(
        self, client_id, client_secret, redirect_uri, authentication_url, resource_url
    ):
        self._client_id = client_id
        self._client_secret = client_secret
        self._redirect_uri = redirect_uri
        self._authentication_url = authentication_url
        self._resource_url = resource_url
        self._header_name = "Authorization"
        self._header_type = "Bearer"

    def _get_connector_for_ssl(self):
        ssl_context = ssl.create_default_context(cafile=certifi.where())
        return aiohttp.TCPConnector(ssl=ssl_context)

    async def _request_for_token(self, payload):
        conn = self._get_connector_for_ssl()
        async with aiohttp.ClientSession(connector=conn) as session:
            async with session.post(
                f"{self._authentication_url}/token", data=payload
            ) as resp:
                return await resp.json()

    def _get_payload_for_tokens(self, code: str, state: str):
        return {
            "client_id": self._client_id,
            "client_secret": self._client_secret,
            "grant_type": "authorization_code",
            "code": code,
            "state": state,
        }

    def _get_headers_for_user_resource(self, access_token: str):
        return {
            self._header_name : f"{self._header_type} {access_token}"
        }

    async def _request_for_token(self, access_token):
        async with aiohttp.ClientSession() as session:
            async with session.get(
                self._resource_url, headers=self._get_headers_for_user_resource(access_token)
            ) as resp:
                return await resp.json()

    async def _get_user_data(self, access_token: str):
        pass

    async def get_user_data(self, access_token: str):
        pass

    async def get_tokens(self, code: str, state: str):
        payload = self._get_payload_for_tokens(code, state)
        resp = await self._request_for_token(payload)
        if resp.get("access_token") is None or resp.get("refresh_token") is None:
            raise InvalidToken("Tokens can't be None")

        return resp

    async def refresh_access_token(self, refresh_token: str):
        pass

    async def is_authenticated(self, access_token: str):
        pass

    def get_oauth_login_url(self, state: str):
        client_id = f"client_id={self._client_id}"
        redirect_uri = f"redirect_uri={parse.quote(self._redirect_uri, safe='')}"
        response_type = "response_type=code"
        state = f"state={state}"

        return f"{self._authentication_url}/authorize?{client_id}&{redirect_uri}&{response_type}&{state}".strip()
