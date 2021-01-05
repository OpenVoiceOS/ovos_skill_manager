from ovos_skills_manager.github.utils import normalize_github_url, \
    blob2raw, author_repo_from_github_url, \
    skill_name_from_github_url, get_branch_from_github_url, validate_branch, \
    download_url_from_github_url
from ovos_skills_manager.github.api import *
from ovos_skills_manager.github.raw import *
from ovos_skills_manager.exceptions import *
from ovos_skills_manager.utils import desktop_to_json, readme_to_json


# it's easy to get rate limited, but the api is significantly faster
# we should attempt using the api whenever possible and fallback to raw
# parsing when we don't have a choice


def get_skill_data(url, branch=None):
    author, repo = author_repo_from_github_url(url)
    branch = branch or get_branch(url)
    data = {
        "authorname": author,
        "foldername": repo,
        "url": normalize_github_url(url),
        "branch": branch,
        "license": "unknown",
        "tags": []
    }
    # augment with repo data
    try:
        api_data = get_repo_data(url)
        # only replace branch if not found by prev methods
        branch = branch or api_data['default_branch']
        data["branch"] = branch
        data["short_description"] = api_data['description']
        data["foldername"] = api_data["name"]
        data["last_updated"] = api_data['updated_at']
        data["url"] = api_data["html_url"]
        data["authorname"] = api_data["owner"]["login"]
        branch = branch or api_data['default_branch']
        if "license" in data:
            data["license"] = api_data["license"]["key"]
    except:
        pass

    # augment with releases data
    try:
        releases = get_releases(url)
        # search release that matches branch
        if branch:
            for r in releases:
                if r["name"] == branch or r["commit"]["sha"] == branch:
                    data["version"] = r["name"]
                    data["download_url"] = r["tarball_url"]
                    break
        # just pick latest release if branch not defined
        elif len(releases) > 0:
            data["version"] = data["branch"] = branch = releases[0]["name"]
            data["download_url"] = releases[0]["tarball_url"]
    except GithubSkillEntryError as e:
        pass

    # augment with readme data
    try:
        data = merge_dict(data, get_readme_json(url, branch),
                          merge_lists=True, skip_empty=True, no_dupes=True)
    except GithubSkillEntryError as e:
        pass

    # find logo
    try:
        data["logo"] = get_logo_url(url, branch)
    except GithubFileNotFound as e:
        pass

    # augment with requirements
    data["requirements"] = get_requirements_json(url, branch)

    # augment with android data
    data["android"] = get_android_json(url, branch)

    # augment with desktop data
    try:
        data["desktop"] = get_desktop_json(url, branch)
        data["desktopFile"] = True
    except GithubFileNotFound:
        data["desktopFile"] = False

    # augment tags
    if is_viral(data["license"]):
        data["tags"].append("viral-license")
    elif is_permissive(data["license"]):
        data["tags"].append("permissive-license")
    elif "unknown" in data["license"]:
        data["tags"].append("no-license")

    try:
        data["license"] = get_license_type(url, branch)
    except GithubLicenseNotFound:
        pass

    # augment with json data
    # this should take precedence over everything else
    try:
        data = merge_dict(data, get_skill_json(url, branch),
                          merge_lists=True, skip_empty=True, no_dupes=True)
    except GithubFileNotFound:
        pass

    return data


def get_branch(url):
    try:
        return get_branch_from_github_url(url)
    except GithubInvalidBranch:
        try:
            return get_branch_from_skill_json(url)
        except GithubFileNotFound:
            try:
                return get_branch_from_github_releases(url)
            except GithubAPIRateLimited:
                raise GithubInvalidBranch
            except:
                return get_branch_from_github_api(url)


def get_branch_from_github_releases(url, branch=None):
    try:
        return get_branch_from_skill_json_github_api(url, branch)
    except GithubAPIRateLimited:
        return get_branch_from_latest_release_github_url(url)


def get_branch_from_skill_json(url, branch=None):
    try:
        return get_branch_from_skill_json_github_api(url, branch)
    except GithubAPIRateLimited:
        return get_branch_from_skill_json_github_url(url)


def get_repo_data(url):
    try:
        return get_repo_data_from_github_api(url)
    except GithubAPIException:
        raise  # TODO raw approach


def get_releases(url):
    try:
        return get_repo_releases_from_github_api(url)
    except GithubAPIException:
        return get_repo_releases_from_github_url(url)


def get_latest_release(url):
    return get_releases(url)[0]


