from collections import defaultdict

from github.Issue import Issue

from gihuha.models import GData


def print_projectless_issues(data: GData):
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
