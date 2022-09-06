# gihuha

Tools to play with GitHub organizations, projects, and issues.

## usage

Currently gihuha only prints out issues that don't have an associated project.

1. Set the `GITHUB_API_TOKEN` environment variable to a GitHub access token that can read repos and issues.
   * A Personal Access Token is recommended. 
   * You can use an `.env` file.
2. Run `python -m gihuha print-projectless-issues YOUR_ORG_NAME`
