from pathlib import Path
from grader.grade import grade_file
from grader.utils.dir import get_files
from grader.cases import cases

if __name__ == '__main__':
    for each in get_files("test"):
        filename = Path(each).name

        problem_set = filename[:3]
        problem_number = filename.split("_")[-1][-5:-3]

        case_set = cases[problem_set][problem_number]

        grade_file(each, case_set)
