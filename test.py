import MeCab

from process_file_parallel import process_file_parallel, process_file_parallel_and_save

mecab = MeCab.Tagger("-Owakati")


def fn(line):
    return mecab.parse(line.strip()).strip()


def main():
    results = process_file_parallel(input_path="in.txt", fn=fn)
    print(results[0])
    print(len(results))

    process_file_parallel_and_save(input_path="in.txt", output_path="out.txt", fn=fn)


if __name__ == "__main__":
    main()
