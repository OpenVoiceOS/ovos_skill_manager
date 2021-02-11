from json_database import JsonStorageXDG

from ovos_skills_manager.skill_entry import SkillEntry
from ovos_skills_manager.appstores import AbstractAppstore
import json
import requests


def get_neon_skills(parse_github=False, skiplist=None, token=None):
    skiplist = skiplist or []
    skills_url = "https://api.github.com/repos/NeonGeckoCom/neon-skills-submodules/contents/skill-metadata.json"
    skill_json = json.loads(requests.get(skills_url, headers={"Authorization": f"token {token}",
                                                              "Accept": "application/vnd.github.v3.raw"}).text)
    for skill in skill_json.values():
        if skill["url"] in skiplist:
            continue
        skill["appstore"] = "Neon"
        skill["appstore_url"] = skills_url
        yield SkillEntry.from_json(skill,
                                   parse_github=parse_github)


class NeonSkills(AbstractAppstore):
    def __init__(self, parse_github=False):
        super().__init__("Neon", parse_github, self.get_auth())

    def get_skills_list(self, skiplist=None):
        skiplist = skiplist or []
        return get_neon_skills(parse_github=self.parse_github,
                               skiplist=skiplist, token=self.auth_token)

    @staticmethod
    def get_auth():
        """
        Gets the github auth token
        """
        config = JsonStorageXDG("OVOS-SkillsManager")
        token = config["appstores"]["neon"].get("token")
        return token
