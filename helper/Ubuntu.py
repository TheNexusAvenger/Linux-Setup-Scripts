"""
TheNexusAvenger

Helper functions for Ubuntu.
"""

import os
import re
import tempfile
from typing import List
from helper.Http import httpGet
from helper.Process import runProcess


def getPpaRepositories() -> List[str]:
    """Determines the PPA repositories that are installed.

    :return: The PPA that are installed.
    """

    # Get the list of files to check.
    filesList = []
    if os.path.exists("/etc/apt/sources.list"):
        filesList.append("/etc/apt/sources.list")
    if os.path.exists("/etc/apt/sources.list.d/"):
        for fileName in os.listdir("/etc/apt/sources.list.d/"):
            filesList.append("/etc/apt/sources.list.d/" + fileName)

    # Find the PPA entries in the files.
    ppaRepositories = []
    for filePath in filesList:
        with open(filePath) as file:
            for line in file.readlines():
                line = line.strip()
                if not line.startswith("#"):
                    for entry in re.findall(r"ppa\.[^/]+/([^/]+)/([^/]+)", line):
                        ppaEntry = "ppa:" + entry[0] + "/" + entry[1]
                        if ppaEntry not in ppaRepositories:
                            ppaRepositories.append(ppaEntry)
    return ppaRepositories


def addPpaRepository(repository: str) -> None:
    """Adds a PPA repository.

    :param repository: PPA repository to add.
    """

    runProcess(["add-apt-repository", "-y", repository])
    runProcess(["apt", "update"])


def installDebFile(url: str) -> None:
    """Downloads and installs a deb file.

    :param url: URL of the deb file to download and install.
    """

    # Download the file.
    path = tempfile.NamedTemporaryFile(suffix=".deb").name
    with open(path, "wb") as file:
        file.write(httpGet(url))

    try:
        # Install the .deb file.
        runProcess(["dpkg", "-i", path])
    except:
        # Install the dependencies after it fails and try again.
        runProcess(["apt", "-f", "install", "-y"])
        runProcess(["dpkg", "-i", path])
