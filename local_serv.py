from flask import Flask, request
import config
from Oauth import exchanger

app = Flask(__name__)

@app.route('/oauth/callback/')
def oauth_callback():
    code = request.args.get('code')
    if code:
        exchanger(code)
        return f"Received authorization code: {code}"
    else:
        return "Authorization code not found", 400