import os
import sys

from dotenv import load_dotenv
from nerdgraph.queries.get_managed_accounts import get_managed_accounts
from nerdgraph.utils.nerdgraph_client import NerdGraphClient
from nerdgraph.utils.csv_writer import write_to_csv
from nerdgraph.utils.logger import Logger
from nerdgraph.queries.get_managed_accounts.workflow import get_managed_accounts_workflow
from nerdgraph.utils.csv_reader import read_account_numbers

# Create logger for the module
logger = Logger(__name__).get_logger()

def main():
    logger.info('********** Application Started **********')

    # Load environment variables from .env-pan file
    load_dotenv()

    # Create an instance of the NerdGraphClient
    nerdgraph_client = NerdGraphClient()

    # Application variables
    is_canceled = [True, False]
    csv_output_path = "data/output"
    csv_input_path = "data/input"
    csv_input_filename = "cancel_account_list.csv"
    # cancel_account_numbers = [] # List of accounts to cancel. Otherwise, use CSV file.

    # Get account numbers from CSV file
    cancel_account_numbers = read_account_numbers(os.path.join(csv_input_path, csv_input_filename))
    print(cancel_account_numbers)
    logger.info(f'Accounts to cancel: {cancel_account_numbers}')

    # Get managed accounts workflow
    active_accounts, canceled_accounts = get_managed_accounts_workflow(nerdgraph_client, csv_output_path)

    try:
        active_account_ids = [account['id'] for account in active_accounts]
        canceled_account_ids = [account['id'] for account in canceled_accounts]

        account_numbers_to_cancel = []
        for account in cancel_account_numbers:
            if account in canceled_account_ids:
                logger.warning(f'Account {account} is already canceled. Remove from the list.')
            elif account not in active_account_ids:
                logger.warning(f'Account {account} is not found in active or cancelled account lists. Remove from the list.')
            else:
                account_numbers_to_cancel.append(account)
                logger.info(f'Account {account} is active.')

        logger.info(f'Accounts to cancel: {account_numbers_to_cancel}')
    except Exception as e:
        logger.error(f'Error checking if accounts are already canceled or active: {e}')
        return

    logger.info('********** Application Complete **********')

if __name__ == "__main__":
    main()