from click import echo
from ovos_skills_manager import OVOSSkillsManager

def echo_version():
    osm = OVOSSkillsManager()
    echo(osm.config.get('version'))