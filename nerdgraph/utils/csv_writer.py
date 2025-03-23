from typing import List, Dict, Any
import csv
import os
from nerdgraph.utils import Logger

# Create logger for the module
logger = Logger(__name__).get_logger()

# Default output directory
DEFAULT_CSV_OUTPUT_PATH = "data/output"

def _ensure_output_dir(csv_path: str) -> None:
    """
    Ensure the output directory exists. If it doesn't, create it.
    :param csv_path: Directory path for output file
    :return: None
    """
    if not os.path.exists(csv_path):
        try:
            os.makedirs(csv_path)
            logger.info(f"Created output directory: {csv_path}")
        except OSError as e:
            logger.error(f"Failed to create output directory: {e}")
            raise

def _validate_csv_data(data: List[Dict[str, Any]]) -> bool:
    """
    Validate that data is a non-empty list of dictionaries.
    :param data: List of dictionaries to validate
    :return: True if data is valid, False otherwise
    """
    if not data or not isinstance(data, list):
        logger.error("No data to write or data is not a list")
        return False

    if not all(isinstance(record, dict) for record in data):
        logger.error("All items in data must be dictionaries")
        return False

    if len(data) == 0:
        logger.warning("Empty data list provided")
        return False

    return True

def write_to_csv(file_name: str, data: List[Dict[str, Any]],
                 csv_path: str = DEFAULT_CSV_OUTPUT_PATH) -> bool:
    """
    Write a list of dictionaries to a CSV file. Each dictionary in the list represents a row in the CSV file.
    The keys of the dictionaries represent the column headers.
    :param file_name: Name of the output file.
    :param data: List of dictionaries to write.
    :param csv_path: Directory path for output file (default: 'data/output').
    :return: True if successful, False otherwise.
    """
    try:
        # Validate data
        if not _validate_csv_data(data):
            return False

        # Create the output directory if it doesn't exist
        _ensure_output_dir(csv_path)

        # Create the full file path
        file_path = os.path.join(csv_path, file_name)

        # Get headers from the first dictionary
        headers = list(data[0].keys())

        # Write the data to the file
        with open(file_path, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=headers)
            writer.writeheader()
            writer.writerows(data)

        logger.info(f"Successfully wrote {len(data)} records to {file_path}")
        return True

    except (IOError, OSError) as e:
        logger.error(f"File error when writing CSV: {e}")
        return False
    except Exception as e:
        logger.error(f"Unexpected error when writing CSV: {e}")
        return False