def get_file(url, filepath):
    try:
        return get_file_from_github_api(url, filepath)
    except GithubAPIException:
        raise  # TODO raw approach


# handle requirements info
def get_requirements_json(url, branch=None):
    data = {}
    try:
        manif = get_manifest(url, branch)
        data = manif['dependencies'] or {}
    except GithubSkillEntryError:
        pass
    data["python"] = data.get("python") or []
    data["skill"] = data.get("skill") or []
    data["system"] = data.get("system") or {}
    try:
        req = get_requirements(url, branch)
        data["python"] = list(set(data["python"] + req))
    except GithubSkillEntryError:
        pass
    try:
        skill_req = get_skill_requirements(url, branch)
        data["skill"] = list(set(data["skill"] + skill_req))
    except GithubSkillEntryError:
        pass
    return data


def get_manifest(url, branch=None):
    try:
        return get_manifest_from_github_api(url, branch)
    except GithubAPIException:
        return get_manifest_from_github_url(url, branch)


def get_requirements(url, branch=None):
    try:
        return get_requirements_from_github_api(url, branch)
    except GithubAPIException:
        return get_requirements_from_github_url(url, branch)


def get_skill_requirements(url, branch=None):
    try:
        return get_skill_requirements_from_github_api(url, branch)
    except GithubAPIException:
        return get_skill_requirements_from_github_url(url, branch)


# handle readme
def get_readme(url, branch=None):
    try:
        return get_readme_from_github_api(url, branch)
    except GithubAPIException:
        return get_readme_from_github_url(url, branch)


def get_readme_json(url, branch=None):
    readme = get_readme(url, branch)
    data = readme_to_json(readme)
    if data.get("icon", "").startswith("./"):
        data["icon"] = normalize_github_url(url) + data["icon"][1:]
    return data


def get_readme_url(url, branch=None):
    try:
        return get_readme_url_from_github_api(url, branch)
    except GithubAPIException:
        return get_readme_url_from_github_url(url, branch)


# handle license info
def get_license(url, branch=None):
    try:
        return get_license_from_github_api(url, branch)
    except GithubAPIException:
        return get_license_from_github_url(url, branch)


def get_license_data(url, branch=None):
    try:
        return get_license_data_from_github_api(url, branch)
    except GithubAPIException:
        return get_license_data_from_github_url(url, branch)


def get_license_type(url, branch=None):
    try:
        # we use the individual methods here instead of retrieving license
        # text and parsing it, that's because it should save a couple http
        # requests since license_type should be cached by get_repo_data
        return get_license_type_from_github_api(url, branch)
    except GithubAPIException:
        return get_license_type_from_github_url(url, branch)


def get_license_url(url, branch=None):
    try:
        return get_license_url_from_github_api(url, branch)
    except GithubAPIException:
        return get_license_url_from_github_url(url, branch)


# handle .json info
def get_skill_json(url, branch=None):
    try:
        return get_skill_json_from_github_api(url, branch)
    except GithubAPIException:
        return get_skill_json_from_github_url(url, branch)


def get_skill_json_url(url, branch=None):
    try:
        return get_json_url_from_github_api(url, branch)
    except GithubAPIException:
        return get_json_url_from_github_url(url, branch)


# handle .desktop info
def get_desktop(url, branch=None):
    try:
        return get_desktop_from_github_api(url, branch)
    except GithubAPIException:
        return get_desktop_from_github_url(url, branch)


def get_desktop_json(url, branch=None):
    desktop = get_desktop(url, branch)
    return desktop_to_json(desktop)


def get_desktop_url(url, branch=None):
    try:
        return get_desktop_url_from_github_api(url, branch)
    except GithubAPIException:
        return get_desktop_url_from_github_url(url, branch)


# handle icon
def get_icon(url, branch=None):
    try:
        return get_icon_url_from_github_api(url, branch)
    except GithubAPIException:
        return get_icon_url_from_github_url(url, branch)


# handle logo
def get_logo_url(url, branch=None):
    try:
        return get_logo_url_from_github_api(url, branch)
    except GithubAPIException:
        return get_logo_url_from_github_url(url, branch)


# handle android
def get_android_url(url, branch=None):
    try:
        return get_android_url_from_github_api(url, branch)
    except GithubAPIException:
        return get_android_url_from_github_url(url, branch)


def get_android_json(url, branch=None):
    try:
        return get_android_json_from_github_api(url, branch)
    except GithubAPIException:
        return get_android_json_from_github_url(url, branch)
