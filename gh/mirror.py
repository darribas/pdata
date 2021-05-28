"""
Create and update an archive of Github repositories
"""

import os
import git
import click
from datetime import datetime
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
        if not row["private"]:
            repo_list.append(row["html_url"]+".git")
    return repo_list

def clone_update_repo(git_url, folder_p, verbose=False):
    """
    Check existence of local copy, fetch if present, clone otherwise
    
    Arguments
    ---------
    git_url : str
              Git URL to repo to check
    folder_p : str
               Local path where repo exists or should be placed
    verbose : Boolean
              [Optional. Default=False] If True, print logs
    
    Returns
    -------
    log : str
          Log message of action
    """
    owner = git_url.split("/")[-2]
    repo_name = git_url.split("/")[-1].replace(".git", "")
    name = os.path.join(owner, repo_name)
    repo_folder = os.path.join(folder_p, name)
    log = f"{datetime.now()}\t| Working on {git_url}\n"
    # Update
    if os.path.exists(repo_folder):
        wd = os.getcwd()
        os.chdir(repo_folder)
        out = subprocess.run(
            ["git", "fetch", "origin"],
            capture_output=True,
            text=True
        )
        os.chdir(wd)
        log += f"\t{out.stdout}\n\t{out.stderr}\n"
        log += f"{datetime.now()}\t| Updated {repo_folder}"
    # Clone
    else:
        out = subprocess.run(
            ["git", "clone", git_url, repo_folder],
            capture_output=True,
            text=True        
        )
        log += f"\t{out.stdout}\n\t{out.stderr}\n"
        log += f"{datetime.now()}\t| Cloned {git_url} into {repo_folder}\n"
    if verbose:
        print(log)
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
@click.option(
    "-t",
    "--github_token",
    type=click.Path(file_okay=True, dir_okay=False, allow_dash=False),
    default=None,
    help=("Path to JSON file with Github token. "\
          "If not provided, `db_path` is not updated"),
)
@click.option(
    "-l",
    "--log_file",
    type=click.Path(file_okay=True, dir_okay=False, allow_dash=False),
    default=None,
    help="Path to write out log file",
)
@click.option(
    "-m",
    "--log-mode",
    type=click.Path(file_okay=True, dir_okay=False, allow_dash=False),
    default=None,
    help="Mode to write out log file (default=`w`)",
)
@click.option(
    "-v",
    "--verbose",
    is_flag=True,
    help="Print out logs",
)
def run_update(
    db_path, folder_p, github_token=None, log_file=None, log_mode="w", verbose=False
):
    """
    Clone/update a list of repositories whose URLs are stored in a DB
    
    ...

    Read DB with list of repos, clone/update each
    
    Arguments:
    
    DB_PATH : path to the SQLITE database with Github information
    
    FOLDER_P : local folder for the repo mirrors
    """
    if github_token:
        if verbose:
            log = f"{datetime.now()}\t| Downloading/updating Github DB..."
            print(log)
        out = subprocess.run(
            ["github-to-sqlite", "repos", "--readme", "--readme-html", "-a", github_token, db_path]
        )
    repo_urls = get_repo_list(db_path)
    if verbose:
        log = f"{datetime.now()}\t| Repo URLs extracted"
        print(log)
    for repo in repo_urls:
        log = clone_update_repo(repo, folder_p, verbose=verbose)
    return None

if __name__ == '__main__':
    run_update()

