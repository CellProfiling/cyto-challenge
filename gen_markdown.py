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
    'Team', 'F1 score', 'Precision', 'Recall'
]
SCORE_FILE = 'scores.json'
RECALL = 'recall'
PRECISION = 'precision'
F1_SCORE = 'f1_score'
SOLUTIONS = {
    '2': ['solutions/challenge2/major13_test_obfuscated.csv'],
    '3': ['solutions/challenge3/rare_events_test_obfuscated.csv'],
    '4': [
        'solutions/challenge4/class_disc_test_obfuscated.csv',
        'solutions/challenge4/rare_events_class_disc_test_obfuscated.csv'],
    'bonus': [
        'solutions/bonus/major13_test_ccv_obfuscated.csv',
        'solutions/bonus/rare_events_test_ccv_obfuscated.csv'],
    'test': ['solutions/test/toy_events_solution.csv']
}
PROTEIN_ATLAS = 'Data provided by the [Human Protein Atlas]({})\n\n'
CYTO_CONFERENCE = 'Challenge hosted by [cytoconference.org]({})\n\n'
LEADERBOARD_HEAD = '# Leaderboard\n\n'
CHALLENGE_HEAD = '## Challenge {}\n\n'
INSTRUCTIONS = 'INSTRUCTIONS.md'


def make_table(scores, challenge):
    """Make a list of lists for a challenge, that will constitute a table."""
    table = sorted(
        [
            [
                team, results[challenge][F1_SCORE],
                results[challenge][PRECISION],
                results[challenge][RECALL]]
            for team, results in scores.items() if results.get(challenge)],
        key=lambda x: x[1], reverse=True)
    return table


def gen_md(path=None):
    """Generate the readme file."""
    if path is None:
        path = SCORE_FILE
    text = ''
    with open(INSTRUCTIONS, 'r') as instructions_file:
        instructions = instructions_file.read()
    with open(path, 'r') as score_file:
        scores = json.load(score_file)
    tables = {
        challenge: make_table(scores, challenge) for challenge in SOLUTIONS}
    tables = OrderedDict(sorted(tables.items(), key=lambda t: t[0]))
    with open(README, 'r+') as readme:
        readme.truncate()  # clear file
        text += LEADERBOARD_HEAD
        for challenge, table in tables.items():
            if table:
                text += CHALLENGE_HEAD.format(challenge)
                text += tabulate(table, HEADERS, tablefmt="pipe")
                text += '\n\n'
        link_text = PROTEIN_ATLAS + CYTO_CONFERENCE
        text += link_text.format(*LINKS)
        text += instructions
        print(text)
        readme.write(text)


def main():
    """Run main."""
    gen_md()


if __name__ == '__main__':
    main()
