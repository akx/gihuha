import click
import tqdm
from github import Github, Hook, Organization, Repository

from gihuha import settings
from gihuha.cli.main import main
from gihuha.storage import storage


@main.command()
@click.argument("org_name")
def list_hooks(org_name):
    key = f"org-repo-hooks:{org_name}"
    hooks_per_repo: dict[Organization, list[Hook]] = storage.get(key)
    if hooks_per_repo is None:
        hooks_per_repo = storage[key] = retrieve_hooks_per_repo(org_name)
    for repo, hooks in sorted(
        hooks_per_repo.items(), key=lambda pair: pair[0].full_name
    ):
        if not hooks:
            continue
        print(f"{repo.full_name}:")
        hook: Hook
        for hook in hooks:
            url = hook.config["url"]
            print(f"  {hook.id} - {hook.name} - {url}")
        print()


@main.command()
@click.argument("org_name")
@click.argument("source_repo_name")
@click.argument("source_hook_id", type=int)
@click.argument("dest_repo_name")
def copy_hook(org_name, source_repo_name, source_hook_id, dest_repo_name):
    g = Github(settings.GITHUB_API_TOKEN, per_page=100)
    org: Organization = g.get_organization(org_name)
    source_repo: Repository = org.get_repo(source_repo_name)
    dest_repo: Repository = org.get_repo(dest_repo_name)
    source_hook = source_repo.get_hook(source_hook_id)
    print(source_hook)
    dest_hook = dest_repo.create_hook(
        name=source_hook.name,
        config=source_hook.config,
        events=source_hook.events,
        active=source_hook.active,
    )
    print("->", dest_hook)


def retrieve_hooks_per_repo(org_name: str) -> dict[Organization, list[Hook]]:
    g = Github(settings.GITHUB_API_TOKEN, per_page=100)
    org: Organization = g.get_organization(org_name)
    repo: Repository
    hooks_per_repo = {}
    for repo in tqdm.tqdm(org.get_repos(), desc="retrieving repos/hooks"):
        hooks_per_repo[repo] = list(repo.get_hooks())
    return hooks_per_repo
