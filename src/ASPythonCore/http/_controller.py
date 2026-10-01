from abc import ABC
from functools import wraps
from http import HTTPMethod, HTTPStatus
from inspect import currentframe, getmembers, ismethod
from types import FunctionType
from typing import Any


def get(endpoint: str = "/") -> FunctionType:
    def decorator(fn: FunctionType):
        @wraps(fn)
        def http_method_wrapper(*args: Any, **kwargs: Any) -> None:
            print("HTTP GET operation being executed...")

            fn(*args, **kwargs)

        setattr(http_method_wrapper, "__endpoint__", endpoint)
        setattr(http_method_wrapper, "__http_method__", HTTPMethod.GET)

        return http_method_wrapper

    return decorator


def post(endpoint: str = "/") -> FunctionType:
    def decorator(fn: FunctionType):
        @wraps(fn)
        def http_method_wrapper(*args: Any, **kwargs: Any) -> None:
            print("HTTP POST operation being executed...")

            fn(*args, **kwargs)

        setattr(http_method_wrapper, "__endpoint__", endpoint)
        setattr(http_method_wrapper, "__http_method__", HTTPMethod.POST)

        return http_method_wrapper

    return decorator


def put(endpoint: str = "/") -> FunctionType:
    def decorator(fn: FunctionType):
        @wraps(fn)
        def http_method_wrapper(*args: Any, **kwargs: Any) -> None:
            print("HTTP PUT operation being executed...")

            fn(*args, **kwargs)

        setattr(http_method_wrapper, "__endpoint__", endpoint)
        setattr(http_method_wrapper, "__http_method__", HTTPMethod.PUT)

        return http_method_wrapper

    return decorator


def delete(endpoint: str = "/") -> FunctionType:
    def decorator(fn: FunctionType):
        @wraps(fn)
        def http_method_wrapper(*args: Any, **kwargs: Any) -> None:
            print("HTTP DELETE operation being executed...")

            fn(*args, **kwargs)

        setattr(http_method_wrapper, "__endpoint__", endpoint)
        setattr(http_method_wrapper, "__http_method__", HTTPMethod.DELETE)

        return http_method_wrapper

    return decorator


class Controller(ABC):
    """Base controller class that adds controller atrributes and methods to a class"""

    def expose_endpoints(self):
        print(f"[{self.__class__.__name__}] Mapping endpoints:")

        registered_endpoints: list[str] = []
        methods = getmembers(self, predicate=ismethod)

        for _name, method in methods:
            is_http_wrapped = (
                hasattr(method, "__wrapped__")
                and "http_method_wrapper" in method.__code__.co_name
            )

            if not is_http_wrapped:
                continue

            endpoint_path: str = getattr(method, "__endpoint__")
            http_method: HTTPMethod = getattr(method, "__http_method__")

            endpoint_id = http_method + " " + endpoint_path

            if endpoint_id in registered_endpoints:
                raise AssertionError(
                    "A endpoint with the same path and method cannot coexist"
                )

            registered_endpoints.append(endpoint_id)
            print("\t", endpoint_id)

    def response(self, status: HTTPStatus, data: Any) -> dict[str, Any]:
        current_frame = currentframe()

        if current_frame and current_frame.f_back:
            caller_frame = current_frame.f_back

            if caller_frame and caller_frame.f_back:
                # http_wrapper_frame = caller_frame.f_back

                # print("test", "__http_method__" in dir(http_wrapper_frame))
                # print("getattr", getattr(http_wrapper_frame, "__http_method__"))

                # print("http_wrapper", dir(http_wrapper_frame))
                # print("TEST", http_wrapper_frame)

                # Estudar contextvars.ContextVar pra ver se resolve essa desgraça
                # Ideia: definir headers e status defautls com base no __http_method__ do endpoint
                pass

        return {"status": status, "data": data}
