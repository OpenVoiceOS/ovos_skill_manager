import click
from ovos_skills_manager import OVOSSkillsManager
from pprint import pformat

APPSTORE_OPTIONS = ["ovos", "mycroft", "pling", "andlo", "neon", "all", "default"]


@click.command()
@click.option('--appstore', default="all",
              type=click.Choice(APPSTORE_OPTIONS),
              help='print config of a specific appstore')
def print_config(appstore):
    osm = OVOSSkillsManager()
    if appstore == "all":
        prompt = "Appstore configuration:\n" + pformat(osm.config["appstores"])
    elif appstore == "default":
        for k, s in list(osm.config["appstores"].items()):
            if not s["active"]:
                osm.config["appstores"].pop(k)
        prompt = "Active appstores configuration:\n" + \
                 pformat(osm.config["appstores"])
    else:
        name = osm.validate_appstore_name(appstore)
        prompt = appstore.title() + " configuration:\n" +\
                 pformat(osm.config["appstores"][name])
    click.echo(prompt)


if __name__ == '__main__':
    print_config()
