import os
from multiprocessing import Pool
from pathlib import Path

import MeCab
from more_itertools import divide

IN = Path("./in.txt")
OUT = Path("./out.txt")


def run(text_iter):
    mecab = MeCab.Tagger("-Owakati")
    results = []

    for line in text_iter:
        line: str = mecab.parse(line.strip()).strip()
        if not line.isspace():
            results.append(line)

    return results


def main():
    num_procs = os.cpu_count()
    with IN.open() as f, OUT.open("w") as w:
        with Pool(processes=num_procs) as pool:
            for sentences in pool.map(run, divide(num_procs, f)):
                w.write("".join(f"{s}\n" for s in sentences))


if __name__ == "__main__":
    main()
