"""Check pull requests and score submitted answers."""
import json
import os
from collections import Mapping, defaultdict
from glob import iglob

from gen_markdown import (CHALLENGE_BONUS, F1_SCORE, F1_SCORE_OLD, PRECISION,
                          PRECISION_OLD, RECALL, RECALL_OLD, SCORE_FILE,
                          SOLUTIONS, gen_md)
from pr_validation import validate
from solution_checker import ScoreError, score

SUBMISSION_PATH = './submissions/*/*.csv'
TRAVIS_COMMIT_RANGE = 'TRAVIS_COMMIT_RANGE'
MASTER_HEAD_RANGE = 'master..HEAD'
TRAVIS_PULL_REQUEST_SLUG = 'TRAVIS_PULL_REQUEST_SLUG'
SCORE_FAIL = 'auto-scoring failed'


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
        scores_copy = update({}, scores)
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
            for team, results in scores.items():
                scores_copy[team][challenge][F1_SCORE_OLD] = results[
                    challenge].get(F1_SCORE, '-')
                scores_copy[team][challenge][PRECISION_OLD] = results[
                    challenge].get(PRECISION, '-')
                scores_copy[team][challenge][RECALL_OLD] = results[
                    challenge].get(RECALL, '-')
            for sol_path in SOLUTIONS[challenge]:
                try:
                    fin_r_score, fin_p_score, fin_f_score = score(
                        submitted, sol_path)
                except ScoreError:
                    update(scores_copy, {team: {challenge: {
                        RECALL: SCORE_FAIL, PRECISION: SCORE_FAIL,
                        F1_SCORE: SCORE_FAIL}}})
                # FIXME: Handle cases of more than one solution per challenge
                else:
                    update(scores_copy, {team: {challenge: {
                        RECALL: fin_r_score, PRECISION: fin_p_score,
                        F1_SCORE: fin_f_score}}})
            print(scores_copy)
        json.dump(scores_copy, score_file)


def main():
    """Run main."""
    check()
    gen_md()


if __name__ == '__main__':
    main()
