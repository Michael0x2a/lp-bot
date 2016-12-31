import CommonMark

sample2 = """
Hello world!

    this is a code sample

Some `inline code`

- List 1
- List 2
"""


def extract(text: str) -> None:
    parser = CommonMark.Parser()
    ast = parser.parse(text)
    #print(CommonMark.dumpAST(ast))
    print(CommonMark.dumpJSON(ast))


def main() -> None:
    with open("sample.txt", "r") as stream:
        sample = stream.read()
    extract(sample2)


if __name__ == '__main__':
    main()

