import csv
from typing import List
from nerdgraph.utils.logger import Logger

# Create logger for the module
logger = Logger(__name__).get_logger()

def read_account_numbers(file_path: str) -> List[int]:
    """
    Reads New Relic account numbers from a CSV file. The CSV can have multiple columns, but must have a column named
    'account_number' that contains the account numbers.
    :param file_path: Path to the CSV file
    :return: List of account numbers
    """
    account_numbers = []

    try:
        with open(file_path, mode='r') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                try:
                    account_numbers.append(int(row['account_number']))
                except ValueError:
                    logger.error(f"Invalid account number: {row['account_number']}")
        logger.info(f"Successfully read {len(account_numbers)} account numbers from {file_path}.")
    except FileNotFoundError:
        logger.error(f"File not found: {file_path}")
    except Exception as e:
        logger.error(f"Error reading CSV file: {e}")

    return account_numbers