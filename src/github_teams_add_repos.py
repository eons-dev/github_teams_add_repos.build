import logging
from github import github

# Adapted from https://gist.github.com/narze/2c2e141f03daea2c23fc5795107d41d4
class github_teams_add_repos(github):
    def __init__(this, name="github_teams_add_repos"):
        super().__init__(name)

        this.supportedProjectTypes = []

        this.requiredKWArgs.append('org')
        this.requiredKWArgs.append('team')

        this.optionalKWArgs['permission'] = 'push'
        this.optionalKWArgs['repos'] = []

    def Build(this):
        super().Build()

        if (this.permission not in ['pull', 'push', 'admin']):
            logging.error(f"Invalid permission: {this.permission}")
            raise Exception(f"Invalid permission: {this.permission}")

        if (not this.repos):
            code, this.repos = this.RunCommand(f"gh repo list {this.org} --limit 200 --json name --json owner -q '.[] | \"\(.owner.login)/\(.name)\"'", saveout=True)
        else:
            this.repos = [f"{this.org}/{repo}" for repo in this.repos]
        logging.info(f"Using repos: {this.repos}")
        if (not this.repos):
            raise Exception("No repos found")
        
        for repo in this.repos:
            this.RunCommand(f"gh api --method PUT -H \"Accept: application/vnd.github+json\" /orgs/{this.org}/teams/{this.team}/repos/{repo} -f permission={this.permission}")