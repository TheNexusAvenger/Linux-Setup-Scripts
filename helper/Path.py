"""
TheNexusAvenger

Helper for finding files in the system PATH.
"""

import os
from typing import Optional


def getFilePath(fileName: str) -> Optional[str]:
    """Finds the full path of a file in the system PATH.

    :param fileName: Name of the file to find.
    :return: The path to the file if it exists.
    """

    for pathEntry in (os.name == "nt" and os.getenv("PATH").split(";") or os.getenv("PATH").split(":")):
        filePath = os.path.join(pathEntry, fileName)
        if os.path.exists(filePath):
            return filePath
    return None


def pathFileExists(fileName: str) -> bool:
    """Determines if a file exists in the system PATH.

    :param fileName: Name of the file to find.
    :return: If the file exists in the system PATH.
    """

    return getFilePath(fileName) is not None