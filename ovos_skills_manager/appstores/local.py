from ovos_skills_manager.skill_entry import SkillEntry
from ovos_skills_manager.appstores import AbstractAppstore
from ovos_skills_manager.licenses import parse_license_type
from ovos_skills_manager.github.utils import GITHUB_README_FILES, \
    GITHUB_ICON_FILES, GITHUB_JSON_FILES, GITHUB_DESKTOP_FILES, \
    GITHUB_LOGO_FILES, GITHUB_REQUIREMENTS_FILES, \
    GITHUB_SKILL_REQUIREMENTS_FILES, GITHUB_LICENSE_FILES, \
    GITHUB_MANIFEST_FILES, author_repo_from_github_url
from ovos_skills_manager.utils import readme_to_json
from ovos_utils.skills import get_skills_folder
from ovos_skills_manager.requirements import validate_manifest
from ovos_utils.json_helper import merge_dict
import json
from os import listdir, walk
from os.path import join, isdir, isfile


def get_local_skills(parse_github=False, skiplist=None):
    skills = get_skills_folder()
    skiplist = skiplist or []
    folders = listdir(skills)
    for fold in folders:
        path = join(skills, fold)
        if not isdir(path) or fold in skiplist:
            continue

        skill = {
            "appstore": "InstalledSkills",
            "appstore_url": skills,
            "skill_id": fold,
            "foldername": fold,
            "requirements": {"python": [], "system": [], "skill": []}
        }

        # if installed by msm/osm will obey this convention
        if "." in fold:
            try:
                repo, author = fold.split(".")
                skill["skillname"] = repo
                skill["authorname"] = author
                skill["url"] = f'https://github.com/{author}/{repo}'
            except: # TODO replace with some clever check ?
                pass

        # parse git info
        gitinfo = join(path, ".git/config")
        if isfile(gitinfo):
            with open(gitinfo) as f:
                for l in f.readlines():
                    if l.strip().startswith("url ="):
                        skill["url"] = l.split("url =")[-1].strip()
                        skill["authorname"], skill["skillname"] = \
                            author_repo_from_github_url(skill["url"])
                    if l.strip().startswith("[branch "):
                        skill["branch"] = l.split("branch")[-1]\
                            .replace('"', "").strip()

        for rtdir, foldrs, files in walk(join(skills, fold)):
            for f in files:
                if f in GITHUB_JSON_FILES:
                    with open(join(rtdir, f)) as fi:
                        skill_meta = json.load(fi)
                    skill = merge_dict(skill, skill_meta, merge_lists=True)
                elif f in GITHUB_README_FILES:
                    with open(join(rtdir, f)) as fi:
                        readme = readme_to_json(fi.read())
                    skill = merge_dict(skill, readme,
                                       new_only=True, merge_lists=True)
                elif f in GITHUB_DESKTOP_FILES:
                    skill['desktopFile'] = True
                elif f in GITHUB_ICON_FILES:
                    skill["icon"] = join(rtdir, f)
                elif f in GITHUB_LICENSE_FILES:
                    with open(join(rtdir, f)) as fi:
                        lic = fi.read()
                    skill["license"] = parse_license_type(lic)
                elif f in GITHUB_LOGO_FILES:
                    skill["logo"] = join(rtdir, f)
                elif f in GITHUB_MANIFEST_FILES:
                    with open(join(rtdir, f)) as fi:
                        manifest = validate_manifest(fi.read())
                    skill["requirements"]["python"] += manifest.get("python") or []
                    skill["requirements"]["system"] += manifest.get("system") or []
                    skill["requirements"]["skill"] += manifest.get("skill") or []
                elif f in GITHUB_REQUIREMENTS_FILES:
                    with open(join(rtdir, f)) as fi:
                        reqs = [r for r in fi.read().split("\n") if r.strip()]
                    skill["requirements"]["python"] += reqs
                elif f in GITHUB_SKILL_REQUIREMENTS_FILES:
                    with open(join(rtdir, f)) as fi:
                        reqs = [r for r in fi.read().split("\n") if r.strip()]
                    skill["requirements"]["skill"] += reqs
        yield SkillEntry.from_json(skill, parse_github=parse_github)


class InstalledSkills(AbstractAppstore):
    def __init__(self, *args, **kwargs):
        super().__init__("InstalledSkills", appstore_id="local",
                         *args, **kwargs)

    def get_skills_list(self, skiplist=None):
        skiplist = skiplist or []
        return get_local_skills(parse_github=self.parse_github,
                                skiplist=skiplist)
