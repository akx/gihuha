import argparse
import os
import pickle

from gihuha import settings
from gihuha.models import GData
from gihuha.retrieve import retrieve_data
from gihuha.tools import print_projectless_issues


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("org_name")
    args = ap.parse_args()
    org_name = args.org_name
    base_path = f"./data_{org_name}"
    pickle_file = os.path.join(base_path, "data.pickle")

    if not os.path.isfile(pickle_file):
        retrieve_data(
            github_api_token=settings.GITHUB_API_TOKEN,
            base_path=base_path,
            org_name=org_name,
        )
    with open(pickle_file, "rb") as f:
        data: GData = pickle.load(f)

    print_projectless_issues(data)


if __name__ == "__main__":
    main()
