import json
from os.path import isfile
from ovos_skills_manager.session import SESSION as requests
from ovos_skills_manager.exceptions import GithubInvalidUrl, \
    JSONDecodeError, GithubJsonNotFound, GithubInvalidBranch
from ovos_skills_manager.github import parse_github_url, \
    download_url_from_github_url, get_requirements_json_from_github_url, \
    branch_from_github_url
from ovos_utils.json_helper import merge_dict
from ovos_utils.skills import blacklist_skill, whitelist_skill, \
    make_priority_skill, get_skills_folder
from ovos_skill_installer import install_skill
from ovos_skills_manager.requirements import install_system_deps, pip_install
from ovos_utils.log import LOG


class SkillEntry:
    def __init__(self, data=None):
        self._data = data or {}

    @property
    def as_json(self):
        return self._data

    # constructors
    @staticmethod
    def from_json(data, parse_github=True):
        if isinstance(data, str):
            if data.startswith("http"):
                url = data
                if "github" in url:
                    # url parsed in github info step bellow
                    data = {"url": url}
                else:
                    try:
                        res = requests.get(url).text
                        data = json.loads(res)
                    except JSONDecodeError:
                        raise GithubJsonNotFound
            elif isfile(data):
                with open(data) as f:
                    data = json.load(f)
            else:
                data = json.loads(data)

        if not isinstance(data, dict):
            # TODO new exception
            raise ValueError("unrecognized format")

        # augment with github info
        if parse_github:
            url = data.get("url", "")
            if "github" in url:
                branch = data.get("branch")
                try:
                    github_data = parse_github_url(url, branch)
                    data = merge_dict(data, github_data, merge_lists=True,
                                      skip_empty=True, no_dupes=True)
                except GithubInvalidUrl as e:
                    raise e
        return SkillEntry(data)

    @staticmethod
    def from_github_url(url, branch=None):
        data = parse_github_url(url, branch)
        return SkillEntry.from_json(data, False)

    # properties
    @property
    def url(self):
        return self.as_json.get("url")

    @property
    def skill_name(self):
        return self.as_json.get("skillname") or self.as_json.get("name")

    @property
    def skill_short_description(self):
        return self.as_json.get("short_description") or \
               self.skill_description.split(".")[0].split("\n")[0]

    @property
    def skill_description(self):
        return self.as_json.get("description") or self.skill_name

    @property
    def skill_folder(self):
        return self.as_json.get("foldername") or self.url.split("/")[-1]

    @property
    def skill_category(self):
        return self.as_json.get("category") or "VoiceApp"

    @property
    def skill_icon(self):
        # TODO bundle a default icon
        return self.as_json.get("icon") or "https://raw.githack.com/FortAwesome/Font-Awesome/master/svgs/solid/robot.svg"

    @property
    def skill_author(self):
        return self.as_json.get("authorname")

    @property
    def skill_tags(self):
        return self.as_json.get("tags", [])

    @property
    def skill_examples(self):
        return self.as_json.get("examples", [])

    @property
    def homescreen_msg(self):
        home_screen_msg = "{skill_folder}.{author}.home"
        return home_screen_msg.format(skill_folder=self.skill_folder,
                                      author=self.skill_author)

    @property
    def branch(self):
        return self.as_json.get("branch")

    @property
    def download_url(self):
        return self.as_json.get("download_url") or \
               download_url_from_github_url(self.url, self.branch)

    @property
    def requirements(self):
        return self.as_json.get("requirements") or \
               get_requirements_json_from_github_url(self.url, self.branch)

    @property
    def license(self):
        return self.as_json.get("license") or "unknown"

    # generators
    def generate_desktop_json(self):
        return {'Terminal': 'false',
                'Type': 'Application',
                'Name': self.skill_name,
                'Exec': 'mycroft-gui-app --hideTextInput --skill' +
                        self.homescreen_msg,
                'Icon': self.skill_icon,
                'Categories': self.skill_category,
                'StartupNotify': 'false',
                'X-DBUS-StartupType': 'None',
                'X-KDE-StartupNotify': 'false'}

    def generate_desktop_file(self):
        data = self.generate_desktop_json()
        desktop_file = "[Desktop Entry]"
        for k in data:
            desktop_file += "\n" + k + "=" + data[k]
        return desktop_file

    def generate_readme(self):
        template = """# <img src='{icon}' card_color='#000000' width='50' height='50' style='vertical-align:bottom'/> {title}
{one_liner}

## About
{description}

## Examples
{examples}

## Credits
{author}

## Category
{category}

## Tags
{tags}
"""
        return template.format(title=self.skill_name,
                               description=self.skill_description,
                               category="**" + self.skill_category + "**",
                               author=self.skill_author,
                               icon=self.skill_icon,
                               one_liner=self.skill_short_description,
                               examples="\n* " + "\n* ".join(self.skill_examples),
                               tags=" ".join(["#" + t for t in self.skill_tags]))

    # actions
    def blacklist(self):
        blacklist_skill(self.skill_folder)

    def whitelist(self):
        whitelist_skill(self.skill_folder)

    def make_priority(self):
        make_priority_skill(self.skill_folder)

    def download(self, folder=None):
        folder = folder or get_skills_folder()
        file = self.skill_folder + "." + self.download_url.split(".")[-1]
        return install_skill(self.download_url, folder, file)

    def install(self, folder=None, default_branch="master"):
        LOG.info("Installing skill: {url} from branch: {branch}".format(
            url=self.url, branch=self.branch))
        skills = self.requirements.get("skill", [])
        if skills:
            LOG.info('Installing required skills')
        for s in skills:
            try:
                branch = branch_from_github_url(s)
            except GithubInvalidBranch:
                LOG.warning("skill branch not specified for {skill}, "
                            "falling back to '{branch}'".
                            format(branch=default_branch, skill=s))
                branch = default_branch
            skill = SkillEntry.from_github_url(s, branch)
            skill.install(folder)

        system = self.requirements.get("system")
        if system:
            LOG.info('Installing system requirements')
            install_system_deps(system)

        pyth = self.requirements.get("python")
        if pyth:
            LOG.info('Running pip install')
            pip_install(pyth)

        LOG.info("Downloading " + self.url)
        return self.download(folder)

    def update(self, folder=None):
        # convenience method
        return self.install(folder)
