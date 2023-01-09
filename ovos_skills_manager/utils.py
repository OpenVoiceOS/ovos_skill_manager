import json
import os.path

import requests

from typing import Union, List
from os import listdir, path
from os.path import isdir, isfile, join, expanduser
from random import shuffle
from distutils.version import StrictVersion

from ovos_utils.log import LOG
from ovos_utils.skills.locations import get_plugin_skills, get_skill_directories

from ovos_skills_manager.session import SESSION


def parse_python_dependencies(python_deps: list, token: str = None) -> list:
    """
    Parses a dependencies dict to resolve any conflicts, perform any formatting, add authentication, etc.
    :param python_deps: list of python dependencies to be passed to pip
    :param token: Optional Github token to authorize access to private repositories hosting dependencies
    :return: list of parsed dependencies
    """
    # Handle case sensitivity in dependencies and any potentially required auth
    for i in range(0, len(python_deps)):
        r = python_deps[i]
        if "@" in r:  # Handle dependencies like: `neon_utils @ git+https://github.com/NeonGeckoCom/neon-skill-utils
            parts = [p.lower() if p.strip().startswith("git+http") else p for p in r.split('@')]
            r = "@".join(parts)
        if token:  # Add a passed github token into the dependency URL
            if "github.com" in r:
                r = r.replace("github.com", f"{token}@github.com")
        python_deps[i] = r
    return python_deps


def readme_to_json(text: str) -> dict:
    """Accepts a README file as a str, and returns a dict representing valid JSON about a skill
    """
    text = text.replace("\r", "").replace("\t", "") + "\n## "  # marker to
    # end parsing
    data = {}
    current_section = "title"
    current_text = ""
    current_items = []
    for line in text.split("\n"):
        if line.startswith("# ") and current_section == "title":
            current_text = line.split("# ")[-1].replace("\\", "").replace('"', "'")
            # can be <img src=' or <img src=\' or <img src=\"
            icon_start = "<img src='"
            icon_end = "'"
            if current_text.startswith(icon_start):
                icon = current_text.split(icon_start)[-1].split(icon_end)[0]
                data["icon"] = icon
                current_text = current_text.split("/>")[-1]
            data["skillname"] = current_text.split(">")[-1].strip()
            current_section = "short_description"
            current_text = ""
        elif line.startswith("## ") or line.startswith("# "):
            line = line.replace("##", "#")
            if current_section == "About" or\
                    current_section == "short_description":
                data["description"] = current_text.strip()
                if current_items:
                    data["description"] += "\n" + "\n * ".join(current_items)
                if current_section == "short_description":
                    data["short_description"] = current_text.strip().split("\n")[0]
            elif current_section == "Usage" or current_section == "Examples"\
                    or current_section == "Intents":
                data["examples"] = current_items
            elif current_section == "Credits":
                if not current_items:
                    current_items = [current_text.strip()]
                data["credits"] = current_items
            elif current_section == "Category":
                cats = [c.strip() for c in
                        current_text.replace("*", "").split("\n") if c.strip()]
                data["category"] = cats[0]
                data["categories"] = cats

            elif current_section == "Tags":
                tags = [t.strip() for t in current_text.split("#") if t.strip()]
                data["tags"] = tags
                if data.get("categories"):
                    data["tags"] += data["categories"]
                data["tags"] = list(set(data["tags"]))
            elif current_section == "Supported Devices":
                platforms = [t.strip() for t in current_text.split(" ") if t.strip()]
                data["platforms"] = platforms
            current_section = line.split("# ")[-1].replace(":", "").strip()
            current_text = ""
            current_items = []
        elif line.startswith("* "):
            current_items.append(line[2:].replace("`", "").replace('"', ""))
        elif line.startswith("- "):
            current_items.append(line[2:].replace("`", "").replace('"', ""))
        else:
            current_text += "\n" + line

    return data


def desktop_to_json(desktop: str) -> dict:
    """Accepts a desktop entry as a str, and returns a dict representing valid JSON about a skill
    """
    lines = desktop.split("\n")
    data = {}
    for l in lines:
        if "=" not in l:
            continue
        k = l.split("=")[0]
        val = l.replace(k + "=", "")
        data[k] = val
    return data


def build_skills_list():
    """
    Builds skills list for extracting examples, intents, etc.
    : returns: list of skill directories
    """
    skills = list()
    skills_dirs = get_skill_directories()
    plugin_dirs = get_plugin_skills()[0]

    for skills_dir in skills_dirs:
        if not isdir(skills_dir):
            LOG.warning(f"No such directory: {skills_dir}")
            continue
        for skill in listdir(skills_dir):
                    if path.isdir(path.join(skills_dir, skill)):
                        skills.append(path.join(skills_dir, skill))

    for skill_dir in plugin_dirs:
        if path.isdir(skill_dir[0]):
            skills.append(skill_dir[0])

    return skills


