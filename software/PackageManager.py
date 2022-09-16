"""
TheNexusAvenger

Wrappers for package managers.
"""

import os
import subprocess
from typing import List
from helper.Path import pathFileExists
from helper.Process import runProcess

staticPackageManagers = {}


class PackageManager:
    def isPackageInstalled(self, package: str) -> bool:
        """Determines if a package is installed.

        :param package: The name of the package to check.
        :return: Whether it is installed or not.
        """

        raise NotImplementedError()


    def installPackages(self, packages: List[str]) -> None:
        """Installs a list of packages.

        :param packages: Packages to install.
        """

        raise NotImplementedError()


class AptPackageManager(PackageManager):
    def __init__(self):
        """Creates the apt package manager interface.
        """

        # Build the cache of the installed packages.
        self.installedPackages = []
        for line in subprocess.check_output(["apt", "list", "--installed"], stderr=subprocess.DEVNULL).decode().split("\n"):
            self.installedPackages.append(line.split("/")[0].lower())


    def isPackageInstalled(self, package: str) -> bool:
        """Determines if a package is installed.

        :param package: The name of the package to check.
        :return: Whether it is installed or not.
        """

        return package.lower() in self.installedPackages


    def installPackages(self, packages: List[str]) -> None:
        """Installs a list of packages.

        :param packages: Packages to install.
        """

        runProcess(["apt", "install", "-y"] + packages)


class PacmanPackageManager(PackageManager):
    def __init__(self, keyword="pacman"):
        """Creates the pacman package manager interface.
        """

        # Build the cache of the installed packages.
        self.keyword = keyword
        self.installedPackages = []
        for line in subprocess.check_output([self.keyword, "-Q"], stderr=subprocess.DEVNULL).decode().split("\n"):
            self.installedPackages.append(line.split(" ")[0].strip().lower())


    def isPackageInstalled(self, package: str) -> bool:
        """Determines if a package is installed.

        :param package: The name of the package to check.
        :return: Whether it is installed or not.
        """

        return package.lower() in self.installedPackages


    def installPackages(self, packages: List[str]) -> None:
        """Installs a list of packages.

        :param packages: Packages to install.
        """

        runProcess([self.keyword, "--needed", "--noconfirm", "-S"] + packages)


class YayPackageManager(PacmanPackageManager):
    def __init__(self):
        """Creates the yay package manager interface.
        """

        super().__init__("yay")


    def installPackages(self, packages: List[str]) -> None:
        """Installs a list of packages.

        :param packages: Packages to install.
        """

        # Due to permission issues, the AUR install calls are ran in a separate terminal window.
        # --no-confirm is not used due to it aborting when there are conflicting packages.
        runProcess(["su", os.environ["SUDO_USER"], "-c", "konsole -e \"yay -S --needed " + " ".join(packages) + "\""])


def getPackageManager(packageManagerName: str) -> PackageManager:
    """Returns the static package manager for a given name.

    :param packageManagerName: Name of the package manager.
    :return: The package manager for the given name.
    """

    global staticPackageManagers
    packageManagerName = packageManagerName.lower()
    if packageManagerName == "aur":
        packageManagerName = "yay"
    if packageManagerName not in staticPackageManagers.keys():
        if packageManagerName == "apt":
            staticPackageManagers["apt"] = AptPackageManager()
        elif packageManagerName == "pacman":
            staticPackageManagers["pacman"] = PacmanPackageManager()
        elif packageManagerName == "yay":
            staticPackageManagers["yay"] = YayPackageManager()
    return staticPackageManagers[packageManagerName]


def getSystemPackageManager() -> str:
    """Returns the name of system package manager to use.

    :return: The name of system package manager to use.
    """

    for packageManager in ["apt", "pacman"]:
        if pathFileExists(packageManager):
            return packageManager
