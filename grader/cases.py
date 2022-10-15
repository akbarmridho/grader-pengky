from typing import Callable, List, Tuple, TypedDict

validator = Callable[[str], Tuple[bool, str]]


def validate(to_compare: str, string_contain: List[str], number: int | float | None = None, string_not_contain: List[str] | None = None) -> Tuple[bool, str]:
    valid = True
    to_compare = to_compare.lower()
    output = ""

    for sub in string_contain:
        output += sub + " "
        if sub.lower() not in to_compare:
            valid = False

    if valid and string_not_contain is not None:
        for sub in string_not_contain:
            output += f"(not contain) {sub} "
            if sub.lower() in to_compare:
                valid = False

    number_found = False

    if number is not None:
        output += number.__str__() + " "

    for sub in to_compare.split(" "):
        try:
            if type(number) is int:
                intval = int(sub)
                number_found = True

                if intval != number:
                    valid = False
            elif type(number) is float:
                fval = float(sub)
                number_found = True

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
    },
    "H02": {
        "01": [
            TestCase(
                inputs=["12", "2", "3", "4"],
                expect=lambda x: validate(
                    x, ["1 Siap Bang SiapJago 5 SiapBang 7 SiapJago Bang Siap 11 SiapBangJago"])
            ),
            TestCase(
                inputs=["5", "1", "1", "1"],
                expect=lambda x: validate(
                    x, ["SiapBangJago SiapBangJago SiapBangJago SiapBangJago SiapBangJago"])
            )
        ],
        "02": [
            TestCase(
                inputs=["4", "7"],
                expect=lambda x: validate(x, ["adalah 2", "adalah 7"])
            ),
            TestCase(
                inputs=["2", "2"],
                expect=lambda x: validate(x, ["adalah 1", "adalah 2"])
            ),
            TestCase(
                inputs=["1", "1"],
                expect=lambda x: validate(x, ["tidak ditemukan"])
            )
        ],
        "03": [
            TestCase(
                inputs=["7"],
                expect=lambda x: validate(x, ["7"])
            ),
            TestCase(
                inputs=["13"],
                expect=lambda x: validate(x, ["111111"])
            ),
            TestCase(
                inputs=["259"],
                expect=lambda x: validate(x, ["777"])
            )
        ]
    },
    "P02": {
        "01": [
            TestCase(inputs=["10", "8", "15", "100", "10"],
                     expect=lambda x: validate(x, ["75"])),
            TestCase(inputs=["5", "6", "7", "2022", "2023"],
                     expect=lambda x: validate(x, ["97"])),
            TestCase(inputs=["1", "2", "3", "4", "5"],
                     expect=lambda x: validate(x, ["1"])),
            TestCase(inputs=["1000", "1001", "1002", "2001", "2002"],
                     expect=lambda x: validate(x, ["862"]))
        ],
        "02": [
            TestCase(inputs=["3", "5", "75"],
                     expect=lambda x: validate(x, ["dapat"], string_not_contain=["tidak"])),
            TestCase(inputs=["4", "5", "320"],
                     expect=lambda x: validate(x, ["tidak"])),
            TestCase(inputs=["2", "3", "30"],
                     expect=lambda x: validate(x, ["tidak"])),
            TestCase(inputs=["5", "10", "2500"],
                     expect=lambda x: validate(x, ["dapat"], string_not_contain=["tidak"]))
        ],
        "03": [
            TestCase(inputs=["3", "3", "3", "3"],
                     expect=lambda x: validate(x, ["7 10 13"])),
            TestCase(inputs=["5", "4", "8", "9"],
                     expect=lambda x: validate(x, ["29 34 39 44 49 54 59 64 69"])),
            TestCase(inputs=["1", "1", "5", "5"],
                     expect=lambda x: validate(x, ["5 6 7 8 9"])),
            TestCase(inputs=["0", "0", "2", "2"],
                     expect=lambda x: validate(x, ["1 1"]))
        ]
    }
}
