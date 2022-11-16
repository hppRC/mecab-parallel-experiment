import os
import subprocess
import tempfile
from multiprocessing import Pool
from pathlib import Path
from typing import Callable, List, Optional, TypeVar, Union

T = TypeVar("T")
Fn = Callable[[str], Optional[T]]


def run_and_return(
    input_path: Path,
    fn: Fn,
    start: int,
    end: int,
) -> List[T]:
    results = []
    current = start
    with input_path.open() as f:
        f.seek(start)
        for line in f:
            current += len(line.encode())
            ret: T = fn(line.strip())
            if ret is not None:
                results.append(ret)
            if current >= end:
                break

    return results


def run_and_save(
    input_path: Path,
    fn: Fn,
    start: int,
    end: int,
) -> List[T]:
    current = start
    with input_path.open() as f, tempfile.NamedTemporaryFile(mode="w", delete=False) as tmp:
        for line in f:
            current += len(line.encode())
            ret: T = fn(line.strip())

            if ret is not None:
                tmp.write(f"{str(ret)}\n")

            if current >= end:
                break

        return tmp.name


def generate_file_chunks(input_path: Path, num_chunks: int):
    file_size = input_path.stat().st_size

    chunk_size = file_size // num_chunks
    start, end = 0, chunk_size

    with input_path.open(encoding="utf-8", errors="ignore") as f:
        while end < file_size:
            f.seek(end)
            f.readline()

            end = f.tell()
            yield (start, end)
            start, end = end, end + chunk_size

        yield (start, file_size)


def process_file_parallel(
    input_path: Union[str, Path],
    fn: Fn,
    num_procs: int = None,
) -> List[T]:
    input_path: Path = Path(input_path)
    num_procs: int = num_procs or os.cpu_count()

    with Pool(processes=num_procs) as pool:
        chunks = [
            (input_path, fn, start, end)
            for start, end in generate_file_chunks(input_path, num_chunks=num_procs)
        ]
        return list(zip(*pool.starmap(run_and_return, chunks)))


def process_file_parallel_and_save(
    input_path: Union[str, Path],
    output_path: Union[str, Path],
    fn: Fn,
    num_procs: int = None,
) -> None:
    input_path: Path = Path(input_path)
    output_path: Path = Path(output_path)
    num_procs: int = num_procs or os.cpu_count()

    with Pool(processes=num_procs) as pool:
        chunks = [
            (input_path, fn, start, end)
            for start, end in generate_file_chunks(input_path, num_chunks=num_procs)
        ]
        paths = list(pool.starmap(run_and_save, chunks))
        paths_cat = [f'"{path}"' for path in paths]
        cmd = f"cat {' '.join(paths_cat)} > {str(output_path)}"
        subprocess.call(cmd, shell=True)
        for path in paths:
            os.remove(path)
