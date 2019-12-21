import os

import dateparser as dp


def convert_str_time_to_utc(time_str):
    dt = dp.parse(time_str)
    return dt


def read_file_content(file_path):
    with open(file_path, 'r') as file:
        data = file.read()
    return data


def create_directory_if_needed(path, logger):
    try:
        os.mkdir(path)
        logger.info(f"Directory [{path}] created successfully")
    except FileExistsError:
        logger.info(f"Directory [{path}] already exists")
