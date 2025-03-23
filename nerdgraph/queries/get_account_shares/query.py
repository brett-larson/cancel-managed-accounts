from nerdgraph.utils import Logger
from nerdgraph.utils import NerdGraphClient

# Create logger for the module
logger = Logger(__name__).get_logger()

GET_ACCOUNT_SHARES_QUERY = """
query GetAccountShares($accountId: Int!) {
  customerAdministration {
    accountShares(filter: {accountId: {eq: $accountId}}) {
      items {
        accountId
        id
        name
      }
    }
  }
}
"""

def get_account_shares(nerdgraph_client: NerdGraphClient, account_id: int) -> list[dict] | None:
    """
    Get account shares using the account ID.
    :param nerdgraph_client: Instance of NerdGraphClient
    :param account_id: Account ID
    :return: dict
    """
    variables = {
        "accountId": account_id
    }

    try:
        response = nerdgraph_client.execute_query(GET_ACCOUNT_SHARES_QUERY, variables)
        account_shares = _format_response(response)
        return account_shares
    except Exception as e:
        logger.error(f"Failed to get account shares for account {account_id}: {e}")
        return None

def _format_response(response: dict) -> list[dict] | None:
    try:
        account_shares = response["data"]["customerAdministration"]["accountShares"]["items"]
        return account_shares
    except KeyError as e:
        logger.error(f"Failed to get managed accounts: {e}")
        return None