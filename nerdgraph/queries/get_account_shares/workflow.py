from typing import Tuple, List

from nerdgraph.queries.get_account_shares import query
from nerdgraph.utils.nerdgraph_client import NerdGraphClient
from nerdgraph.utils.logger import Logger

# Create logger for the module
logger = Logger(__name__).get_logger()

def get_account_shares_workflow(nerdgraph_client: NerdGraphClient,
                                  account_numbers_to_cancel: list) -> List[dict]:
    """
    Get account shares workflow. This function gets account shares with status and writes the data to CSV files.
    :param nerdgraph_client: NerdGraphClient object
    :param csv_output_path: Path to the output CSV files. If None, the default path is used.
    :return: Tuple of active and canceled accounts
    """
    logger.info('***** Get Account Shares Workflow Started *****')

    account_shares = []

    try:
        # Get account shares
        for account in account_numbers_to_cancel:
            response = query.get_account_shares(nerdgraph_client=nerdgraph_client, account_id=account)

            if response:
                account_shares.extend(response)
            else:
                logger.warning(f"No account shares found for account: {account}")


