from ovos_skills_manager.github.api import get_skill_from_api
from ovos_skills_manager.github import get_skill_data
from pprint import pprint

url = "https://github.com/JarbasSkills/skill-ddg"
branch = "v0.1.0"

pprint(get_skill_data(url, branch))
"""
{'android': {'android_handler': 'skill-ddg.jarbasskills.home',
             'android_icon': 'https://raw.githubusercontent.com/JarbasSkills/skill-ddg/v0.1.0/res/icon/ddg.png',
             'android_name': 'Ddg Skill'},
 'authorname': 'JarbasSkills',
 'branch': 'v0.1.0',
 'categories': ['Information'],
 'category': 'Information',
 'description': 'Uses the [DuckDuckGo API](https://duckduckgo.com/api) to '
                'provide information. \n'
                '\n'
                'NOTE: this is meant a better alternative to the official duck '
                'duck go skill, it will be blacklisted',
 'desktopFile': True,
 'download_url': 'https://github.com/JarbasSkills/skill-ddg/archive/v0.1.0.zip',
 'examples': ['when was stephen hawking born',
              'tell me more',
              'continue',
              'ask the duck about the big bang',
              'who is elon musk'],
 'foldername': 'skill-ddg',
 'icon': 'https://raw.githubusercontent.com/JarbasSkills/skill-ddg/v0.1.0/res/icon/ddg.png',
 'license': 'apache-2.0',
 'logo': 'https://raw.githubusercontent.com/JarbasSkills/skill-ddg/v0.1.0/ui/logo.png',
 'name': 'DuckDuckGo',
 'platforms': ['arm', 'arm64', 'i386', 'x86_64', 'ia64'],
 'requirements': {'python': ['requests', 'google_trans_new', 'RAKEkeywords'],
                  'skill': [],
                  'system': {}},
 'short_description': 'Use DuckDuckGo to answer questions',
 'skillname': 'DuckDuckGo',
 'systemDeps': False,
 'tags': ['searchengine',
          'query',
          'duckduckgo',
          'Information',
          'search-engine',
          'permissive-license'],
 'url': 'https://github.com/JarbasSkills/skill-ddg'}
"""