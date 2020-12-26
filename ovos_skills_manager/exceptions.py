from json.decoder import JSONDecodeError


class SkillRequirementsException(RuntimeError):
    """ Skill requirements installation failed """


class PipException(SkillRequirementsException):
    """ failed to run pip """


class GithubSkillEntryError(ValueError):
    """ failed to understand github skill"""


class GithubInvalidUrl(GithubSkillEntryError):
    """ unrecognized url """


class GithubInvalidBranch(GithubInvalidUrl):
    """ unrecognized url """


class GithubRawUrlNotFound(GithubInvalidUrl):
    """ unrecognized url """


class GithubDownloadUrlNotFound(GithubInvalidUrl):
    """ unrecognized url """


class GithubReadmeNotFound(GithubInvalidUrl):
    """ could not extract readme from github """


class GithubJsonNotFound(GithubInvalidUrl):
    """ could not extract .json from github """


class GithubIconNotFound(GithubInvalidUrl):
    """ could not extract icon from github """


class GithubDesktopNotFound(GithubInvalidUrl):
    """ could not extract .desktop from github """


class GithubLicenseNotFound(GithubInvalidUrl):
    """ could not extract .desktop from github """


class GithubRequirementsNotFound(GithubInvalidUrl):
    """ could not extract requirements.txt from github """


class GithubSkillRequirementsNotFound(GithubInvalidUrl):
    """ could not extract skill_requirements.txt from github """


class GithubManifestNotFound(GithubInvalidUrl):
    """ could not extract manifest.yml from github """


class InvalidManifest(GithubManifestNotFound):
    """ manifest.yml from github is invalid YAML """


class GithubNotSkill(GithubInvalidUrl):
    """ does not seem to be an actual skill """


class UnknownAppstore(ValueError):
    """ unrecognized appstore """