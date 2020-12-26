from ovos_skills_manager import Pling, MycroftMarketplace, AndloSkillList, OVOSstore

appstore = OVOSstore(parse_github=True)
#appstore.sync_skills_list(new_only=True)
total_skills = appstore.total_skills()
print(total_skills)
# 1

appstore = MycroftMarketplace(parse_github=True)
#appstore.sync_skills_list(new_only=True)
total_skills = appstore.total_skills()
print(total_skills)
# 77

appstore = Pling(parse_github=False)
#appstore.sync_skills_list(new_only=True)
total_skills = appstore.total_skills()
print(total_skills)
# 53

appstore = AndloSkillList(parse_github=True)
appstore.sync_skills_list(new_only=True)
total_skills = appstore.total_skills()
print(total_skills)
# 943
