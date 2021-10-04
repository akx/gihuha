import dataclasses
from typing import Dict, Tuple, List

from github.Issue import Issue
from github.Project import Project
from github.ProjectCard import ProjectCard
from github.ProjectColumn import ProjectColumn
from github.Repository import Repository


@dataclasses.dataclass(frozen=True)
class GData:
    project_column_cards: Dict[Tuple[Project, ProjectColumn], List[ProjectCard]]
    repo_issues: Dict[Repository, List[Issue]]
