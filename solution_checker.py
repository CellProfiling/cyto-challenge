import argparse
import csv
import sys
import collections


def parseargs():
    parser = argparse.ArgumentParser()
    parser.add_argument('submitted_answer')
    parser.add_argument('solution_key')
    parser.add_argument('-i', '--include', action='append',
                        help=('Inlcude the specified class. '
                              'Can be used multiple times'))
    args = parser.parse_args()
    return args.submitted_answer, args.solution_key, args.include


def read_key_file(f_path):
    ids = {}
    try:
        with open(f_path, 'r') as f:
            for line in csv.reader(f):
                id_ = line[0].strip()
                classes = [x.strip() for x in line[1:]]
                ids[id_] = classes
        return ids
    except IndexError:
        print(('Expected input on format "ID, class1, ...\\n" but'
               'recieved ' + ''.join(line)), file=sys.stderr)
        sys.exit(-1)
    except FileNotFoundError:
        assert isinstance(f_path, str)
        print('Could not find the file ' + f_path, file=sys.stderr)
        sys.exit(-1)
    except AssertionError:
        print('Not a valid filename', file=sys.stderr)
        sys.exit(-1)


def calc_precision(submitted, solution):
    precision = collections.defaultdict(lambda: {'tp': 0, 'fp': 0})
    for sub in submitted:
        sub_key = submitted[sub]
        try:
            sol_key = solution[sub]
        except:
            print(sub + ' Could not be found in solution key', file=sys.stderr)

        for key in sub_key:
            if key in sol_key:
                precision[key]['tp'] += 1
            else:
                precision[key]['fp'] += 1
    for key in precision:
        tp = precision[key]['tp']
        fp = precision[key]['fp']
        precision[key]['prec'] = tp/(tp + fp)
    return dict(precision)


def calc_recall(submitted, solution):
    recall = collections.defaultdict(lambda: {'tp': 0, 'fn': 0})
    for sub in submitted:
        sub_key = submitted[sub]
        try:
            sol_key = solution[sub]
        except:
            print(sub + ' Could not be found in solution key', file=sys.stderr)

        for key in sol_key:
            if key in sub_key:
                recall[key]['tp'] += 1
            else:
                recall[key]['fn'] += 1

    for key in recall:
        tp = recall[key]['tp']
        fn = recall[key]['fn']
        recall[key]['rec'] = tp/(tp + fn)
    return dict(recall)


def calc_f1_score(precision, recall):
    f1_score = collections.defaultdict(float)
    for key in precision:
        prec = precision[key]['prec']
        if key in recall:
            rec = recall[key]['rec']
        else:
            rec = 0
        f1_score[key] = 2 * ((prec * rec) / ((prec + rec) or 1.0))
    return dict(f1_score)


def main():
    submitted_answer, solution_key, include_classes = parseargs()
    submitted = read_key_file(submitted_answer)
    solution = read_key_file(solution_key)

    if len(submitted) != len(solution):
        print('Differring number of answers and solutions', file=sys.stderr)
        print('Num answers: {}, Num solutions: {}'.format(
              len(submitted), len(solution), file=sys.stderr))

    precision = calc_precision(submitted, solution)
    recall = calc_recall(submitted, solution)
    f1_score = calc_f1_score(precision, recall)
    fs = 0.0
    rs = 0.0
    ps = 0.0
    if include_classes:
        keys = include_classes
    else:
        keys = f1_score.keys()

    for key in keys:
        if key not in f1_score:
            print(key, 'not in the available keys', file=sys.stderr)
            sys.exit(-1)

        fs += f1_score[key]
        try:
            rs += recall[key]['rec']
        except:
            pass
        try:
            ps += precision[key]['prec']
        except:
            pass
    fs /= len(f1_score)
    rs /= len(f1_score)
    ps /= len(f1_score)

    print('Recall:', rs)
    print('Precision:', ps)
    print('F1 score:', fs)


if __name__ == '__main__':
    main()
