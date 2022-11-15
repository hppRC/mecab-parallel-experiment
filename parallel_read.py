import os
from multiprocessing import Pool
from pathlib import Path

import MeCab

IN = Path("./in.txt")
OUT = Path("./out.txt")


def run(start: int, end: int):
    mecab = MeCab.Tagger("-Owakati")
    results = []

    current = start
    with IN.open() as f:
        f.seek(start)

        for line in f:
            current += len(line.encode())
            line: str = mecab.parse(line.strip()).strip()

            if not line.isspace():
                results.append(line)

            if current >= end:
                break

    return results


def main():
    file_size = IN.stat().st_size
    num_procs = os.cpu_count()

    chunk_size = file_size // num_procs
    chunks = []
    start, end = 0, chunk_size

    with IN.open(encoding="utf-8", errors="ignore") as f:
        while end < file_size:
            f.seek(end)
            f.readline()

            end = f.tell()
            chunks.append((start, end))
            start, end = end, end + chunk_size

        chunks.append((start, file_size))

    with OUT.open("w") as out:
        with Pool(processes=num_procs) as pool:
            for sentences in pool.starmap(run, chunks):
                out.write("\n".join(sentences) + "\n")


if __name__ == "__main__":
    main()
