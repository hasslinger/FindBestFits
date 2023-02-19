from configuration.logging_configuration import log


class FindBestFitsException(Exception):
    def __init__(self, message):
        log.error(message)
        super().__init__(message)
