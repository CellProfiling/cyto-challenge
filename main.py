"""Check pull requests and score submitted answers."""
import json
import os
from glob import iglob

from gen_markdown import (F1_SCORE, PRECISION, RECALL, SCORE_FILE, SOLUTIONS,
                          gen_md)
from pr_validation import validate
from solution_checker import score

SUBMISSION_PATH = './submissions/*/*.csv'
TRAVIS_COMMIT_RANGE = 'TRAVIS_COMMIT_RANGE'
MASTER_HEAD_RANGE = 'master..HEAD'
TRAVIS_PULL_REQUEST_SLUG = 'TRAVIS_PULL_REQUEST_SLUG'


def check(commit_range=None, branch_slug=None):
    """Perform checks."""
    env = os.environ.copy()
    if commit_range is None:
        commit_range = env.get(TRAVIS_COMMIT_RANGE)
    if commit_range is None:
        commit_range = MASTER_HEAD_RANGE
    if branch_slug is None:
        branch_slug = env.get(TRAVIS_PULL_REQUEST_SLUG)
    if branch_slug:
        validate(commit_range, branch_slug, SOLUTIONS.keys())
    else:
        check_scores()


def check_scores():
    """Check scores."""
    with open(SCORE_FILE, 'r+') as score_file:
        scores = json.load(score_file)
        score_file.seek(0)
        score_file.truncate()  # clear file
        for submitted in iglob(SUBMISSION_PATH):
            base, _ = os.path.splitext(submitted)
            _, team_challenge = os.path.split(base)
            parts = team_challenge.split('_')
            challenge = str(parts[-1])
            team = ''.join(parts[:-1])
            solutions = SOLUTIONS[challenge]
            for sol_path in solutions:
                fin_r_score, fin_p_score, fin_f_score = score(
                    submitted, sol_path)
                # FIXME: Handle cases of more than one solution per challenge
                scores.update({team: {challenge: {
                    RECALL: fin_r_score, PRECISION: fin_p_score,
                    F1_SCORE: fin_f_score}}})
            print(scores)
        json.dump(scores, score_file)


def main():
    """Run main."""
    check()
    gen_md()


if __name__ == '__main__':
    main()
