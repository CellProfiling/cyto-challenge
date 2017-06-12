"""Calculate score for answers."""
import argparse
import csv
import sys
import collections

from gen_markdown import CHALLENGE_1

PREC = 'prec'
REC = 'rec'
TRUE_POS = 'tp'
FALSE_POS = 'fp'
FALSE_NEG = 'fn'


class ScoreError(Exception):
    """Error raised when the solution checker fails."""

    pass


def calculate_and_print_score(f1_score, precision, recall):
    """Calculate and print score."""
    fin_f_score = 0.0
    fin_r_score = 0.0
    fin_p_score = 0.0

    for key in f1_score:
        if key in f1_score:
            fin_f_score += f1_score[key]
        if key in recall:
            fin_r_score += recall[key][REC]
        if key in precision:
            fin_p_score += precision[key][PREC]
    fin_f_score /= len(f1_score)
    fin_r_score /= len(f1_score)
    fin_p_score /= len(f1_score)

    print('Recall:', fin_r_score)
    print('Precision:', fin_p_score)
    print('F1 score:', fin_f_score)
    return fin_r_score, fin_p_score, fin_f_score


def parseargs():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument('submitted_answer')
    parser.add_argument('solution_key')
    parser.add_argument(
        '-c', '--challenge', dest='challenge', type=str,
        help='the challenge name')
    args = parser.parse_args()
    return args.submitted_answer, args.solution_key, args.challenge


def read_key_file(f_path):
    """Read key file."""
    ids = {}
    try:
        with open(f_path, 'r') as fil:
            for line in csv.reader(fil):
                id_ = line[0].strip()
                classes = [x.strip() for x in line[1:]]
                ids[id_] = classes
        return ids
    except IndexError:
        print(('Expected input on format "ID, class1, ...\\n" but'
               'recieved', ''.join(line)), file=sys.stderr)
        raise ScoreError(
            'Expected input on format "ID, class1, ...\\n" but'
            'recieved {}'.format(''.join(line)))
    except FileNotFoundError:
        assert isinstance(f_path, str)
        print('Could not find the file', f_path, file=sys.stderr)
        raise ScoreError('Could not find the file {}'.format(f_path))
    except AssertionError:
        print('Not a valid filename', file=sys.stderr)
        raise ScoreError('Not a valid filename')


def calc_precision(submitted, solution):
    """Calculate precision."""
    precision = collections.defaultdict(lambda: {TRUE_POS: 0, FALSE_POS: 0})
    for sub in submitted:
        sub_key = submitted[sub]
        sol_key = solution.get(sub)
        if sol_key is None:
            print(sub, 'could not be found in solution key', file=sys.stderr)
            raise ScoreError(
                '{} could not be found in solution key'.format(sub))

        for key in sub_key:
            if key in sol_key:
                precision[key][TRUE_POS] += 1
            else:
                precision[key][FALSE_POS] += 1
    for key in precision:
        tp_prec = precision[key][TRUE_POS]
        fp_prec = precision[key][FALSE_POS]
        precision[key][PREC] = tp_prec / (tp_prec + fp_prec)
    return dict(precision)


def calc_recall(submitted, solution):
    """Calculate recall."""
    recall = collections.defaultdict(lambda: {TRUE_POS: 0, FALSE_NEG: 0})
    for sub in submitted:
        sub_key = submitted[sub]
        sol_key = solution.get(sub)
        if sol_key is None:
            print(sub, 'could not be found in solution key', file=sys.stderr)
            raise ScoreError(
                '{} could not be found in solution key'.format(sub))

        for key in sol_key:
            if key in sub_key:
                recall[key][TRUE_POS] += 1
            else:
                recall[key][FALSE_NEG] += 1

    for key in recall:
        tp_recall = recall[key][TRUE_POS]
        fn_recall = recall[key][FALSE_NEG]
        recall[key][REC] = tp_recall / (tp_recall + fn_recall)
    return dict(recall)


def calc_f1_score(precision, recall):
    """Calculate f1 score."""
    f1_score = collections.defaultdict(float)
    for key in precision:
        prec = precision[key][PREC]
        if key in recall:
            rec = recall[key][REC]
        else:
            rec = 0
        f1_score[key] = 2 * ((prec * rec) / ((prec + rec) or 1.0))
    return dict(f1_score)


def score_1(submitted, solution):
    """Slice dicts and return only nui, mito and nui+mito."""
    nui_mito_sol = {
        idx: classes for idx, classes in solution.items()
        if ['Nucleoli'] == classes
        or ['Mitochondria'] == classes
        or ['Mitochondria', 'Nucleoli'] == sorted(classes)}
    nui_mito_sub = {
        idx: classes for idx, classes in submitted.items()
        if idx in nui_mito_sol}
    return nui_mito_sub, nui_mito_sol


def score(submitted_answer, solution_key, challenge=None):
    """Score the submitted answer."""
    submitted = read_key_file(submitted_answer)
    solution = read_key_file(solution_key)
    if challenge == CHALLENGE_1:
        submitted, solution = score_1(submitted, solution)

    if len(submitted) != len(solution):
        print('Differring number of answers and solutions', file=sys.stderr)
        print('Num answers: {}, Num solutions: {}'.format(
            len(submitted), len(solution), file=sys.stderr))
        raise ScoreError()

    precision = calc_precision(submitted, solution)
    recall = calc_recall(submitted, solution)
    f1_score = calc_f1_score(precision, recall)
    return calculate_and_print_score(f1_score, precision, recall)


def main():
    """Calculate score for answer."""
    submitted_answer, solution_key, challenge = parseargs()
    score(submitted_answer, solution_key, challenge)


if __name__ == '__main__':
    main()
