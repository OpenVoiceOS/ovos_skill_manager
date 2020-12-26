from ovos_skills_manager.exceptions import *
from ovos_skills_manager.utils import desktop_to_json, readme_to_json
from ovos_utils import camel_case_split, create_daemon
from ovos_utils.log import LOG
from ovos_utils.json_helper import merge_dict
from ovos_skills_manager.session import SESSION as requests
from ovos_skills_manager.licenses import get_license_type
import json
import yaml
from enum import Enum


class GithubUrls(str, Enum):
    URL = "https://github.com/{author}/{repo}"
    BRANCH = URL + "/tree/{branch}"
    README = URL + "/blob/{branch}/README.md"
    LICENSE = URL + "/blob/{branch}/LICENSE"
    SKILL_JSON = URL + "/blob/{branch}/res/desktop/skill.json"
    DESKTOP_FILE = URL + "/blob/{branch}/res/desktop/{repo}.desktop"
    ICON = URL + "/blob/{branch}/res/icon/{repo}.png"
    SKILL = URL + "/blob/{branch}/__init__.py"
    MANIFEST = URL + "/blob/{branch}/manifest.yml"
    REQUIREMENTS = URL + "/blob/{branch}/requirements.txt"
    SKILL_REQUIREMENTS = URL + "/blob/{branch}/skill_requirements.txt"
    DOWNLOAD = URL + "/archive/{branch}.zip"


GITHUB_README_LOCATIONS = [
    GithubUrls.URL + "/blob/{branch}/README",
    GithubUrls.URL + "/blob/{branch}/README.md",
    GithubUrls.URL + "/blob/{branch}/README.txt",
    GithubUrls.URL + "/blob/{branch}/README.rst",
    GithubUrls.URL + "/blob/{branch}/readme",
    GithubUrls.URL + "/blob/{branch}/readme.md",
    GithubUrls.URL + "/blob/{branch}/readme.rst",
    GithubUrls.URL + "/blob/{branch}/readme.txt",
    GithubUrls.URL + "/blob/{branch}/Readme",
    GithubUrls.URL + "/blob/{branch}/Readme.md",
    GithubUrls.URL + "/blob/{branch}/Readme.rst",
    GithubUrls.URL + "/blob/{branch}/Readme.txt"
]

GITHUB_LICENSE_LOCATIONS = [
    GithubUrls.URL + "/blob/{branch}/LICENSE",
    GithubUrls.URL + "/blob/{branch}/LICENSE.md",
    GithubUrls.URL + "/blob/{branch}/LICENSE.txt",
    GithubUrls.URL + "/blob/{branch}/License",
    GithubUrls.URL + "/blob/{branch}/License.md",
    GithubUrls.URL + "/blob/{branch}/License.txt",
    GithubUrls.URL + "/blob/{branch}/license",
    GithubUrls.URL + "/blob/{branch}/license.md",
    GithubUrls.URL + "/blob/{branch}/license.txt"
]

GITHUB_ICON_LOCATIONS = [
    GithubUrls.URL + "/blob/{branch}/res/icon/{repo}",
    GithubUrls.URL + "/blob/{branch}/res/icon/{repo}.png",
    GithubUrls.URL + "/blob/{branch}/res/icon/{repo}.svg",
    GithubUrls.URL + "/blob/{branch}/res/icon/{repo}.jpg"
]

GITHUB_JSON_LOCATIONS = [
    GithubUrls.URL + "/blob/{branch}/res/desktop/skill.json",
    GithubUrls.URL + "/blob/{branch}/skill.json"
]


# url utils
def normalize_github_url(url):
    url = url.replace("https://raw.githubusercontent.com",
                      "https://github.com").replace(".git", "")
    if not url.startswith("https://github.com/"):
        raise GithubInvalidUrl
    authorname, skillname = url.replace("https://github.com/", "").split("/")[
                            :2]
    return "/".join(["https://github.com", authorname, skillname])


def file_url_to_raw_github_url(url):
    if not url.startswith("https://github.com") and \
            not url.startswith("https://raw.githubusercontent.com"):
        raise GithubInvalidUrl
    url = url.replace("/blob", ""). \
        replace("https://github.com", "https://raw.githubusercontent.com")
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


def branch_from_github_url(url):
    if "/tree/" in url:
        branch = url.split("/tree/")[-1].split("/")[0]
    else:
        branch = "master"
    if validate_branch(branch, url):
        return branch
    raise GithubInvalidBranch


def validate_branch(branch, url):
    url = normalize_github_url(url) + "/tree/{branch}".format(branch=branch)
    return requests.get(url).status_code == 200


