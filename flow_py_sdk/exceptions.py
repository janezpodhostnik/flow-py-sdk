class PySDKError(Exception):
    """
    Base class for other exceptions
    """

    pass


class NotCadenceValueError(PySDKError):
    """
    Cadence value expected, but got something else
    """

    @classmethod
    def from_value(cls, value) -> "NotCadenceValueError":
        return NotCadenceValueError(
            f"Value {value} is not a cadence value. Cadence value expected."
        )
