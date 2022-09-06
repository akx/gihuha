from collections import defaultdict

import click
from github import Issue

from gihuha import settings
from gihuha.cli.main import main
from gihuha.models.project_and_repo_data import ProjectAndRepoData
from gihuha.storage import storage


@main.command()
@click.argument("org_name")
def print_projectless_issues(org_name):
    key = f"project-and-repo-data:{org_name}"
    data = storage.get(key)
    if data is None:
        data: ProjectAndRepoData = ProjectAndRepoData.retrieve(
            github_api_token=settings.GITHUB_API_TOKEN,
            org_name=org_name,
        )
        storage[key] = data

    issue_url_to_card = defaultdict(list)
    for cards in data.project_column_cards.values():
        for card in cards:
            if card.content_url and "issue" in card.content_url and not card.archived:
                issue_url_to_card[card.content_url].append(card)
    for repo, issues in sorted(
        data.repo_issues.items(), key=lambda pair: pair[0].full_name
    ):
        if not issues:
            continue
        issue: Issue
        for issue in sorted(issues, key=lambda issue: issue.number):
            if issue.pull_request:
                continue
            if issue.url not in issue_url_to_card:
                print(f"{repo.full_name}#{issue.number} - {issue.html_url}")
