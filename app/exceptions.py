class ProductNotFound(Exception):
    """
    Exception raised when an item is not found.
    """

    pass


class ProductNotAvailable(Exception):
    """
    Exception raised when an item is not available.
    """

    pass


class ProductsAreDuplicated(Exception):
    """
    Exception raised when an item is duplicated.
    """

    pass


class OrderNotFound(Exception):
    """
    Exception raised when an order is not found.
    """

    pass


class USDRateNotFound(Exception):
    """
    Exception raised when a USD rate is not found.
    """

    pass
