from abc import ABC, abstractmethod


class IHomeRoute(ABC):

    @classmethod
    @abstractmethod
    def render_home_page(cls, data: dict) -> str:
        pass

    @classmethod
    @abstractmethod
    def render_home_page_filtered(cls, data: dict) -> str:
        pass

