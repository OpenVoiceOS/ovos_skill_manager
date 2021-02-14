import requests_cache
USER_AGENT = "OSM v0.0.X"
SESSION = requests_cache.CachedSession(expire_after=5 * 60, backend="memory")
SESSION.headers = {"User-Agent": USER_AGENT}


def set_github_token(token):
    global SESSION
    SESSION.headers["Authorization"] = f"token {token}"


def clear_github_token():
    global SESSION
    if "Authorization" in SESSION.headers:
        SESSION.headers.pop("Authorization")
