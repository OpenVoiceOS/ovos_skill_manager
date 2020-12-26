from ovos_skills_manager import Pling, OVOSstore
from pprint import pprint

appstore = OVOSstore()
skill = appstore.search_skills_by_name("skill-ddg")[0]
pprint(skill.as_json)
skill.install("my_skills_folder")


appstore = Pling()
skill = appstore.search_skills_by_name("skill-voip")[0]
pprint(skill.as_json)
skill.install("my_skills_folder")
