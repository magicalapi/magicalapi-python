class AsyncClient:
    """
    The MagicalAPI client module to work and connect to the api.
    """

    def __init__(self, api_key: str) -> None:
        """initializing MagicalAPI client.


        api_key(``str``):
            your Magical API account's `api_key` that you can get it from https://panel.magicalapi.com/

        """
        self._api_key = api_key

    @property
    def api_key(self):
        return self._api_key
