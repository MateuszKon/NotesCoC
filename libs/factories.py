from functools import wraps


def name_factory(func: callable) -> callable:
    """
    Changing function into factory of the function with custom name.
    Factory function must be called with 'name' parameter. 'name' is used to
    set __name__ parameter of created function.
    :param func: function which will be result of factory method
    :return: callable which called return origianl func with modified __name__
    """
    def decorator(self, name: str):
        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(self, *args, **kwargs)
        wrapper.__name__ = name
        return wrapper
    return decorator
