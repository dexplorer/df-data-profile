import logging
import csv


def uf_open_file(file_path: str, open_mode: str):
    """
    Open a file with exception handling.

    :param file_path: File path
    :type file_path: str
    :param open_mode: File open mode
    :type open_mode: str
    :return: File object
    :rtype: TextIOWrapper
    """

    try:
        f = open(file_path, open_mode)
    except FileNotFoundError as error:
        logging.error(error)
        raise  # re-raise error with stack trace
        # raise FileNotFoundError   # Don't do this, you'll lose the stack trace!
    else:
        return f

def uf_read_delim_file_to_list_of_dict(file_path: str, delim=',') -> list[dict]:
    with uf_open_file(file_path=file_path, open_mode="r") as f:
        if delim == '|':
            reader = csv.DictReader(f, dialect='pipe')
        else:
            # reader = csv.DictReader(f, fieldnames=content_header) # omit fieldnames to use the first row as field names
            reader = csv.DictReader(f)

        file_records: list[dict] = [row for row in reader]

    try:
        if file_records:
            # print(file_records[:2])
            return file_records
        else:
            raise ValueError("Error in reading the file.")
    except ValueError as error:
        logging.error(error)
        raise    