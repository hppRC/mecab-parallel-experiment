multitime -n 5 poetry run python naive.py
multitime -n 5 poetry run python serial_read.py
multitime -n 5 poetry run python parallel_read.py
multitime -n 5 poetry run python parallel_read_write.py
multitime -n 5 poetry run python parallel_read_write_at_once.py