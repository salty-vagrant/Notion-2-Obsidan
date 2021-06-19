class Link:
    def __init__(self, name: str, uri: str, embedded: bool = False, alt_name: str = ""):
        self._name = name
        self._alt_name = alt_name
        self._uri = uri
        self._embedded = embedded

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Link):
            return NotImplemented
        return self._uri == other._uri

    def __ne__(self, other: object) -> bool:
        if not isinstance(other, Link):
            return NotImplemented
        return self._uri != other._uri

    def __gt__(self, other: object) -> bool:
        if not isinstance(other, Link):
            return NotImplemented
        return self._uri > other._uri

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, Link):
            return NotImplemented
        return self._uri < other._uri
