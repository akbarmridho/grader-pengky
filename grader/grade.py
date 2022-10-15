import subprocess
from subprocess import run
from typing import List

from grader.cases import TestCase, TestResult  # type: ignore


def grade_case(file: str, test_case: TestCase) -> TestResult:
    try:
        case_input = "".join([each + "\n" for each in test_case["inputs"]])
        process = run(["python", file], input=case_input,
                      encoding="utf-8", stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                      timeout=1)

        start_idx = 0

        for i in range(len(test_case['inputs'])):
            result = process.stdout.find(":", start_idx)
            if result == -1:
                raise Exception(
                    f"Invalid amount of :. Expected {len(test_case['inputs'])} found {i}")
            start_idx = result + 1

        output = process.stdout[start_idx:]
        # splitted = process.stdout.splitlines()

        # output = splitted[-1].split(":")[-1].strip()

        # if output == "" or output == "\n":
        # output = splitted[-2]

        if not output:
            output = f"Empty string result. Stacktrace:\n{process.stdout}"

        valid, expected = test_case["expect"](output)

        return TestResult(expect=expected, got=output, valid=valid)

    except Exception as e:
        return TestResult(expect="Program runnable", got=f"Returned {e}\n", valid=False)


def grade_file(file: str, cases: List[TestCase]):
    outfile = file[:-3] + "_result.txt"

    valid_count = 0

    with open(outfile, "w") as f:
        for i in range(len(cases)):
            result = grade_case(file, cases[i])
            f.write(20*"=" + "\n")
            f.write(f"Test Case {i+1}\n")

            f.write("Input: " + " ".join(cases[i]["inputs"]) + "\n")

            f.write(
                f'Expected: {result["expect"]}\nGot: {result["got"]}\n')

            if result["valid"]:
                f.write("VALID\n")
                valid_count += 1
            else:
                f.write("NOT VALID\n")

            f.write(20*"=" + "\n")

        f.write(f"Valid {valid_count} out of {len(cases)}")
