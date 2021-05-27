"""
Create and update an archive of Github repositories
"""

import os
import git
import click
import subprocess
import sqlite_utils

def get_repo_list(db_path):
    """
    Extract list of git URLs for repos
    
    Arguments
    ---------
    db_path : str
              Path to sqlite DB with repo information
    Returns
    -------
    repo_list : list
                List of strings containing git URL for each repo
    """
    db = sqlite_utils.Database(db_path)
    repo_list = []
    for row in db.table("repos").rows:
        repo_list.append(row["html_url"]+".git")
    return repo_list

def clone_update_repo(git_url, folder_p):
    """
    Check existence of local copy and clone/fetch otherwise
    """
    owner = git_url.split("/")[-2]
    repo_name = git_url.split("/")[-1].strip(".git")
    name = os.path.join(owner, repo_name)
    repo_folder = os.path.join(folder_p, name)
    # Update
    if os.path.exists(repo_folder):
        out = subprocess.run(
            ["cd", repo_folder, "&&","git", "fetch", "origin"]
        )
        log = f"Updated {repo_folder}"
    # Clone
    else:
        out = subprocess.run(
            ["git", "clone", git_url, repo_folder]
        )
        log = f"Cloned {git_url} into {repo_folder}"
    return log

@click.command()
@click.argument(
        "db_path",
        required=True
)
@click.argument(
        "folder_p",
        required=True
)
def run_update(db_path, folder_p):
    """
    Clone/update a list of repositories whose URLs are stored in a DB
    ...

    Read DB with list of repos, clone/update each
    """
    return None

if __name__ == '__main__':
    run_update()

