class ElementableError(Exception):
    pass


class InvalidElementError(KeyError, ElementableError):

    def __init__(self, msg):
        msg = f"Element {msg} is not supported"
        super().__init__(msg)
