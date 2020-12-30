from ovos_skills_manager.github import *
from ovos_skills_manager.utils import desktop_to_json, readme_to_json
from ovos_skills_manager.licenses import get_license_type, is_viral, \
    is_permissive
from ovos_utils.log import LOG
from ovos_utils.json_helper import merge_dict
import json
import yaml
from enum import Enum


# Manual Extraction
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
    GithubUrls.URL + readme for readme in GITHUB_README_FILES
]

GITHUB_LICENSE_LOCATIONS = [
    GithubUrls.URL + lic for lic in GITHUB_LICENSE_FILES
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
    # TODO solve rate limiting
    # for t in GithubUrls:
    #         def cache():
    #             try:
    #                 match_url_template(url, t, branch)
    #             except GithubInvalidUrl:
    #                 pass
    #             except Exception as e:
    #                 LOG.exception(e)
    #
    #         create_daemon(cache)
    return


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
    LOG.warning(
        "{url} contains an invalid manifest, attempting recovery".format(
            url=url))
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
        data = manif['dependencies'] or {"python": [], "system": {},
                                         "skill": []}
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


def get_skill_from_github_url(data, url, branch=None):
    # cache_repo_requests(url)  # speed up requests TODO avoid rate limit
    url = normalize_github_url(url)
    if not branch:
        try:
            branch = branch_from_github_url(url)
        except GithubInvalidBranch:
            pass
    if branch:
        data["branch"] = branch
    data["url"] = url
    data["skillname"] = skill_name_from_github_url(url)
    data["requirements"] = get_requirements_json_from_github_url(url, branch)
    data["download_url"] = download_url_from_github_url(url, branch)

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

    # branch should override branch from readme/json ?
    # i believe so because json in github might be outdated
    if branch:
        data["branch"] = branch

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
    if is_viral(data["license"]):
        data["tags"].append("viral-license")
    elif is_permissive(data["license"]):
        data["tags"].append("permissive-license")
    elif "unknown" in data["license"]:
        data["tags"].append("no-license")
    return data
