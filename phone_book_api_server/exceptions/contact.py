class ContactNotFoundError(Exception):
    """Contact Does Not Exist Error."""


class ContactAlreadyExist(Exception):
    """Contact Already Exist in db."""


class InvalidContactParams(Exception):
    """Invalid Contact Parameters."""


class InvalidContactNumber(InvalidContactParams):
    """Invalid Contact Phone Number."""

    def __init__(self, detail: str):
        super().__init__(detail)


class InvalidContactName(InvalidContactParams):
    """Invalid Contact Name."""

    def __init__(self, detail: str):
        super().__init__(detail)


class InvalidContactEmail(InvalidContactParams):
    """Invalid Contact Email."""

    def __init__(self, detail: str):
        super().__init__(detail)
