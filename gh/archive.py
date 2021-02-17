"""
Create and update an archive of Github repositories
"""

import click

def get_repo_list(db):
    """
    Extract list of git URLs for repos
    """
    return repo_list

def clone_update_repo(git_url, folder_p):
    """
    Check existence of local copy and clone/fetch otherwise
    """
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
def run_update(db_path, folder_p):
    """
    Clone/update a list of repositories whose URLs are stored in a DB
    ...

    Read DB with list of repos, clone/update each
    """
    return None

if __name__ == '__main__':
    run_update()

