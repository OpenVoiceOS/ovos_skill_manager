import requests_cache

SESSION = requests_cache.CachedSession(expire_after=5 * 60, backend="memory")
API_SESSION = requests_cache.CachedSession(expire_after=5 * 60,
                                           backend="memory")


def set_auth_token(token):
    global API_SESSION
    API_SESSION.headers = {
        "Accept": "application/vnd.github.v3.raw",
        "Authorization": f"token {token}"
    }
