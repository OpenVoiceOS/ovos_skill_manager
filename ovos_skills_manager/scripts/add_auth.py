import click
from ovos_skills_manager import OVOSSkillsManager


APPSTORE_OPTIONS = ["neon"]


@click.command()
@click.option('--appstore', prompt='select appstore',
              type=click.Choice(APPSTORE_OPTIONS),
              help='add auth token for a specific appstore')
@click.option('--token', type=str,
              prompt='Auth Token',
              help='GitHub Personal Access Token')
def add_auth(appstore, token):
    osm = OVOSSkillsManager()
    osm.set_appstore_auth_token(appstore, token)
    prompt = f"Appstore token:\n{token}"
    click.echo(prompt)
    click.confirm('Save changes?', abort=True)
    osm.config.store()
    click.echo("changes saved!")


if __name__ == '__main__':
    add_auth()
