"""
Create and update an archive of Github repositories
"""

import os
import click
import subprocess
import sqlite_utils

def get_repo_list(db):
    """
    Extract list of git URLs for repos
    """
    db = sqlite_utils.Database(db)
    repo_list = db.execute(
            """
            SELECT 'https://github.com/' || full_name || '.git'
            FROM repos 
            WHERE private == 0
            ;
            """    
    ).fetchall()
    repo_list = [i[0] for i in repo_list]
    return repo_list

@click.command()
@click.option(
        "-u",
        "--git-url",
        help = "Git URL to repo"
)
@click.option(
        "-f",
        "--folder-p",
        help = "Path to the folder where to store locally repositories"
)
def cu_single_repo(git_url, folder_p):
    """
    Clone/update a single repository

    ...

    Check existence of local copy and clone/fetch otherwise.

    The repo is then placed (or assumed to be) at `folder_p/org/repo`
    """
    parts = git_url.split("/")
    org_name = parts[-2]
    repo_name = parts[-1].replace(".git", "")
    repo_folder = f"{folder_p}/{org_name}/{repo_name}"
    # Update
    if os.path.isdir(folder_p):
        subprocess.run(
                ["cd", "repo_folder", "&&", "git", "fetch"]
        )
        subprocess.run(
                ["cd", "repo_folder", "&&", "git", "fetch", "--tags"]
        )
    # Clone
    else:
        subprocess.run(
                ["mkdir", "-p", repo_folder]
        )
        subprocess.run(
                ["git", "clone", git_url, repo_folder]
        )
    return None

@click.command()
@click.option(
        "-db",
        "--path-to-db",
        help = "Path to DB with list of repositories"
)
@click.option(
        "-f",
        "--folder-for-backup",
        help = "Path to the folder where to store locally repositories"
)
def cu_repos(db_path, folder_p):
    """
    Clone/update a list of repositories
    ...

    List of URLs repos are stored in a SQLite DB. Read DB with list of repos,
    clone/update each
    """
    return None

if __name__ == '__main__':
    #cu_repos()
    cu_single_repo()

