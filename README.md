# Linux-Setup-Scripts
Helper scripts developed to set up a Linux desktop install
with KDE Plasma and desktop applications.

## `extra` Directory
For additional setup that can't be done in version control
(i.e. SSH keys), an additional `extra/ExtraUserSetup.py`
file can be created that will run after the user setup
is done. It will run without `sudo` permissions.

## Running
In a terminal, the setup script can be run with the following
(Python 3 required):
```bash
wget https://github.com/TheNexusAvenger/Linux-Setup-Scripts/archive/refs/heads/master.zip
unzip ./master.zip -d ./LinuxSetupScripts
cd ./LinuxSetupScripts/*
chmod +x ./run.sh
run.sh
```