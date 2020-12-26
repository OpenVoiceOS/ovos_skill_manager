from ovos_utils.log import LOG
from os.path import exists, join, dirname
import os
import sys
from subprocess import PIPE, Popen
from pako import PakoManager
from ovos_skills_manager.exceptions import PipException, SkillRequirementsException
from json_database.utils.combo_lock import ComboLock
from tempfile import gettempdir

# default constraints to use if none are given
DEFAULT_CONSTRAINTS = '/etc/mycroft/constraints.txt'
PIP_LOCK = ComboLock(join(gettempdir(), "ovos_pip.lock"))


def pip_install(packages, constraints=None):
    if not len(packages):
        return False
    # Use constraints to limit the installed versions
    if constraints and not exists(constraints):
        LOG.error('Couldn\'t find the constraints file')
        return False
    elif exists(DEFAULT_CONSTRAINTS):
        constraints = DEFAULT_CONSTRAINTS

    can_pip = os.access(dirname(sys.executable), os.W_OK | os.X_OK)
    pip_args = [sys.executable, '-m', 'pip', 'install']
    if constraints:
        pip_args += ['-c', constraints]

    if not can_pip:
        pip_args = ['sudo', '-n'] + pip_args

    with PIP_LOCK:
        """
        Iterate over the individual Python packages and
        install them one by one to enforce the order specified
        in the manifest.
        """
        for dependent_python_package in packages:
            pip_command = pip_args + [dependent_python_package]
            proc = Popen(pip_command, stdout=PIPE, stderr=PIPE)
            pip_code = proc.wait()
            if pip_code != 0:
                stderr = proc.stderr.read().decode()
                raise PipException(
                    pip_code, proc.stdout.read().decode(), stderr
                )

    return True


def install_system_deps(manifest, overrides=None):
    overrides = overrides or {
        exe: (packages or '').split()
        for exe, packages in manifest.items()
    }
    packages = overrides.pop('all', [])
    if not len(packages):
        return False
    try:
        manager = PakoManager()
        return manager.install(packages, overrides=overrides)
    except Exception as e:
        raise SkillRequirementsException(str(e))
