from abc import ABC, abstractmethod
from typing import Union

from flask import Response


class IRequestDataHandler(ABC):

    @classmethod
    @abstractmethod
    def get_request_data(cls) -> dict:
        """Get data sent in request from user"""
        pass

    @classmethod
    @abstractmethod
    def prepare_response(
            cls,
            template: str = None,
            **kwargs
    ) -> Union[Response, str]:
        """
        Preparing response based on Content-Type of a request and parameters.

        :param template: path  to html be rendered (if applicabale)
        :param kwargs: all data which must be included in response
        :return: Response type object or rendered html into string
        """
        pass
