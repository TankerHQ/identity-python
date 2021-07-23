import argparse
from pathlib import Path
import sys

import tbump
import tbump.config


def version_from_git_tag(git_tag: str) -> str:
    prefix = "v"
    assert git_tag.startswith(prefix), f"tag should start with {prefix}"
    cfg_file = tbump.config.get_config_file(Path.cwd())
    tbump_cfg = cfg_file.get_config()
    regex = tbump_cfg.version_regex
    version = git_tag[len(prefix):]
    match = regex.match(version)
    assert match, f"Could not parse {git_tag} as a valid tag"
    return version


def deploy_sdk(*, git_tag: str) -> None:
    version = version_from_git_tag(git_tag)
    tbump.bump_files(version)


def main() -> None:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(title="subcommands", dest="command")
    deploy_parser = subparsers.add_parser("deploy")
    deploy_parser.add_argument("--git-tag", required=True)
    args = parser.parse_args()
    if args.command == "deploy":
        deploy_sdk(git_tag=args.git_tag)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
