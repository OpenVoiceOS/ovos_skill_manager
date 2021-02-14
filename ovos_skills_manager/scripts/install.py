import click
from ovos_skills_manager import SkillEntry, OVOSSkillsManager
from ovos_skills_manager.session import set_github_token

SEARCH_OPTIONS = ['all', 'name', 'url', 'category', 'author', 'tag',
                  'description']
APPSTORE_OPTIONS = ["ovos", "mycroft", "pling", "andlo", "neon", "default", "all"]


def search_skill(method, query, fuzzy, no_ignore_case, thresh, appstore):
    osm = OVOSSkillsManager()

    ignore_case = not no_ignore_case
    thresh = thresh / 100

    if appstore == "all":
        for s in APPSTORE_OPTIONS:
            if s != "all" and s != "default":
                osm.enable_appstore(s)
    elif appstore != "default":
        for s in APPSTORE_OPTIONS:
            if s != appstore and s != "default" and s!= "all":
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
@click.option('--skill', prompt='skill to install (url or search term)',
              help='skill to install')
@click.option('--branch', type=str,
              help='select skill github branch to use')
@click.option('--folder', type=str, default="/opt/mycroft/skills",
              help='path where skill will be installed, default /opt/mycroft/skills')
@click.option('--search', default=False, is_flag=True,
              help="search appstores, otherwise assume it's a github url")
@click.option('--appstore', default="default",  # case_sensitive=False,
              type=click.Choice(APPSTORE_OPTIONS),
              help='search a specific appstore, default search '
                   'appstores enabled in config file')
@click.option('--method', default="all",  # case_sensitive=False,
              type=click.Choice(SEARCH_OPTIONS),
              help='match this metadata field when searching')
@click.option('--fuzzy/--exact', default=True,
              help='exact or fuzzy matching, default fuzzy')
@click.option('--thresh', type=click.IntRange(0, 100, clamp=True), default=80,
              help='fuzzy matching threshold from 0 (everything is a match) '
                   'to 100 (exact match),  default 80')
@click.option('--no-ignore-case', default=False, is_flag=True,
              help='ignore upper/lower case, default ignore')
def install(method, skill, fuzzy, no_ignore_case, thresh, appstore, search,
            branch, folder):
    set_github_token(OVOSSkillsManager().appstores[appstore].get("auth_token"))
    if search:
        skills = search_skill(method, skill, fuzzy, no_ignore_case,
                              thresh, appstore)
    elif not skill.startswith("http"):
        click.confirm('{s} does not look like a valid skill url, do you '
                      'want to enable search?'.format(s=skill),
                      abort=True)
        skills = search_skill(method, skill, fuzzy, no_ignore_case,
                              thresh, appstore)
    else:
        skills = [SkillEntry.from_github_url(skill, branch)]

    if not len(skills):
        click.echo("NO RESULTS")
    else:
        # ask option
        prompt = "\nSearch Results:\n    appstore - branch - url \n"
        opts = {}
        for s in skills:
            idx = len(opts) + 1
            prompt += str(idx) + " - " + s.appstore + " - " + s.branch + " " +\
                      s.url + "\n"
            opts[idx] = s
        prompt += "0 - cancel installation\n"
        def ask_selection():
            click.echo(prompt)
            value = click.prompt('Select an option', type=int)
            if value < 0 or value > len(opts):
                click.echo("Invalid choice")
                return ask_selection()
            return value

        value = ask_selection()
        if value == 0:
            click.echo("Installation cancelled")
            return
        skill = opts[value]
        skill_str = skill.branch + " " + skill.url
        click.confirm('Do you want to install {s} ?'.format(s=skill_str),
                      abort=True)
        skill.install(folder)


if __name__ == '__main__':
    install()
