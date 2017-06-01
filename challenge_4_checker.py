import argparse
import csv


def parseargs():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument('submitted_answer')
    parser.add_argument('solution_key')
    parser.add_argument('-n', '--new', action='append',
                        help=('Specify novel class. '
                              'Can be used multiple times'))
    args = parser.parse_args()
    return args.submitted_answer, args.solution_key, args.new


def read_novel_classes(submitted, solution, novel_classes):
    for line in csv.reader(open(solution)):
        id_ = line[0]
        classes = {x.strip() for x in line[1:]}

        if any(x in classes for x in novel_classes):
            print('yay')


def main():
    submitted_answer, solution_key, novel_classes = parseargs()
    read_novel_classes(submitted_answer, solution_key, novel_classes)

if __name__ == '__main__':
    main()
