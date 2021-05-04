import click
from ovos_skills_manager import OVOSSkillsManager

APPSTORE_OPTIONS = ["neon"]

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