def validate_github_skill_url(url, branch=None):
    try:
        url = match_url_template(url, GithubUrls.SKILL, branch)
        data = requests.get(url).text

        if "def create_skill():" in data:
            return True
    except GithubInvalidUrl:
        pass
    raise GithubNotSkill


def is_valid_github_skill_url(url, branch=None):
    try:
        return validate_github_skill_url(url, branch)
    except GithubNotSkill:
        return False


def cache_repo_requests(url, branch=None):
    # this looks dumb, but offers a good speed up since this package uses
    # requests_cache
    for t in GithubUrls:
        def cache():
            try:
                match_url_template(url, t, branch)
            except GithubInvalidUrl:
                pass
            except Exception as e:
                LOG.exception(e)
        create_daemon(cache)


def match_url_template(url, template, branch=None):
    branch = branch or branch_from_github_url(url)
    author, repo = author_repo_from_github_url(url)
    url = template.format(author=author, branch=branch, repo=repo)
    if requests.get(url).status_code == 200:
        return file_url_to_raw_github_url(url)
    raise GithubInvalidUrl


# url getters
def json_url_from_github_url(url, branch=None):
    # try default github url
    for template in GITHUB_JSON_LOCATIONS:
        try:
            return match_url_template(url, template, branch)
        except GithubInvalidUrl:
            pass
    # try direct url
    try:
        return file_url_to_raw_github_url(url)
    except GithubInvalidUrl:
        if requests.get(url).status_code == 200:
            return url
    raise GithubJsonNotFound


def readme_url_from_github_url(url, branch=None):
    # try url from default github location
    for template in GITHUB_README_LOCATIONS:
        try:
            return match_url_template(url, template, branch)
        except GithubInvalidUrl:
            pass
    # try direct url
    try:
        return file_url_to_raw_github_url(url)
    except GithubInvalidUrl:
        if requests.get(url).status_code == 200:
            return url
    raise GithubReadmeNotFound


def desktop_url_from_github_url(url, branch=None):
    # try default github location
    try:
        return match_url_template(url, GithubUrls.DESKTOP_FILE, branch)
    except GithubInvalidUrl:
        pass

    # try direct url
    try:
        return file_url_to_raw_github_url(url)
    except GithubInvalidUrl:
        if requests.get(url).status_code == 200:
            return url
    raise GithubDesktopNotFound


def download_url_from_github_url(url, branch=None):
    # specific file
    try:
        return file_url_to_raw_github_url(url)
    except GithubInvalidUrl:
        pass
    # full git repo
    branch = branch or branch_from_github_url(url)
    author, repo = author_repo_from_github_url(url)
    url = GithubUrls.DOWNLOAD.format(author=author, branch=branch, repo=repo)
    if requests.get(url).status_code == 200:
        return url
    raise GithubInvalidUrl


def icon_url_from_github_url(url, branch=None):
    try:
        desktop = get_desktop_json_from_github_url(url, branch)
    except GithubDesktopNotFound:
        desktop = {}
    icon_file = desktop.get("Icon")
    if icon_file:
        return icon_file
    for template in GITHUB_ICON_LOCATIONS:
        try:
            return match_url_template(url, template, branch)
        except GithubInvalidUrl:
            pass

    raise GithubIconNotFound


def license_url_from_github_url(url, branch=None):
    # default github locations
    for template in GITHUB_LICENSE_LOCATIONS:
        try:
            return match_url_template(url, template, branch)
        except GithubInvalidUrl:
            pass
    # direct url
    try:
        return file_url_to_raw_github_url(url)
    except GithubInvalidUrl:
        pass
    raise GithubLicenseNotFound


def requirements_url_from_github_url(url, branch=None):
    # try default github url
    try:
        return match_url_template(url, GithubUrls.REQUIREMENTS, branch)
    except GithubInvalidUrl:
        raise GithubRequirementsNotFound


def skill_requirements_url_from_github_url(url, branch=None):
    # try default github url
    try:
        return match_url_template(url, GithubUrls.SKILL_REQUIREMENTS, branch)
    except GithubInvalidUrl:
        raise GithubSkillRequirementsNotFound


def manifest_url_from_github_url(url, branch=None):
    # try default github url
    try:
        return match_url_template(url, GithubUrls.MANIFEST, branch)
    except GithubInvalidUrl:
        raise GithubManifestNotFound


# data getters
def get_requirements_from_github_url(url, branch=None):
    url = requirements_url_from_github_url(url, branch)
    return [t for t in requests.get(url).text.split("\n")
            if t.strip() and not t.strip().startswith("#")]


