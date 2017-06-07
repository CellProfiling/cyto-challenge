"""Calculate score fow answers to challenge 4."""
import argparse
import sys
from collections import defaultdict

from solution_checker import (ScoreError, calc_f1_score, calc_precision,
                              calc_recall, calculate_and_print_score,
                              read_key_file)

PREC = 'prec'
REC = 'rec'
TRUE_POS = 'tp'
FALSE_POS = 'fp'
FALSE_NEG = 'fn'


def parseargs():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument('submitted_answer')
    parser.add_argument('solution_key')
    parser.add_argument('new_classes',
                        help='Specify path to novel classes in a csv file.')
    args = parser.parse_args()
    return args.submitted_answer, args.solution_key, args.new_classes


def get_known_classes(solution, novel_classes):
    """Gets all classes that the challengers should already know"""
    known_classes = set()
    for classes in solution.values():
        for class_ in classes:
            if class_ in novel_classes:
                continue
            known_classes.add(class_)
    return known_classes


def get_novel_ids(solution, novel_classes):
    """Gets all ids with novel classes, and their full annotations"""
    novel = {}
    for id_ in solution:
        classes = solution[id_]
        if any(x in classes for x in novel_classes):
            novel[id_] = set(classes)
    return novel


def translate_unknowns(submitted, novel, known_classes):
    """Translate unknown classes."""
    submitted_to_novel = defaultdict(lambda: defaultdict(int))
    submitted_translation = {}
    occupied = set()
    for id_ in novel:
        submitted_classes = submitted.get(id_)
        if submitted_classes is None or submitted_classes[0] == '':
            print('%s has a bad input line' % id_)
            raise ScoreError()

        submitted_classes = set(submitted_classes) - known_classes
        solution_classes = novel[id_] - known_classes

        for sol_cls in solution_classes:
            for sub_cls in submitted_classes:
                submitted_to_novel[sub_cls][sol_cls] += 1

    # I am aware that this is fugly, but it works
    # translates the classes submitted by the competitor into the novel class
    # that is present the most times for that unknown class.
    # If for example the class UC1 has been applied to the class A twice and
    # the class B once, UC1 will be translated to A in every instance.
    for sub_cls in submitted_to_novel:
        max_ = -1
        current = ''
        for cls_ in submitted_to_novel[sub_cls]:
            if submitted_to_novel[sub_cls][cls_] > max_:
                max_ = submitted_to_novel[sub_cls][cls_]
                current = cls_
        occupied.add(current)
        submitted_translation[sub_cls] = current

    for sub_classes in submitted.values():
        for i, cls_ in enumerate(sub_classes):
            if cls_ in submitted_translation:
                sub_classes[i] = submitted_translation[cls_]

    return submitted


def score_4(submitted_answer, solution_key, novel_classes):
    """Score challenge 4."""
    submitted = read_key_file(submitted_answer)
    solution = read_key_file(solution_key)
    if len(submitted) != len(solution):
        print('Differring number of answers and solutions', file=sys.stderr)
        print('Num answers: {}, Num solutions: {}'.format(
            len(submitted), len(solution), file=sys.stderr))
        raise ScoreError()
    novel_classes = read_key_file(novel_classes)
    novel_classes = [
        class_ for row in novel_classes.values() for class_ in row]

    known_classes = get_known_classes(solution, novel_classes)
    novel = get_novel_ids(solution, novel_classes)

    translated_submitted = translate_unknowns(submitted, novel, known_classes)

    # From here, most of the code for rare classes can be used
    precision = calc_precision(translated_submitted, solution)
    recall = calc_recall(translated_submitted, solution)
    f1_score = calc_f1_score(precision, recall)
    return calculate_and_print_score(f1_score, precision, recall)


def main():
    """Run main."""
    submitted_answer, solution_key, novel_classes = parseargs()
    score_4(submitted_answer, solution_key, novel_classes)


if __name__ == '__main__':
    main()
