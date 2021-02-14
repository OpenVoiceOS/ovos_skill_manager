import requests_cache

SESSION = requests_cache.CachedSession(expire_after=5 * 60, backend="memory")


def set_github_token(token):
    global SESSION
    SESSION.headers = {
        "Accept": "application/vnd.github.v3.raw",
        "Authorization": f"token {token}"
    }


def clear_github_token():
    global SESSION
    SESSION.headers = {}
