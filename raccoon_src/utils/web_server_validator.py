from requests.exceptions import ConnectionError, TooManyRedirects
from raccoon_src.utils.request_handler import RequestHandler
from raccoon_src.utils.singleton import Singleton
from raccoon_src.utils.exceptions import WebServerValidatorException, RequestHandlerException


class WebServerValidator(metaclass=Singleton):
    """
    Validates the web server of a given host by attempting to establish a connection.
    """
    def __init__(self):
        self.request_handler = RequestHandler()

    def validate_target_webserver(self, host):
        """
        Validates the target web server.
        """
        try:
            self.request_handler.send(
                "GET",
                timeout=20,
                url="{}://{}:{}".format(
                    host.protocol,
                    host.target,
                    host.port
                )
            )
            return True
        except RequestHandlerException:
            raise WebServerValidatorException
