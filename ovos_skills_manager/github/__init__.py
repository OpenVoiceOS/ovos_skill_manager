from ovos_skills_manager.exceptions import *
from ovos_utils import camel_case_split
from ovos_skills_manager.session import SESSION as requests

GITHUB_README_FILES = ["README", "README.md", "README.txt", "README.rst",
                       "readme", "readme.md", "readme.rst", "readme.txt",
                       "Readme", "Readme.md", "Readme.rst", "Readme.txt"
                       ]

GITHUB_LICENSE_FILES = ["LICENSE", "LICENSE.txt", "UNLICENSE",
                        "LICENSE.md", "License", "License.md",
                        "License.txt", "license", "license.md", "license.txt"
                        ]

GITHUB_ICON_FILES = ["res/icon/{repo}", "res/icon/{repo}.png",
                     "res/icon/{repo}.svg", "res/icon/{repo}.jpg"]
GITHUB_JSON_FILES = ["res/desktop/skill.json", "skill.json"]
GITHUB_DESKTOP_FILES = ["res/desktop/{repo}.desktop", "{repo}.desktop"]
GITHUB_MANIFEST_FILES = ["manifest.yml"]
GITHUB_REQUIREMENTS_FILES = ["requirements.txt"]
GITHUB_SKILL_REQUIREMENTS_FILES = ["skill_requirements.txt"]
GITHUB_REQUIREMENTS_SCRIPT_FILES = ["requirements.sh"]
GITHUB_SKILL_INIT_FILES = ["__init__.py"]


# url utils
def normalize_github_url(url):
    url = url.replace("https://raw.githubusercontent.com",
                      "https://github.com").replace(".git", "")
    if not url.startswith("https://github.com/"):
        raise GithubInvalidUrl
    author, skillname = url.replace("https://github.com/", "").split("/")[:2]
    return "/".join(["https://github.com", author, skillname])


def file_url_to_raw_github_url(url, validate=False):
    if not url.startswith("https://github.com") and \
            not url.startswith("https://raw.githubusercontent.com"):
        raise GithubInvalidUrl
    url = url.replace("/blob", ""). \
        replace("https://github.com", "https://raw.githubusercontent.com")
    if validate:
        if requests.get(url).status_code != 200:
            raise GithubRawUrlNotFound
    return url


def author_repo_from_github_url(url):
    url = normalize_github_url(url)
    return url.split("/")[-2:]


def skill_name_from_github_url(url):
    _, repo = author_repo_from_github_url(url)
    words = camel_case_split(repo.replace("-", " ").lower()).split(" ")
    name = " ".join([w for w in words if w != "skill"]) + " skill"
    return name.title()


def branch_from_github_url(url, validate=False):
    branch = None
    if "/tree/" in url:
        branch = url.split("/tree/")[-1].split("/")[0]

    if branch:
        if validate:
            if not validate_branch(branch, url):
                raise GithubInvalidBranch
        return branch
    else:
        raise GithubInvalidBranch


def validate_branch(branch, url):
    url = normalize_github_url(url) + "/tree/{branch}".format(branch=branch)
    return requests.get(url).status_code == 200


def parse_github_url(url, branch=None):
    author, repo = author_repo_from_github_url(url)
    data = {
        "authorname": author,
        "foldername": repo,
        "url": url,
        "branch": branch,
        "license": "unknown"
    }
    return data
