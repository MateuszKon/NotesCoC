from abc import ABC, abstractmethod
from typing import Union

from flask import Response


class IHomeRoute(ABC):

    @classmethod
    @abstractmethod
    def render_home_page(cls, data: dict) -> str:
        pass

    @classmethod
    @abstractmethod
    def render_home_page_filtered(cls, data: dict) -> str:
        pass