def read_skill_json(skill_dir: str) -> dict:
    """
    Get a dict representation of the specified skill (directory)
    :param skill_dir: directory containing skill files
    :returns: dict spec read from `skill.json` or built from skill dirname
    """        
    if not path.isdir(skill_dir):
        raise FileNotFoundError(f"{skill_dir} is not a valid directory")
    if path.isfile(path.join(skill_dir, "skill.json")):
        with open(path.join(skill_dir, "skill.json")) as f:
            skill_data = json.load(f)
    else:
        skill_name = str(path.basename(skill_dir).split('.')[0]).\
            replace('-', ' ').lower()
        skill_data = {"title": skill_name}
    return skill_data


def read_skill_examples(skill_dir: str) -> list:
    """
    Get a list of examples from the specified skill (directory)
    :param skill_dir: directory containing skill files
    :returns: list of examples
    """
    examples = list()
    if not path.isdir(skill_dir):
        raise FileNotFoundError(f"{skill_dir} is not a valid directory")

    skill_data = read_skill_json(skill_dir)
    if "examples" in skill_data:
        examples = skill_data["examples"]

    elif path.isfile(path.join(skill_dir, "README.md")):
        with open(path.join(skill_dir, "README.md")) as f:
            readme = f.read()
            readme_data = readme_to_json(readme)
            if readme_data.get("examples"):
                examples = readme_data["examples"]
     
    return examples


def get_skills_info():
    """
    Builds a list of skills with info about them
    :returns: list of skills with info
    """
    skills_info = list()
    skills_list = build_skills_list()
    for skill_dir in skills_list:
        info = read_skill_json(skill_dir)
        skills_info.append(info)
    
    return skills_info


def get_skills_examples(randomize=False):
    """
    Builds a list of skill examples from all skills
    :param randomize: whether to randomize the list of examples
    :returns: list of skill examples
    """
    skill_examples = list()
    skills_list = build_skills_list()
    for skill_dir in skills_list:
        examples = read_skill_examples(skill_dir)
        skill_examples += examples
    
    if randomize:
        shuffle(skill_examples)
        return skill_examples
    else:
        return skill_examples


def get_skills_from_url(url: str) -> list:
    """
    Parse a list of skill references at a given URL
    :param url: URL of skill list to parse (one skill per line)
    :returns: list of skills by name, url, and/or ID
    """
    r = SESSION.get(url)
    if not r.ok:
        LOG.warning(f"Cached response returned: {r.status_code}")
        SESSION.cache.delete_url(r.url)
        r = requests.get(url)
    if r.ok:
        return [s for s in r.text.split("\n") if s.strip()]
    else:
        LOG.error(f"{url} request failed with code: {r.status_code}")
    return []


def set_osm_constraints_file(constraints_file: str):
    """
    Sets the DEFAULT_CONSTRAINTS param for OVOS Skills Manager.
    :param constraints_file: path to valid constraints file for the core
    """
    if not constraints_file:
        raise ValueError("constraints_file not defined")
    import ovos_skills_manager.requirements
    ovos_skills_manager.requirements.DEFAULT_CONSTRAINTS = constraints_file


def get_pypi_package_versions(pkg_name: str) -> list:
    """
    Get a list of package versions available on PyPI
    :param pkg_name: package name to search on PyPI
    :returns: sorted list of available versions on PyPI
    """
    url = f"https://pypi.org/pypi/{pkg_name}/json"
    data = requests.get(url).json()
    versions = list(data.get("releases", {}).keys())
    versions.sort(key=StrictVersion)
    return versions


def install_local_skill_dependencies(
        skills_dirs: Union[str, List[str]] = None) -> list:
    """
    Install skill dependencies for skills in the specified directory and ensure
    the directory is loaded.
    NOTE: dependence on other skills is not handled here.
          Only Python and System dependencies are handled
    :param skills_dirs: Directory or list of directories to install skills from
    :returns: list of installed skill directories
    """
    from ovos_skills_manager.skill_entry import SkillEntry
    from ovos_skills_manager.requirements import pip_install, install_system_deps
    skills_dirs = skills_dirs or get_skill_directories()

    if not isinstance(skills_dirs, list):
        skills_dirs = [skills_dirs]
    installed_skills = list()
    for skills_dir in skills_dirs:
        skills_dir = os.path.expanduser(skills_dir)
        if not isdir(skills_dir):
            raise ValueError(f"{skills_dir} is not a valid directory")
        for skill in listdir(skills_dir):
            skill_dir = join(skills_dir, skill)
            if not isdir(skill_dir):
                continue
            if not isfile(join(skill_dir, "__init__.py")):
                continue
            LOG.debug(f"Attempting installation of {skill}")
            try:
                entry = SkillEntry.from_directory(skill_dir)
                pip_install(entry.requirements.get('python', list()))
                install_system_deps(entry.requirements.get('system', dict()))
                installed_skills.append(skill)
            except Exception as e:
                LOG.error(f"Exception while installing {skill}")
                LOG.exception(e)
    return installed_skills
