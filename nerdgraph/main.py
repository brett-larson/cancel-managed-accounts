import os
import sys

from dotenv import load_dotenv
from nerdgraph.queries.get_managed_accounts import get_managed_accounts
from nerdgraph.utils.nerdgraph_client import NerdGraphClient
from nerdgraph.utils.csv_writer import write_to_csv
from nerdgraph.utils.logger import Logger
from nerdgraph.queries.get_managed_accounts.workflow import get_managed_accounts_workflow

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

    # Get managed accounts workflow
    active_accounts, canceled_accounts = get_managed_accounts_workflow(nerdgraph_client, csv_output_path)




    logger.info('********** Application Complete **********')

if __name__ == "__main__":
    main()