from ovos_skills_manager.appstores.pling import get_pling_skills
from ovos_skills_manager.appstores.mycroft_marketplace import get_mycroft_marketplace_skills
from ovos_skills_manager.appstores.andlo import get_andlos_list_skills
from ovos_skills_manager.appstores.ovos import get_ovos_skills
from pprint import pprint

for skill in get_pling_skills(parse_github=False):
    pprint(skill.skill_name)

exit()
for skill in get_ovos_skills():
    pprint(skill.json)

for skill in get_mycroft_marketplace_skills("20.08"):
    pprint(skill.json)



for skill in get_andlos_list_skills():
    pprint(skill.json)



