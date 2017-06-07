"""Check pull requests and score submitted answers."""
import json
import os
from collections import Mapping, defaultdict
from glob import iglob

from challenge_4_checker import score_4
from gen_markdown import (CHALLENGE_4, CHALLENGE_BONUS, F1_HIGH, F1_SCORE,
                          PRECISION, RECALL, SCORE_FILE, SOLUTIONS, gen_md)
from pr_validation import validate
from solution_checker import ScoreError, score

SUBMISSION_PATH = './submissions/*/*.csv'
TRAVIS_COMMIT_RANGE = 'TRAVIS_COMMIT_RANGE'
MASTER_HEAD_RANGE = 'master..HEAD'
TRAVIS_PULL_REQUEST_SLUG = 'TRAVIS_PULL_REQUEST_SLUG'
SCORE_FAIL = 'auto-scoring failed'
NEW_CLASSES_PATH = './solutions/4/new_classes.csv'


def update(old_dict, u_dict):
    """Update dict recursively and create defaultdict if no key is found."""
    for key, val in u_dict.items():
        if isinstance(val, Mapping):
            r_dict = update(old_dict.get(key, defaultdict(dict)), val)
            old_dict[key] = r_dict
        else:
            old_dict[key] = u_dict[key]
    return old_dict


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
        scores = update({}, scores)
        score_file.seek(0)
        score_file.truncate()  # clear file
        for submitted in iglob(SUBMISSION_PATH):
            base, _ = os.path.splitext(submitted)
            _, team_challenge = os.path.split(base)
            parts = team_challenge.split('_')
            challenge = str(parts[-1])
            if challenge == CHALLENGE_BONUS:
                continue
            team = ''.join(parts[:-1])
            for sol_path in SOLUTIONS[challenge]:
                try:
                    if challenge == CHALLENGE_4:
                        fin_r_score, fin_p_score, fin_f_score = score_4(
                            submitted, sol_path, NEW_CLASSES_PATH)
                    else:
                        fin_r_score, fin_p_score, fin_f_score = score(
                            submitted, sol_path)
                except ScoreError:
                    update(scores, {team: {challenge: {
                        RECALL: SCORE_FAIL, PRECISION: SCORE_FAIL,
                        F1_SCORE: SCORE_FAIL}}})
                else:
                    update(scores, {team: {challenge: {
                        RECALL: fin_r_score, PRECISION: fin_p_score,
                        F1_SCORE: fin_f_score}}})
                    if fin_f_score > scores[team][challenge].get(
                            F1_HIGH, 0):
                        scores[team][challenge][F1_HIGH] = fin_f_score
        print(scores)
        json.dump(scores, score_file)
        score_file.write('\n')


def main():
    """Run main."""
    check()
    gen_md()


if __name__ == '__main__':
    main()
