"""Generate the readme markdown file."""
import json
from collections import OrderedDict

from tabulate import tabulate


README = 'README.md'
LINKS = [
    'http://proteinatlas.org',
    'http://cytoconference.org/2017/Program/Image-Analysis-Challenge.aspx',
]
HEADERS = [
    'Team', 'F1 score', 'Highest F1 Score', 'Precision', 'Recall'
]
SCORE_FILE = 'scores.json'
RECALL = 'recall'
PRECISION = 'precision'
F1_SCORE = 'f1_score'
F1_HIGH = 'f1_high'
CHALLENGE_1 = '1'
CHALLENGE_2 = '2'
CHALLENGE_3 = '3'
CHALLENGE_4 = '4'
CHALLENGE_BONUS = 'bonus'
CHALLENGE_TEST = 'test'
SOLUTIONS = {
    CHALLENGE_2: ['solutions/2/major13_test_obfuscated.csv'],
    CHALLENGE_3: ['solutions/3/rare_events_test_obfuscated.csv'],
    CHALLENGE_4: [
        'solutions/4/novel_classes_class_disc_test.csv'],
    CHALLENGE_BONUS: [
        'solutions/bonus/major13_test_ccv_obfuscated.csv',
        'solutions/bonus/rare_events_test_ccv_obfuscated.csv'],
    CHALLENGE_TEST: ['solutions/test/toy_events_solution.csv']
}
PROTEIN_ATLAS = 'Data provided by the [Human Protein Atlas]({})\n\n'
CYTO_CONFERENCE = 'Challenge hosted by [cytoconference.org]({})\n\n'
LEADERBOARD_HEAD = '# Leaderboard\n\n'
CHALLENGE_HEAD = '## Challenge {}\n\n'
INSTRUCTIONS = 'INSTRUCTIONS.md'
DISCLAIMER = 'DISCLAIMER.md'
DEADLINE = 'DEADLINE.md'
TAB_COL_ORDER = [F1_SCORE, F1_HIGH, PRECISION, RECALL]
CHALLENGE_3_ISSUE = (
    'There is a problem with the uploaded image test set for '
    'challenge 3. We are working on a fix.\n\n')


def make_table(scores, challenge):
    """Make a list of lists for a challenge, that will constitute a table."""
    table = []
    for team, results in scores.items():
        if not results.get(challenge):
            continue
        inner = [team]
        inner.extend([
            '{:.3f}'.format(results[challenge][col])
            if isinstance(results[challenge].get(col), float)
            else results[challenge].get(col, 'N/A')
            for col in TAB_COL_ORDER])
        table.append(inner)
    return sorted(table, key=lambda x: x[1], reverse=True)


def read_file(path):
    """Open and read file at path and return contents."""
    with open(path, 'r') as fil:
        return fil.read()


def gen_md(path=None):
    """Generate the readme file."""
    if path is None:
        path = SCORE_FILE
    text = ''
    with open(path, 'r') as score_file:
        scores = json.load(score_file)
    tables = {
        challenge: make_table(scores, challenge) for challenge in SOLUTIONS}
    tables = OrderedDict(sorted(tables.items(), key=lambda t: t[0]))
    with open(README, 'r+') as readme:
        readme.truncate()  # clear file
        text += '{}\n\n'.format(read_file(DEADLINE))
        text += '{}\n\n'.format(read_file(DISCLAIMER))
        text += LEADERBOARD_HEAD
        for challenge, table in tables.items():
            if table:
                text += CHALLENGE_HEAD.format(challenge)
                if challenge == CHALLENGE_3:
                    text += CHALLENGE_3_ISSUE
                text += tabulate(table, HEADERS, tablefmt='pipe')
                text += '\n\n'
        link_text = PROTEIN_ATLAS + CYTO_CONFERENCE
        text += link_text.format(*LINKS)
        text += read_file(INSTRUCTIONS)
        readme.write(text)


def main():
    """Run main."""
    gen_md()


if __name__ == '__main__':
    main()
