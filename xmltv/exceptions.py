class XMLTVException(Exception):
    pass


class ChannelNotFound(XMLTVException):
    pass


class SourceNotFound(XMLTVException):
    pass
