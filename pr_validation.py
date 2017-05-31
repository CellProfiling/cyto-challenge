"""Validate PR only changes allowed files."""
import argparse
import os
import sys

import sh

BRANCH_SLUG = 'branch_slug'
# TRAVIS_COMMIT_RANGE or FETCH_HEAD $(git merge-base FETCH_HEAD master)
COMMIT_RANGE = 'commit_range'
REPO_PATH = 'repo_path'


def parse_command_line():
    """Parse the provided command line."""
    parser = argparse.ArgumentParser(
        description='Validate PR only changes allowed files.')
    parser.add_argument(
        '-p', '--repo-path', dest=REPO_PATH, type=str,
        help='the name of the git project')
    parser.add_argument(
        '-g', '--commit-range', dest=COMMIT_RANGE, type=str,
        default='master..HEAD',
        help='the commit range to scan, ie "master..HEAD"')
    parser.add_argument(
        '-b', '--branch', dest=BRANCH_SLUG, type=str, help='the branch slug')
    args = parser.parse_args()
    return args


def validate(commit_range, branch_slug=None, repo=None):
    """Validate pull request."""
    git = sh.git.bake('--no-pager')
    env = os.environ.copy()
    cwd = os.getcwd()
    if branch_slug is None:
        branch_slug = env.get('TRAVIS_PULL_REQUEST_SLUG')
    if branch_slug is None:
        print('No branch slug specified')
        stop(cwd, 1)
    if repo is not None:
        os.chdir(repo)
    changes = git.diff(commit_range, '--name-only')
    change_list = changes.strip().split('\n')
    username = branch_slug.split('/')[0]
    allowed = [
        '{}_{}'.format(username, challenge_no)
        for challenge_no in (1, 2, 3, 4)]
    unallowed = [fil for fil in change_list if fil not in allowed]
    if not unallowed:
        stop(cwd)
        return
    print(
        'All files changed are not equal to '
        '[GitHub username]_[challenge number].csv.\nYour GitHub username is: ',
        username)
    print('Unallowed changes in:')
    for fil in unallowed:
        print(fil)
    stop(cwd, 1)


def stop(path, code=0):
    """Change dir to path, exit and return code."""
    os.chdir(path)
    if code == 0:
        return
    sys.exit(code)


def main():
    """Run main."""
    cmd_args = parse_command_line()
    validate(cmd_args.commit_range, cmd_args.branch_slug, cmd_args.repo_path)


if __name__ == '__main__':
    main()
