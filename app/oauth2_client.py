import json
from urllib.parse import urlparse

import requests
from oauthlib.oauth2 import WebApplicationClient


class OAuth2Client:
    provider = None

    token_endpoint = None

    userinfo_endpoint = None

    authorization_endpoint = None

    @classmethod
    def get_grant_request_url(
        cls, client_id, redirect_uri, scope=None, state=None
    ):
        oauth_client = WebApplicationClient(client_id)
        request_uri = oauth_client.prepare_request_uri(
            cls.authorization_endpoint,
            redirect_uri=redirect_uri,
            scope=scope,
            state=json.dumps(state) if state else None,
        )

        return request_uri

    @classmethod
    def get_userinfo(
        cls, client_id, client_secret, code, authorization_response
    ):
        client = WebApplicationClient(client_id)

        base_url = authorization_response.replace(
            "?" + urlparse(authorization_response).query, ""
        )

        # get access token
        token_url, headers, body = client.prepare_token_request(
            cls.token_endpoint,
            authorization_response=authorization_response,
            redirect_url=base_url,
            code=code,
        )
        token_response = requests.post(
            token_url,
            headers=headers,
            data=body,
            auth=(client_id, client_secret),
        )
        client.parse_request_body_response(token_response.text)

        # get user information
        uri, headers, body = client.add_token(cls.userinfo_endpoint)
        userinfo_response = requests.get(uri, headers=headers, data=body)
        data = userinfo_response.json()

        return data


class GoogleOAuth2Client(OAuth2Client):
    token_endpoint = "https://oauth2.googleapis.com/token"

    userinfo_endpoint = "https://openidconnect.googleapis.com/v1/userinfo"

    authorization_endpoint = "https://accounts.google.com/o/oauth2/v2/auth"


class FacebookOAuth2Client(OAuth2Client):
    token_endpoint = "https://graph.facebook.com/v10.0/oauth/access_token"

    userinfo_endpoint = "https://graph.facebook.com/v10.0/me?fields=name,email"

    authorization_endpoint = "https://www.facebook.com/v10.0/dialog/oauth"
