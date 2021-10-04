import pickle
from pathlib import Path
from typing import Dict, Tuple, List

import tqdm
from github import Github
from github.Issue import Issue
from github.Organization import Organization
from github.Project import Project
from github.ProjectCard import ProjectCard
from github.ProjectColumn import ProjectColumn
from github.Repository import Repository

from gihuha.models import GData


def retrieve_data(*, github_api_token: str, base_path: str, org_name: str):
    base_path = Path(base_path)
    base_path.mkdir(parents=True, exist_ok=True)
    g = Github(github_api_token, per_page=100)
    org: Organization
    org = g.get_organization(org_name)

    project_column_cards = get_project_column_cards(org)
    repo_issues = get_repo_issues(org)

    gd = GData(project_column_cards=project_column_cards, repo_issues=repo_issues)

    with open(base_path / "data.pickle", "wb") as outf:
        pickle.dump(gd, file=outf, protocol=pickle.HIGHEST_PROTOCOL)


def get_project_column_cards(
    org: Organization,
) -> Dict[Tuple[Project, ProjectColumn], List[ProjectCard]]:
    projects = list(
        tqdm.tqdm(org.get_projects(state="open"), desc="retrieving projects")
    )
    project: Project
    project_column: ProjectColumn
    project_column_cards = {}
    for project in projects:
        column: ProjectColumn
        for column in project.get_columns():
            project_column_cards[(project, column)] = list(
                tqdm.tqdm(
                    column.get_cards(archived_state="open"),
                    desc=f"retrieving {project.name} col {column.name} cards",
                )
            )
    return project_column_cards


def get_repo_issues(org: Organization) -> Dict[Repository, List[Issue]]:
    repo: Repository
    repos = [
        repo
        for repo in tqdm.tqdm(org.get_repos(type="private"), desc="retrieving repos")
        if not repo.archived
    ]
    repo_issues = {
        repo: list(
            tqdm.tqdm(
                repo.get_issues(state="open"), desc=f"retrieving {repo.name} issues"
            )
        )
        for repo in tqdm.tqdm(repos, desc="retrieving issues")
    }
    return repo_issues
