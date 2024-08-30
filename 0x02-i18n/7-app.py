#!/usr/bin/env python3
"""
Basic Flask app with internationalization support.
"""
from flask import Flask, render_template, request, g
from flask_babel import Babel
import pytz
from pytz.exceptions import UnknownTimeZoneError


class Config:
    """
    This is the configuration class
    """
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


app = Flask(__name__)
app.config.from_object(Config)

babel = Babel(app)


users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


def get_user():
    """
    Return the user dictionary or None if login_as was not passed
    or ID is not found.
    """
    user_id = request.args.get('login_as')
    if user_id and user_id.isdigit():
        user_id = int(user_id)
        return users.get(user_id)
    return None


@app.before_request
def before_request():
    """Before request handler to set the user in flask.g."""
    g.user = get_user()


@babel.localeselector
def get_locale() -> str:
    """
    Determine the best match for supported languages.
    """
    locale_param = request.args.get('locale')
    if locale_param in app.config['LANGUAGES']:
        return locale_param

    if g.user and g.user.get('locale') in app.config['LANGUAGES']:
        return g.user['locale']

    return request.accept_languages.best_match(app.config['LANGUAGES'])


@babel.timezoneselector
def get_timezone() -> str:
    timezone_param = request.args.get('timezone')
    if timezone_param:
        try:
            # Validate the timezone
            pytz.timezone(timezone_param)
            return timezone_param
        except UnknownTimeZoneError:
            # If the timezone is not valid, fall through to the next options
            pass
    if g.user and g.user.get('timezone'):
        try:
            # Validate the timezone
            pytz.timezone(g.user['timezone'])
            return g.user['timezone']
        except UnknownTimeZoneError:
            # If the timezone is not valid, fall through to the next options
            pass
    return 'UTC'
 

@app.route('/')
def index() -> str:
    """
    renders the index page
    """
    return render_template('7-index.html')


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
