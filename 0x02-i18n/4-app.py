#!/usr/bin/env python3
"""
Basic Flask app with internationalization support.
"""
from flask import Flask, render_template, request
from flask_babel import Babel, _


class Config:
    """
    This is the configuration class for the flask application
    """
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


app = Flask(__name__)
app.config.from_object(Config)

babel = Babel(app)


@babel.localeselector
def get_locale() -> str:
    """
    Determine the best match for supported languages.
    """
    locale_param = request.args.get('locale')
    if locale_param in app.config['LANGUAGES']:
        return locale_param
    return request.accept_languages.best_match(app.config['LANGUAGES'])


@app.route('/')
def index() -> str:
    """
    renders the index page for the application
    """
    return render_template('4-index.html')


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
