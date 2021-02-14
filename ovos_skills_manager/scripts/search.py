import click
from ovos_skills_manager import OVOSSkillsManager
from ovos_skills_manager.session import set_github_token

SEARCH_OPTIONS = ['all', 'name', 'url', 'category', 'author', 'tag',
                  'description']
APPSTORE_OPTIONS = ["ovos", "mycroft", "pling", "andlo", "neon", "default", "all"]


def search_skill(method, query, fuzzy, no_ignore_case, thresh, appstore):
    osm = OVOSSkillsManager()
    set_github_token(osm.appstores[appstore].get("auth_token"))

    ignore_case = not no_ignore_case
    thresh = thresh / 100

    if appstore == "all":
        for s in APPSTORE_OPTIONS:
            if s != "all" and s != "default":
                osm.enable_appstore(s)
    elif appstore != "default":
        for s in APPSTORE_OPTIONS:
            if s != appstore and s != "default" and s != "all":
                osm.disable_appstore(s)
        osm.enable_appstore(appstore)

    if method == "name":
        skills = [s for s in osm.search_skills_by_name(
            query, fuzzy=fuzzy, ignore_case=ignore_case, thresh=thresh)]
    elif method == "url":
        skills = [s for s in osm.search_skills_by_url(query)]
    elif method == "category":
        skills = [s for s in osm.search_skills_by_category(
            query, fuzzy=fuzzy, ignore_case=ignore_case, thresh=thresh)]
    elif method == "author":
        skills = [s for s in osm.search_skills_by_author(
            query, fuzzy=fuzzy, ignore_case=ignore_case, thresh=thresh)]
    elif method == "tag":
        skills = [s for s in osm.search_skills_by_tag(
            query, fuzzy=fuzzy, ignore_case=ignore_case, thresh=thresh)]
    elif method == "description":
        skills = [s for s in osm.search_skills_by_description(
            query, fuzzy=fuzzy, ignore_case=ignore_case, thresh=thresh)]
    else:
        skills = [s for s in osm.search_skills(
            query, fuzzy=fuzzy, ignore_case=ignore_case, thresh=thresh)]

    return skills


@click.command()
@click.option('--query', prompt='search term',
              help='Search a skill with this query')
@click.option('--method', default="all",  # case_sensitive=False,
              type=click.Choice(SEARCH_OPTIONS),
              help='match this metadata field when searching')
@click.option('--appstore', default="default",  # case_sensitive=False,
              type=click.Choice(APPSTORE_OPTIONS),
              help='search a specific appstore, by default searches '
                   'appstores enabled in config file')
@click.option('--fuzzy/--exact', default=True, help='exact or fuzzy matching')
@click.option('--thresh', type=click.IntRange(0, 100, clamp=True), default=80,
              help='fuzzy matching threshold from 0 (everything is a match) '
                   'to 100 (exact match)')
@click.option('--no-ignore-case', default=False, is_flag=True,
              help='ignore upper/lower case')
def search(method, query, fuzzy, no_ignore_case, thresh, appstore):
    skills = search_skill(method, query, fuzzy, no_ignore_case,
                          thresh, appstore)

    if not len(skills):
        click.echo("NO RESULTS")
    else:
        for s in skills:
            click.echo(s)


if __name__ == '__main__':
    search()
