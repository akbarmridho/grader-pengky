import subprocess
from subprocess import run
from typing import List

from grader.cases import TestCase, TestResult  # type: ignore


def grade_case(file: str, test_case: TestCase) -> TestResult:
    try:
        case_input = "".join([each + "\n" for each in test_case["inputs"]])
        process = run(["python", file], input=case_input,
                      encoding="utf-8", stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        splitted = process.stdout.splitlines()
        output = splitted[-1].split(":")[-1].strip()

        # if output == "" or output == "\n":
        # output = splitted[-2]

        valid, expected = test_case["expect"](output)

        return TestResult(expect=expected, got=output, valid=valid)

    except subprocess.CalledProcessError as exc:
        return TestResult(expect="Program runnable", got=f"Returned {exc.returncode}\n{exc}", valid=False)


def grade_file(file: str, cases: List[TestCase]):
    outfile = file[:-3] + "_result.txt"

    valid_count = 0

    with open(outfile, "w") as f:
        for i in range(len(cases)):
            result = grade_case(file, cases[i])
            f.write(f"Test Case {i+1}\n")

            f.write(
                f'Expected: {result["expect"]}\nGot: {result["got"]}\n')

            if result["valid"]:
                f.write("VALID\n")
                valid_count += 1

        f.write(f"Valid {valid_count} out of {len(cases)}")
