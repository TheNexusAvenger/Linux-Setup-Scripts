"""
TheNexusAvenger

Helper functions for processes.
"""

import subprocess
from typing import List


def runProcess(parameters: List[str], workingDirectory: str = None) -> None:
    """Runs a process.

    :param parameters: Parameters to run in the process, including the file and parameters to the file.
    :param workingDirectory: Working directory to run the process.
    """

    process = subprocess.Popen(parameters, cwd=workingDirectory)
    process.wait()
    if process.returncode != 0:
        raise Exception("Process returned an error code " + str(process.returncode))
