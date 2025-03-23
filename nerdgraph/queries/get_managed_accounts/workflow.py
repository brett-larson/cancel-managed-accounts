from typing import Tuple, List

from nerdgraph.queries.get_managed_accounts import get_managed_accounts
from nerdgraph.utils.nerdgraph_client import NerdGraphClient
from nerdgraph.utils.csv_writer import write_to_csv
from nerdgraph.utils.logger import Logger

# Create logger for the module
logger = Logger(__name__).get_logger()

def get_managed_accounts_workflow(nerdgraph_client: NerdGraphClient,
                                  csv_output_path: str = None) -> Tuple[List[dict], List[dict]]:
    """
    Get managed accounts workflow. This function gets managed accounts with status and writes the data to CSV files.
    :param nerdgraph_client: NerdGraphClient object
    :param csv_output_path: Path to the output CSV files. If None, the default path is used.
    :return: Tuple of active and canceled accounts
    """
    logger.info('***** Get Managed Accounts Workflow Started *****')

    is_canceled = [True, False]
    active_accounts = []
    canceled_accounts = []

    if csv_output_path is None:
        csv_path = csv_output_path
    else:
        csv_path = "data/output"


    try:
        # Get managed accounts with status
        for status in is_canceled:
            response = get_managed_accounts(nerdgraph_client=nerdgraph_client, is_canceled=status)

            if response:
                csv_file_name = "cancelled_managed_accounts.csv" if status else "active_managed_accounts.csv"
                write_to_csv(file_name=csv_file_name, data=response, csv_path=csv_path)

                # Write response to appropriate list
                if status:
                    canceled_accounts.extend(response)
                else:
                    active_accounts.extend(response)
            else:
                logger.warning(f"No managed accounts found with status: {status}")

    except Exception as e:
        logger.critical(f"An error occurred: {e}")


    logger.info('***** Get Managed Accounts Workflow Complete *****')

    return active_accounts, canceled_accounts

if __name__ == "__main__":
    get_managed_accounts_workflow()