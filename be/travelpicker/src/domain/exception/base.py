class Exception(Exception):
    @classmethod
    def format_message(cls):
        return "{}: {}".format(
            cls.__class__.__name__, "{}".format(cls)
        )


class RequestException(Exception):
    pass


class SystemException(Exception):
    pass