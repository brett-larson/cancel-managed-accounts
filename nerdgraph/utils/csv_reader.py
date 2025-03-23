import csv
from typing import List
from nerdgraph.utils.logger import Logger

# Create logger for the module
logger = Logger(__name__).get_logger()

def read_account_numbers(file_path: str) -> List[int]:
    """
    Reads account numbers from a CSV file.
    :param file_path: Path to the CSV file
    :return: List of account numbers
    """
    account_numbers = []

    try:
        with open(file_path, mode='r') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                account_numbers.append(int(row['account_id']))
        logger.info(f"Successfully read {len(account_numbers)} account numbers from {file_path}.")
    except FileNotFoundError:
        logger.error(f"File not found: {file_path}")
    except Exception as e:
        logger.error(f"Error reading CSV file: {e}")

    return account_numbers