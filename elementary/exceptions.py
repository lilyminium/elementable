class ElementaryError(Exception):
    pass

class InvalidElementError(KeyError, ElementaryError):
    
    def __init__(self, msg):
        msg = f"Element {msg} is not supported"
        super().__init__(msg)
