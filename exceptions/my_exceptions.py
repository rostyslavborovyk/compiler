EOF = "EOF"


class UnrecognizedTokenException(Exception):
    pass


class InvalidSyntaxException(Exception):
    pass


class NoVisitMethodException(Exception):
    pass


class NoSuchVariableException(Exception):
    pass
