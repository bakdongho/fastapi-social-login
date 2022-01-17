from urllib import parse
from typing import Optional


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

    def get_oauth_login_url(self, state: Optional[str] = None):
        client_id = f"client_id={self.client_id}"
        redirect_uri = parse.quote(self._redirect_uri, safe="")
        response_type = "response_type=code"
        state = f"&state={state}" if state else ""

        return f"{self._authentication_url}?{client_id}&{redirect_uri}&{response_type}&{state}"
