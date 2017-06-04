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
    'Team', 'F1 score', 'Previous F1 Score', 'Precision', 'Previous precision',
    'Recall', 'Previous recall'
]
SCORE_FILE = 'scores.json'
RECALL = 'recall'
PRECISION = 'precision'
F1_SCORE = 'f1_score'
RECALL_OLD = 'recall_old'
PRECISION_OLD = 'precision_old'
F1_SCORE_OLD = 'f1_score_old'
CHALLENGE_1 = '1'
CHALLENGE_2 = '2'
CHALLENGE_3 = '3'
CHALLENGE_4 = '4'
CHALLENGE_BONUS = 'bonus'
CHALLENGE_TEST = 'test'
SOLUTIONS = {
    CHALLENGE_2: ['solutions/challenge2/major13_test_obfuscated.csv'],
    CHALLENGE_3: ['solutions/challenge3/rare_events_test_obfuscated.csv'],
    CHALLENGE_4: [
        'solutions/challenge4/class_disc_test_obfuscated.csv',
        'solutions/challenge4/rare_events_class_disc_test_obfuscated.csv'],
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
TAB_COL_ORDER = [
    F1_SCORE, F1_SCORE_OLD, PRECISION, PRECISION_OLD, RECALL, RECALL_OLD]


def make_table(scores, challenge):
    """Make a list of lists for a challenge, that will constitute a table."""
    table = []
    for team, results in scores.items():
        if not results.get(challenge):
            continue
        inner = [team]
        inner.extend([
            '{:.3f}'.format(results[challenge].get(col, 0))
            if isinstance(results[challenge].get(col, 0), float)
            else results[challenge][col]
            for col in TAB_COL_ORDER])
        table.append(inner)
    return sorted(table, key=lambda x: x[1], reverse=True)


def gen_md(path=None):
    """Generate the readme file."""
    if path is None:
        path = SCORE_FILE
    text = ''
    with open(INSTRUCTIONS, 'r') as instructions_file:
        instructions = instructions_file.read()
    with open(DISCLAIMER, 'r') as disclaimer_file:
        disclaimer = disclaimer_file.read()
    with open(path, 'r') as score_file:
        scores = json.load(score_file)
    tables = {
        challenge: make_table(scores, challenge) for challenge in SOLUTIONS}
    tables = OrderedDict(sorted(tables.items(), key=lambda t: t[0]))
    with open(README, 'r+') as readme:
        readme.truncate()  # clear file
        text += '{}\n\n'.format(disclaimer)
        text += LEADERBOARD_HEAD
        for challenge, table in tables.items():
            if table:
                text += CHALLENGE_HEAD.format(challenge)
                text += tabulate(table, HEADERS, tablefmt='pipe')
                text += '\n\n'
        link_text = PROTEIN_ATLAS + CYTO_CONFERENCE
        text += link_text.format(*LINKS)
        text += instructions
        readme.write(text)


def main():
    """Run main."""
    gen_md()


if __name__ == '__main__':
    main()
