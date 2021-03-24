from flask import (
    Blueprint,
    request,
    redirect,
    url_for,
    current_app,
    redirect,
    flash,
)
from flask_login import login_user
from .oauth2_client import (
    GoogleOAuth2Client,
    FacebookOAuth2Client,
)
from .models import User


bp = Blueprint('oauth2', __name__)


@bp.route('/google')
def login_with_google():
    request_uri = GoogleOAuth2Client.get_grant_request_url(
        client_id=current_app.config['GOOGLE_CLIENT_ID'],
        redirect_uri=url_for('oauth2.google_callback', _external=True),
        scope=['openid', 'email', 'profile']
    )
    return redirect(request_uri)


@bp.route('/facebook')
def login_with_facebook():
    request_uri = FacebookOAuth2Client.get_grant_request_url(
        client_id=current_app.config['FACEBOOK_CLIENT_ID'],
        redirect_uri=url_for('oauth2.facebook_callback', _external=True),
        scope=['email']
    )
    return redirect(request_uri)


@bp.route('/callback/google')
def google_callback():
    code = request.args.get('code', type=str)
    userinfo = GoogleOAuth2Client.get_userinfo(
        client_id=current_app.config['GOOGLE_CLIENT_ID'],
        client_secret=current_app.config['GOOGLE_CLIENT_SECRET'],
        code=code,
        authorization_response=request.url,
    )
    email = userinfo.get('email')
    user = User.query.filter_by(email=email).first()
    if not user:
        flash('You need to register this email before login')
        return redirect(url_for('main.register'))

    login_user(user)
    return redirect(url_for('main.home'))


@bp.route('/callback/facebook')
def facebook_callback():
    code = request.args.get('code', type=str)
    userinfo = FacebookOAuth2Client.get_userinfo(
        client_id=current_app.config['FACEBOOK_CLIENT_ID'],
        client_secret=current_app.config['FACEBOOK_CLIENT_SECRET'],
        code=code,
        authorization_response=request.url,
    )
    email = userinfo.get('email')
    user = User.query.filter_by(email=email).first()
    if not user:
        flash('You need to register this email before login')
        return redirect(url_for('main.register'))

    login_user(user)
    return redirect(url_for('main.home'))
