import click
from ovos_skills_manager import OVOSSkillsManager


APPSTORE_OPTIONS = ["ovos", "mycroft", "pling", "andlo", "neon", "default", "all"]


@click.command()
@click.option('--appstore', default="default",  # case_sensitive=False,
              type=click.Choice(APPSTORE_OPTIONS),
              help='sync a specific appstore, default syncs'
                   ' appstores enabled in config file')
@click.option('--rebuild', default=False, is_flag=True,
              help='rebuild skill database, if not set only sync data for new '
                   'skills')
@click.option('--merge', default=False, is_flag=True,
              help='merge skill data, if not set replaces skill entries')
@click.option('--github', default=False, is_flag=True,
              help='augment skill data from github, by default only saves '
                   'data provided directly by the appstore')
def sync(appstore, rebuild, merge, github):
    osm = OVOSSkillsManager()
    if github:
        click.echo("WARNING: parsing github can be VERY SLOW!")
        click.confirm('Are you sure you want to parse github?', abort=True)
        for k, s in list(osm.config["appstores"].items()):
            osm.config["appstores"][k]["parse_github"] = True

    if appstore == "all":
        for s in APPSTORE_OPTIONS:
            if s != "all" and s != "default":
                osm.enable_appstore(s)
    elif appstore != "default":
        for s in APPSTORE_OPTIONS:
            if s != appstore and s != "default" and s != "all":
                osm.disable_appstore(s)
        osm.enable_appstore(appstore)

    click.echo("Active appstores: " + ", ".join(osm.get_active_appstores()))
    osm.sync_appstores(new_only=not rebuild, merge=merge)


if __name__ == '__main__':
    sync()
