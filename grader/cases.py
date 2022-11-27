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
    },
    "H03": {
        "01": [
            TestCase(inputs=["4", "abcd"],
                     expect=lambda x: validate(x, ["dcba"])),
            TestCase(inputs=["7", "TuanKil"],
                     expect=lambda x: validate(x, ["liKnauT"]))
        ],
        "02": [
            TestCase(inputs=["5", "4", "3", "1", "0", "2"],
                     expect=lambda x: validate(x, string_contain=["berbeda"], string_not_contain=["tidak"])),
            TestCase(inputs=["4", "3", "17", "17", "100"],
                     expect=lambda x: validate(x, ["tidak"]))
        ],
        "03": [
            TestCase(inputs=["8", "institut", "5", "utara"],
                     expect=lambda x: validate(x, ["dapat", "'ut'"], string_not_contain=["tidak"])),
            TestCase(inputs=["6", "fisika", "5", "kimia"],
                     expect=lambda x: validate(x, ["tidak"]))
        ]
    },
    "P03": {
        "01": [
            TestCase(inputs=["20", "UUUUUDDDDDLLLLLRRFGD"],
                     expect=lambda x: validate(x, ["(-3,-1)"])),
            TestCase(inputs=["12", "RLUDDMNOPZUG"],
                     expect=lambda x: validate(x, ["(0,0)"])),
            TestCase(inputs=["10", "DDDUULLRRR "],
                     expect=lambda x: validate(x, ["(1,-1)"])),
            TestCase(inputs=["17", "LLLLLLLLLLLLLLLLL"],
                     expect=lambda x: validate(x, ["(-17,0)"]))
        ],
        "02": [
            TestCase(inputs=["1", "1920"],
                     expect=lambda x: validate(x, ["1920"])),
            TestCase(inputs=["6", "11", "4", "22", "9", "29", "17"],
                     expect=lambda x: validate(x, ["1482"])),
            TestCase(inputs=["8", "2", "1", "2", "1", "2", "1", "2", "1"],
                     expect=lambda x: validate(x, ["495"])),
            TestCase(inputs=["4", "1", "2", "3", "4"],
                     expect=lambda x: validate(x, ["49"]))
        ],
        "03": [
            TestCase(inputs=["12", "011101100111"],
                     expect=lambda x: validate(x, ["5"])),
            TestCase(inputs=["9", "111111111"],
                     expect=lambda x: validate(x, ["8"])),
            TestCase(inputs=["10", "1110001111"],
                     expect=lambda x: validate(x, ["4"])),
            TestCase(inputs=["33", "001101101101110101011101110110101"],
                     expect=lambda x: validate(x, ["6"]))
        ]
    },
    "H04": {
        "01": [
            TestCase(inputs=["3", "2", "3", "1", "2", "3", "4", "5", "6", "3", "2", "1", "4", "2", "5", "3", "6"],
                     expect=lambda x: validate(x, ["adalah"], string_not_contain=["bukan"])),
            TestCase(inputs=["3", "2", "2", "1", "2", "3", "4", "2", "2", "1", "4", "2", "3"],
                     expect=lambda x: validate(x, ["bukan"])),
            TestCase(inputs=["3", "3", "2", "1", "2", "3", "4", "5", "6", "3", "2", "1", "4", "2", "5", "3", "6"],
                     expect=lambda x: validate(x, ["bukan"]))
        ],
        "02": [
            TestCase(inputs=["3", "0 2 0", "-5 -2 1", "3 -1 6", "1", "2", "3", "3"],
                     expect=lambda x: validate(x, string_contain=["9"])),
            TestCase(inputs=["2", "2 1", "0 1", "1", "1", "2", "2"],
                     expect=lambda x: validate(x, ["4"])),
            TestCase(inputs=["2", "2", "1", "0", "1", "1", "1", "2", "2"],
                     expect=lambda x: validate(x, ["4"])),
            TestCase(inputs=["3", "0", "2", "0", "-5", "-2", "1", "3", "-1", "6", "1", "2", "3", "3"],
                     expect=lambda x: validate(x, string_contain=["9"]))
        ],
        "03": [
            TestCase(inputs=["3", "4", "5"],
                     expect=lambda x: validate(x, [], number=361.35328)),
            TestCase(inputs=["2", "5", "1"],
                     expect=lambda x: validate(x, [], number=1812.0)),
            TestCase(inputs=["10", "100", "5"],
                     expect=lambda x: validate(x, [], number=2186650242.0)),
        ]
    },
    "P04": {
        "01": [
            TestCase(inputs=["-2", "10"],
                     expect=lambda x: validate(x, ["29"])),
            TestCase(inputs=["0", "100"],
                     expect=lambda x: validate(x, ["-67108862"])),
            TestCase(inputs=["1", "0"],
                     expect=lambda x: validate(x, ["1"])),
            TestCase(inputs=["100", "99"],
                     expect=lambda x: validate(x, ["-3422552061"])),
        ],
        "02": [
            TestCase(inputs=["3", "4", "0 1 2 0", "1 0 0 0", "0 0 0 0"],
                     expect=lambda x: validate(x, ["sesuai"], string_not_contain=["tidak"])),
            TestCase(inputs=["3", "4", "0 0 0 0", "0 1 0 0", "0 0 1 0"],
                     expect=lambda x: validate(x, ["tidak"])),
            TestCase(inputs=["2", "3", "1 2 3", "0 2 0"],
                     expect=lambda x: validate(x, ["tidak"])),
            TestCase(inputs=["2", "3", "1 2 3", "1 2 0"],
                     expect=lambda x: validate(x, ["tidak"])),
            TestCase(inputs=["3", "4", "0", "1", "2", "0", "1", "0", "0", "0", "0", "0", "0", "0"],
                     expect=lambda x: validate(x, ["sesuai"], string_not_contain=["tidak"])),
            TestCase(inputs=["3", "4", "0", "0", "0", "0", "0", "1", "0", "0", "0", "0", "1", "0"],
                     expect=lambda x: validate(x, ["tidak"])),
            TestCase(inputs=["2", "3", "1", "2", "3", "0", "2", "0"],
                     expect=lambda x: validate(x, ["tidak"])),
            TestCase(inputs=["2", "3", "1", "2", "3", "1", "2", "0"],
                     expect=lambda x: validate(x, ["tidak"]))
        ],
        "03": [
            TestCase(inputs="3 9 -8 7 -6 5 -4 3 2 1".split(" ") + ["kolom", "2", "7", "3", "exit"],
                     expect=lambda x: validate(x, ["3 1 2"])),
            TestCase(inputs="3 1 2 3 4 5 6 7 8 9".split(" ") + ["ce", "baris", "4", "3", "1", "kolom", "1", "2", "exit"],
                     expect=lambda x: validate(x, ["2 1 3"])),
            TestCase(inputs="2 2 3 4 5 baris 1 3 2 kolom 2 1 baris 2 2 exit".split(" "),
                     expect=lambda x: validate(x, ["3 2"])),
            TestCase(inputs="3 8 -7 0 0 2 3 5 6 9 exit".split(" "),
                     expect=lambda x: validate(x, ["5 6 9"])),
        ]
    }
}
