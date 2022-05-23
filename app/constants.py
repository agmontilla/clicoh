from enum import Enum

USD_API_URL = "https://www.dolarsi.com/api/api.php?type=valoresprincipales"


class Actions(Enum):
    """
    Enum for actions
    """

    CREATE, UPDATE = range(2)


class CurrentExchanges(Enum):
    """
    Enum for current exchanges
    """

    ARS = "Pesos"
    USD = "Dolar Blue"
