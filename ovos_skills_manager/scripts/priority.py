import click
from ovos_skills_manager import OVOSSkillsManager


APPSTORE_OPTIONS = ["ovos", "mycroft", "pling", "neon", "andlo"]


def priority(appstore, priority):
    osm = OVOSSkillsManager()
    osm.set_appstore_priority(appstore, priority)
    prompt = "Appstore priorities:\n"
    for k, s in osm.config["appstores"].items():
        prompt += k + " - " + str(s["priority"]) + "\n"
    click.echo(prompt)
    click.confirm('Save changes?', abort=True)
    osm.config.store()
    click.echo("changes saved!")


if __name__ == '__main__':
    priority()
