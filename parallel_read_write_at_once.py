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

    with IN.open("rb") as f, tempfile.NamedTemporaryFile(mode="w", delete=False) as tmp:
        f.seek(start)

        results = []
        for byte in f.read(end - start).splitlines():
            line: str = mecab.parse(byte.decode().strip()).strip()
            if not line.isspace():
                results.append(line)

        tmp.write("".join(f"{line}\n" for line in results))
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
        paths = [f'"{path}"' for path in pool.starmap(run, chunks)]
        cmd = f"cat {' '.join(paths)} > {OUT}"
        subprocess.call(cmd, shell=True)


if __name__ == "__main__":
    main()
