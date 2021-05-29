# Github mirror

This document provides guidance to set up an automated mirror of all the repositories under an account.

## Command line tool

A lightweight command line is available at `mirror.py` with utilities to pull down information on the repositories and perform a `clone`/`fetch` on each of them on a desired local folder.

```shell
python mirror.py --help
```

Requirements:

- Stack in the Dogsheep [`Dockerfile`](../Dockerfile)
- A personal authentification token from Github
- A local folder where to store the repositories

**NOTE**: currently, `mirror.py` is hardcoded for the user `darribas`. You will need to modify this on the `mirror/run_update` method

## Single command

The cli tool can be directly called from the base of the `pdata` repository:

```shell
cd /path/to/pdata
```

Through a `make` command:

```shell
make gh_clone_fetch data_folder=/path/to/local/mirror/folder
```

This command assumens your Github token is available at `pdata/auths/github_auth.json` and will place the Github DB on `/path/to/local/mirror/folder/github.db`.

## Automated job

If you want to run a clone/fetch job in an automated way, you can create a script (e.g. `auto_github`) with the following:

```
#!/bin/bash
cd /path/to/pdata && make gh_clone_fetch data_folder=/path/to/local/mirror/folder
```

Turn it into an executable:

```
chmod +x auto_github
```

And place it on `/etc/cron.daily`