"""Validate PR only changes allowed files."""
import argparse
import os
import sys

import sh

BRANCH_SLUG = 'branch_slug'
# TRAVIS_COMMIT_RANGE or FETCH_HEAD $(git merge-base FETCH_HEAD master)
COMMIT_RANGE = 'commit_range'
REPO_PATH = 'repo_path'
ALLOWED_CHALLENGES = 'allowed_challenges'
CHALLENGES = ['1', '2', '3', '4', 'bonus', 'test']
SUBMISSIONS = 'submissions'
USERNAME_CHALLENGE = '{}_{}.csv.gpg'
TEAMS = 'teams'
USERNAME_TEAM = '{}_team.csv.gpg'


def parse_command_line():
    """Parse the provided command line."""
    parser = argparse.ArgumentParser(
        description='Validate that a PR only changes allowed files.')
    parser.add_argument(
        '-p', '--repo-path', dest=REPO_PATH, type=str,
        help='the name of the git project')
    parser.add_argument(
        '-g', '--commit-range', dest=COMMIT_RANGE, type=str,
        default='master..HEAD',
        help='the commit range to scan, ie "master..HEAD"')
    parser.add_argument(
        '-b', '--branch', dest=BRANCH_SLUG, type=str, help='the branch slug')
    parser.add_argument(
        '-a', '--allowed', dest=ALLOWED_CHALLENGES, type=list,
        help='the branch slug')
    args = parser.parse_args()
    return args


def validate(commit_range, branch_slug, allowed_challenges=None, repo=None):
    """Validate pull request."""
    git = sh.git.bake('--no-pager')
    cwd = os.getcwd()
    if repo is not None:
        os.chdir(repo)
    changes = git.diff(commit_range, '--name-only')
    if not changes:
        print('No changes found')
        stop(cwd, 1)
    change_list = changes.strip().split('\n')
    username = branch_slug.split('/')[0]
    required = os.path.join(TEAMS, USERNAME_TEAM.format(username))
    if allowed_challenges is None:
        allowed_challenges = CHALLENGES
    allowed = [
        os.path.join(
            SUBMISSIONS, str(challenge),
            USERNAME_CHALLENGE.format(username, challenge))
        for challenge in allowed_challenges]
    allowed.append(required)
    unallowed = [fil for fil in change_list if fil not in allowed]
    if required not in change_list and not os.path.exists(required):
        print(
            'Team info csv file is missing or is not not equal to '
            '[GitHub username]_[team].csv.gpg')
        print('Your GitHub username is:', username)
        print('You team info csv file should be committed as:', required)
        stop(cwd, 1)
    if not unallowed:
        stop(cwd)
        return
    print(
        'All files changed are not equal to '
        '[GitHub username]_[challenge number].csv.gpg')
    print('Your GitHub username is:', username)
    print('Allowed challenges to test are:', allowed_challenges)
    print('Allowed changed files would be:')
    for fil in allowed:
        print(fil)
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
    validate(
        cmd_args.commit_range, cmd_args.branch_slug,
        cmd_args.allowed_challenges, cmd_args.repo_path)


if __name__ == '__main__':
    main()
