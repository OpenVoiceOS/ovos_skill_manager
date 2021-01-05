from ovos_skills_manager import Pling, MycroftMarketplace, AndloSkillList, OVOSstore

appstore = Pling(parse_github=True)
appstore.sync_skills_list(new_only=False)
total_skills = appstore.total_skills()
print(total_skills)
# 53

appstore = OVOSstore(parse_github=True)
appstore.sync_skills_list(new_only=False)
total_skills = appstore.total_skills()
print(total_skills)
# 3

appstore = MycroftMarketplace(parse_github=True)
appstore.sync_skills_list(new_only=False)
total_skills = appstore.total_skills()
print(total_skills)
# 77


appstore = AndloSkillList(parse_github=True)
appstore.sync_skills_list(new_only=False)
total_skills = appstore.total_skills()
print(total_skills)
# 939
