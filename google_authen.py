import os
import requests
from flask import Flask, session, redirect, request, url_for
from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow
import google.auth.transport.requests

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = '1'

GOOGLE_CLIENT_ID = "***"

flow = Flow.from_client_secrets_file(
    client_secrets_file="client_secret.json",
    scopes=["https://www.googleapis.com/auth/userinfo.profile",
            "https://www.googleapis.com/auth/userinfo.email", "openid"],
    redirect_uri="https://bckwcs-5000.csb.app/callback"
)


def google_authen():
    authorization_url, state = flow.authorization_url()
    return redirect(authorization_url)


def callback():
    flow.fetch_token(authorization_response=request.url)

    # if not session["state"] == request.args["state"]:
    # abort(500)  # State does not match!

    credentials = flow.credentials

    request_session = requests.session()
    token_request = google.auth.transport.requests.Request(
        session=request_session)

    id_info = id_token.verify_oauth2_token(
        id_token=credentials._id_token,
        request=token_request,
        audience=GOOGLE_CLIENT_ID
    )

    session["role"] = "User"
    session["username"] = id_info.get("name")
    session['google'] = True
    session['logged_in'] = True

    return redirect(url_for('index'))
