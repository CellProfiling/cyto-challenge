from collections import defaultdict
from solution_checker import *
import argparse
import csv
import sys


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
    parser.add_argument('-n', '--new', action='append',
                        help=('Specify novel class. '
                              'Can be used multiple times'))
    args = parser.parse_args()
    return args.submitted_answer, args.solution_key, set(args.new)


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

        for c in solution_classes:
            for d in submitted_classes:
                submitted_to_novel[d][c] += 1

    # I am aware that this is fugly, but it works
    # translates the classes submitted by the competitor into the novel class
    # that is present the most times for that unknown class.
    # If for example the class UC1 has been applied to the class A twice and
    # the class B once, UC1 will be translated to A in every instance.
    for d in submitted_to_novel:
        max_ = -1
        current = ''
        for c in submitted_to_novel[d]:
            if submitted_to_novel[d][c] > max_:
                max_ = submitted_to_novel[d][c]
                current = c
        occupied.add(current)
        submitted_translation[d] = current

    for sub_classes in submitted.values():
        for i, c in enumerate(sub_classes):
            if c in submitted_translation:
                sub_classes[i] = submitted_translation[c]

    return submitted


def main():
    submitted_answer, solution_key, novel_classes = parseargs()

    submitted = read_key_file(submitted_answer)
    solution = read_key_file(solution_key)

    known_classes = get_known_classes(solution, novel_classes)
    novel = get_novel_ids(solution, novel_classes)

    translated_submitted = translate_unknowns(submitted, novel, known_classes)

    # From here, most of the code for rare classes can be used
    precision = calc_precision(translated_submitted, solution)
    recall = calc_recall(translated_submitted, solution)
    f1_score = calc_f1_score(precision, recall)
    calculate_and_print_score(f1_score, precision, recall)


if __name__ == '__main__':
    main()
