from ovos_skills_manager.github.api import get_readme_from_github_api
from ovos_skills_manager.utils import readme_to_json
from pprint import pprint

# from github url
url = "https://github.com/JarbasSkills/skill-wolfie"



## Non standard readmes  (mycroft)
url = "https://github.com/padresb/bark-skill"
url = "https://github.com/austin-carnahan/days-in-history-skill"
url = "https://github.com/brezuicabogdan/myepisodes-skill"


## Non standard readmes  (pling)

url = "https://github.com/JarbasSkills/skill-better-playback-control"


## Non standard readmes  (andlo)
readme = get_readme_from_github_api(url)
pprint(readme)
pprint(readme_to_json(readme))
