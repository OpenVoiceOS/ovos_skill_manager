import json
from os.path import isfile, expanduser, join, isdir
from ovos_skills_manager.session import SESSION as requests
from ovos_skills_manager.exceptions import GithubInvalidUrl, \
    JSONDecodeError, GithubFileNotFound
from ovos_skills_manager.github import download_url_from_github_url, \
    get_branch, get_skill_data, get_requirements
from ovos_utils.json_helper import merge_dict
from ovos_utils.skills import blacklist_skill, whitelist_skill, \
    make_priority_skill, get_skills_folder
from ovos_skill_installer import install_skill
from ovos_skills_manager.requirements import install_system_deps, pip_install
from ovos_utils.log import LOG
from ovos_utils.enclosure import detect_enclosure
import shutil


class SkillEntry:
    def __init__(self, data=None):
        self._data = data or {}

    @property
    def uuid(self):
        # a unique identifier
        # github_repo.github_author , case insensitive
        # should be guaranteed to be unique
        author = self.skill_author.lower()
        repo = self.skill_folder.lower()
        return repo + "." + author

    @property
    def json(self):
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
                        raise GithubFileNotFound
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
                    github_data = get_skill_data(url, branch)
                    data = merge_dict(data, github_data, merge_lists=True,
                                      skip_empty=True, no_dupes=True)
                except GithubInvalidUrl as e:
                    raise e
        return SkillEntry(data)

    @staticmethod
    def from_github_url(url, branch=None):
        return SkillEntry.from_json({"url": url, "branch": branch}, True)

    # properties
    @property
    def url(self):
        return self.json.get("url")

    @property
    def appstore(self):
        return self.json.get("appstore") or "unknown"

    @property
    def skill_name(self):
        return self.json.get("skillname") or self.json.get("name")

    @property
    def skill_short_description(self):
        return self.json.get("short_description") or \
               self.skill_description.split(".")[0].split("\n")[0]

    @property
    def skill_description(self):
        return self.json.get("description") or self.skill_name

    @property
    def skill_folder(self):
        return self.json.get("foldername") or self.url.split("/")[-1]

    @property
    def skill_category(self):
        return self.json.get("category") or "VoiceApp"

    @property
    def skill_icon(self):
        # TODO bundle a default icon
        return self.json.get("icon") or "https://raw.githack.com/FortAwesome/Font-Awesome/master/svgs/solid/robot.svg"

    @property
    def skill_author(self):
        return self.json.get("authorname")

    @property
    def skill_tags(self):
        return self.json.get("tags", [])

    @property
    def skill_examples(self):
        return self.json.get("examples", [])

    @property
    def homescreen_msg(self):
        home_screen_msg = "{skill_folder}.{author}.home".lower()
        return home_screen_msg.format(skill_folder=self.skill_folder,
                                      author=self.skill_author)

    @property
    def branch(self):
        return self.json.get("branch") or get_branch(self.url)

    @property
    def branch_overrides(self):
        return self.json.get("branch_overrides") or {}

    @property
    def download_url(self):
        """ provided in .json file """
        return self.json.get("download_url") or \
               download_url_from_github_url(self.url, self.branch)

    @property
    def default_download_url(self):
        """ generated from github url directly"""
        return download_url_from_github_url(self.url, self.branch)

    @property
    def requirements(self):
        try:
            return self.json.get("requirements") or \
                   get_requirements(self.url, self.branch)
        except GithubFileNotFound:
            return {}

    @property
    def license(self):
        return self.json.get("license") or "unknown"

    @property
    def desktop_file(self):
        return self.generate_desktop_file()

    # generators
    def generate_desktop_json(self):
        return {'Terminal': 'false',
                'Type': 'Application',
                'Name': self.skill_name,
                'Exec': 'mycroft-gui-app --hideTextInput --skill' +
                        self.homescreen_msg,
                'Icon': self.skill_icon,
                'Categories': "VoiceApp",
                'StartupNotify': 'false',
                'X-DBUS-StartupType': 'None',
                'X-KDE-StartupNotify': 'false'}

    def generate_desktop_file(self):
        desktop_json = self.json.get("desktop") or self.generate_desktop_json()
        # icon renamed
        base_name = ".".join([self.skill_folder, self.skill_author]).lower()
        desktop_json["Icon"] = base_name + self.skill_icon.split(".")[-1]

        desktop_file = "[Desktop Entry]"
        for k in desktop_json:
            desktop_file += "\n" + k + "=" + desktop_json[k]
        return desktop_file

    def generate_readme(self):
        template = \
            """# <img src='{icon}' card_color='#000000' width='50' height='50' style='vertical-align:bottom'/> {title}
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
        if self.download_url.endswith(".tar.gz"):
            ext = "tar.gz"
        elif "zipball" in self.download_url:
            ext = "zip"
        else:
            ext = self.download_url.split(".")[-1]
        file = self.skill_folder + "." + ext
        url = self.download_url
        return install_skill(url, folder, file, session=requests,
                             skill_folder_name=self.uuid)

    def install(self, folder=None, default_branch="master", platform=None,
                update=True):
        if not update and self.is_previously_installed(folder):
            return False
        if self.branch_overrides:
            try:
                platform = platform or detect_enclosure()
            except Exception as e:
                LOG.error("Failed to detect platform")
                raise e
            if platform in self.branch_overrides:
                branch = self.branch_overrides[platform]
                if branch != self.branch:
                    LOG.info("Detected platform specific branch:" + branch)
                    skill = SkillEntry.from_github_url(self.url, branch)
                    return skill.install(folder, default_branch)

        LOG.info("Installing skill: {url} from branch: {branch}".format(
            url=self.url, branch=self.branch))
        skills = self.requirements.get("skill", [])
        if skills:
            LOG.info('Installing required skills')
        for s in skills:
            skill = SkillEntry.from_github_url(s)
            skill.install(folder, default_branch)

        system = self.requirements.get("system")
        if system:
            LOG.info('Installing system requirements')
            install_system_deps(system)

        pyth = self.requirements.get("python")
        if pyth:
            LOG.info('Running pip install')
            pip_install(pyth)

        LOG.info("Downloading " + self.url)
        updated = self.download(folder)
        if self.json.get("desktopFile"):
            LOG.info("Creating desktop entry")
            # TODO support system wide? /usr/local/XXX ?
            desktop_dir = expanduser("~/.local/share/applications")
            icon_dir = expanduser("~/.local/share/icons")

            # copy the files to a unique path, this way duplicate file names
            # dont overwrite each other, eg, several skills with "icon.png"
            base_name = ".".join([self.skill_folder, self.skill_author]).lower()

            # copy icon file
            icon_file = join(icon_dir,
                             base_name + self.skill_icon.split(".")[-1])
            if self.skill_icon.startswith("http"):
                content = requests.get(self.skill_icon).content
                with open(icon_file, "wb") as f:
                    f.write(content)
            elif isfile(self.skill_icon):
                shutil.copyfile(self.skill_icon, icon_file)

            # copy .desktop file
            desktop_file = join(desktop_dir, base_name + ".desktop")
            with open(desktop_file, "w") as f:
                f.write(self.desktop_file)

        return updated

    def update(self, folder=None, default_branch="master", platform=None):
        # convenience method
        return self.install(folder, default_branch, platform, update=True)

    def is_previously_installed(self, folder=None):
        folder = folder or get_skills_folder()
        return isdir(join(folder, self.uuid))

    def __repr__(self):
        return self.skill_name + " " + self.url
