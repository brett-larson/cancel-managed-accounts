from typing import List

from nerdgraph.utils.nerdgraph_client import NerdGraphClient
from nerdgraph.utils.logger import Logger

# Create logger for the module
logger = Logger(__name__).get_logger()

GET_MANAGED_ACCOUNTS = """
query GetManagedAccounts($isCanceled: Boolean!) {
  actor {
    organization {
      accountManagement {
        managedAccounts(isCanceled: $isCanceled) {
          id
          name
        }
      }
    }
  }
}
"""

def get_managed_accounts(nerdgraph_client: NerdGraphClient, is_canceled: bool) -> List | None:
    variables = {"isCanceled": is_canceled}

    try:
        response = nerdgraph_client.execute_query(query=GET_MANAGED_ACCOUNTS, variables=variables)
        managed_accounts = _format_response(response)
        return managed_accounts
    except Exception as e:
        logger.error(f"Failed to get managed accounts: {e}")
        return None

def _format_response(response: dict) -> list[dict] | None:
    try:
        managed_accounts = response["data"]["actor"]["organization"]["accountManagement"]["managedAccounts"]
        return managed_accounts
    except KeyError as e:
        logger.error(f"Failed to get managed accounts: {e}")
        return None