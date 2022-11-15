from pathlib import Path

import MeCab

IN = Path("./in.txt")
OUT = Path("./out.txt")


def main():
    mecab = MeCab.Tagger("-Owakati")

    with IN.open() as f, OUT.open("w") as out:
        for line in f:
            line: str = mecab.parse(line.strip()).strip()
            if not line.isspace():
                out.write(f"{line}\n")


if __name__ == "__main__":
    main()
