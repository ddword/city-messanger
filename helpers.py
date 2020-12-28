import requests
import urllib.parse

from datetime import datetime
from flask import redirect, render_template, request, session
from functools import wraps


def apology(message, code=400):
    """Render message as an apology to user."""

    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s

    return render_template("apology.html", top=code, bottom=escape(message)), code


def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/1.0/patterns/viewdecorators/
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)

    return decorated_function


def get_GPS(city, address):
    '''Contact API nominatim of openstreetmap, example
        https://nominatim.openstreetmap.org/search?q=135+pilkington+avenue,+birmingham&format=json&polygon=1&addressdetails=1
    '''
    try:
        response = requests.get(f"https://nominatim.openstreetmap.org/search?q="
                                f"{urllib.parse.quote_plus(address)},+{urllib.parse.quote_plus(city)}"
                                f"&format=json&polygon=1&addressdetails=1")
        response.raise_for_status()
    except requests.RequestException:
        return None

    # Parse response
    try:
        res = response.json()
        # print(f'GPS coordinates{res}')

        if not res:
            return 0
        return {
            "lat": res[0].get('lat'),
            "lon": res[0].get('lon'),
            "address": res[0].get('display_name'),
        }

    except (KeyError, TypeError, ValueError):
        return None


def get_time():
    now = datetime.now()
    return now.strftime('%Y-%m-%d %H:%M:%S UTC')
