import os
import subprocess
import tempfile
from multiprocessing import Pool
from pathlib import Path

import MeCab

IN = Path("./in.txt")
OUT = Path("./out.txt")


def run(start: int, end: int):
    mecab = MeCab.Tagger("-Owakati")
    current = start

    with IN.open() as f, tempfile.NamedTemporaryFile(mode="w", delete=False) as tmp:
        f.seek(start)

        for line in f:
            current += len(line.encode())
            line: str = mecab.parse(line.strip()).strip()

            if not line.isspace():
                tmp.write(f"{line}\n")

            if current >= end:
                break

        return tmp.name


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

    with Pool(processes=num_procs) as pool:
        paths = list(pool.starmap(run, chunks))
        paths_cat = [f'"{path}"' for path in paths]
        cmd = f"cat {' '.join(paths_cat)} > {OUT}"
        subprocess.call(cmd, shell=True)
        for path in paths:
            os.remove(path)


if __name__ == "__main__":
    main()
