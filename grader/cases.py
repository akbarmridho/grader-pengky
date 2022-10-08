from typing import Callable, List, Tuple, TypedDict

validator = Callable[[str], Tuple[bool, str]]


def validate(to_compare: str, string_contain: List[str], number: int | float | None = None) -> Tuple[bool, str]:
    valid = True
    to_compare = to_compare.lower()
    output = ""

    for sub in string_contain:
        output += sub + " "
        if sub.lower() not in to_compare:
            valid = False

    number_found = False

    for sub in to_compare.split(" "):
        try:
            if type(number) is int:
                intval = int(sub)
                number_found = True
                output += sub + " "
                if intval != number:
                    valid = False
            elif type(number) is float:
                fval = float(sub)
                number_found = True
                output += sub + " "
                fval = fval.__round__(2)
                if fval != number:
                    valid = False
        except ValueError:
            continue

    if number is not None and not number_found:
        valid = False

    return valid, output.strip()


class TestCase(TypedDict):
    inputs: List[str]
    expect: validator


class TestResult(TypedDict):
    expect: str
    got: str
    valid: bool


cases = {
    "H01": {
        "01": [
            TestCase(
                inputs=["10", "15", "10", "12", "10", "11"],
                expect=lambda x: validate(x, ["barang A"])
            ),
            TestCase(
                inputs=["8", "11", "7", "12", "6", "12"],
                expect=lambda x: validate(x, ["barang C"])
            )
        ],
        "02": [
            TestCase(
                inputs=["121"],
                expect=lambda x: validate(x, ["K3"])
            ),
            TestCase(
                inputs=["544"],
                expect=lambda x: validate(x, ["K8"])
            )
        ],
        "03": [
            TestCase(
                inputs=["10", "00", "00", "10", "14", "55"],
                expect=lambda x: validate(x, ["14 menit 55 detik"])
            ),
            TestCase(
                inputs=["19", "55", "20", "21", "14", "05"],
                expect=lambda x: validate(x, ["1 jam 18 menit 45 detik"])
            )
        ]
    },
    "P01": {
        "01": [
            TestCase(
                inputs=["80", "90", "100"],
                expect=lambda x: validate(x, ["minimum", "diperlukan"], 51.43)
            ),
            TestCase(
                inputs=["20", "85", "50"],
                expect=lambda x: validate(x, ["tidak", "mungkin"])
            ),
            TestCase(
                inputs=["35", "70", "70"],
                expect=lambda x: validate(x, ["tidak", "mungkin"])
            ),
            TestCase(
                inputs=["40", "90", "90"],
                expect=lambda x: validate(x, ["minimum", "diperlukan"], 97.14)
            ),
        ],
        "02": [
            TestCase(
                inputs=["400", "3"],
                expect=lambda x: validate(x, ["324000000"])
            ),
            TestCase(
                inputs=["925", "5"],
                expect=lambda x: validate(x, ["1774150000"])
            ),
            TestCase(
                inputs=["5000", "4"],
                expect=lambda x: validate(x, ["7450000000"])
            ),
            TestCase(
                inputs=["250", "3"],
                expect=lambda x: validate(x, ["121500000"])
            )
        ],
        "03": [
            TestCase(
                inputs=["12", "8", "4"],
                expect=lambda x: validate(x, ["berkesempatan"])
            ),
            TestCase(
                inputs=["12", "8", "0"],
                expect=lambda x: validate(x, ["tidak"])
            ),
            TestCase(
                inputs=["13", "16", "3"],
                expect=lambda x: validate(x, ["berkesempatan"])
            ),
            TestCase(
                inputs=["30", "18", "0"],
                expect=lambda x: validate(x, ["berkesempatan"])
            )
        ]
    }
}
