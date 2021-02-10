import click
from ovos_skills_manager import OVOSSkillsManager


APPSTORE_OPTIONS = ["ovos", "mycroft", "pling", "neon", "andlo"]


@click.command()
@click.option('--appstore', prompt='select appstore',
              type=click.Choice(APPSTORE_OPTIONS),
              help='change priority of a specific appstore')
@click.option('--priority', type=click.IntRange(0, 100, clamp=True),
              prompt='new appstore priority',
              help='appstore priority, from 0 (highest) to 100 (lowest)')
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