def get_skill_requirements_from_github_url(url, branch=None):
    url = skill_requirements_url_from_github_url(url, branch)
    return [t for t in requests.get(url).text.split("\n")
            if t.strip() and not t.strip().startswith("#")]


def get_manifest_from_github_url(url, branch=None):
    url = manifest_url_from_github_url(url, branch)
    manifest = requests.get(url).text
    data = yaml.safe_load(manifest)
    if not data:
        # most likely just the template full of comments
        raise InvalidManifest
    if 'dependencies' in data:
        return data
    # some skills in the wild have the manifest without the top-level key
    LOG.warning("{url} contains an invalid manifest, attempting recovery".format(url=url))
    recovered = {"dependencies": {}}
    if "python" in data:
        recovered["dependencies"]["python"] = data["python"]
    if "skill" in data:
        recovered["dependencies"]["skill"] = data["skill"]
    if "system" in data:
        recovered["dependencies"]["system"] = data["system"]
    if not len(recovered["dependencies"]):
        # suspicious, doesn't follow standard
        raise InvalidManifest
    return recovered


def get_json_from_github_url(url, branch=None):
    branch = branch or branch_from_github_url(url)
    try:
        url = json_url_from_github_url(url, branch)
        url = file_url_to_raw_github_url(url)
    except GithubInvalidUrl:
        raise GithubJsonNotFound

    res = requests.get(url).text
    return json.loads(res)


def get_readme_from_github_url(url, branch=None):
    url = readme_url_from_github_url(url, branch)
    return requests.get(url).text


def get_license_from_github_url(url, branch=None):
    url = license_url_from_github_url(url, branch)
    return requests.get(url).text


def get_license_type_from_github_url(url, branch=None):
    license = get_license_from_github_url(url, branch).lower()
    return get_license_type(license)


def get_desktop_from_github_url(url, branch=None):
    url = desktop_url_from_github_url(url, branch)
    return requests.get(url).text


# data parsers
def get_desktop_json_from_github_url(url, branch=None):
    desktop = get_desktop_from_github_url(url, branch)
    return desktop_to_json(desktop)


def get_readme_json_from_github_url(url, branch=None):
    readme = get_readme_from_github_url(url, branch)
    return readme_to_json(readme)


def get_requirements_json_from_github_url(url, branch=None):
    data = {"python": [], "system": {}, "skill": []}
    try:
        manif = get_manifest_from_github_url(url, branch)
        data = manif['dependencies']
    except GithubManifestNotFound:
        pass
    try:
        req = get_requirements_from_github_url(url, branch)
        data["python"] = list(set(data["python"] + req))
    except GithubRequirementsNotFound:
        pass
    try:
        skill_req = get_skill_requirements_from_github_url(url, branch)
        data["skill"] = list(set(data["skill"] + skill_req))
    except GithubSkillRequirementsNotFound:
        pass
    return data


def parse_github_url(url, branch=None):
    # cache_repo_requests(url)  # speed up requests TODO avoid rate limit
    branch = branch or branch_from_github_url(url)
    url = normalize_github_url(url)
    author, repo = author_repo_from_github_url(url)

    data = {
        "authorname": author,
        "skillname": repo,
        "foldername": repo,
        "name": skill_name_from_github_url(url),
        "url": url,
        "branch": branch,
        "license": "unknown",
        "requirements": get_requirements_json_from_github_url(url, branch),
        "download_url": download_url_from_github_url(url, branch)
    }

    try:
        data["license"] = get_license_type_from_github_url(url, branch)
    except GithubLicenseNotFound:
        pass
    try:
        data["icon"] = icon_url_from_github_url(url, branch)
    except GithubIconNotFound:
        pass

    # augment with json data
    try:
        data = merge_dict(data, get_json_from_github_url(url, branch),
                          merge_lists=True, skip_empty=True, no_dupes=True)
    except GithubJsonNotFound:
        pass

    # augment with readme data
    try:
        data = merge_dict(data, get_readme_json_from_github_url(url, branch),
                          merge_lists=True, skip_empty=True, no_dupes=True)
    except GithubReadmeNotFound:
        pass

    # parse bigscreen flags
    if data["requirements"].get("system"):
        data['systemDeps'] = True
    else:
        data['systemDeps'] = False
    try:
        desktop = get_desktop_from_github_url(url, branch)
        data['desktopFile'] = True
    except GithubDesktopNotFound:
        data['desktopFile'] = False

    # augment tags
    if "tags" not in data:
        data["tags"] = []
    if "gpl" in data["license"]:
        data["tags"].append("viral-license")
    if "mit" in data["license"] or "apache" in data["license"]:
        data["tags"].append("permissive-license")
    if "unknown" in data["license"]:
        data["tags"].append("no-license")
    return data
