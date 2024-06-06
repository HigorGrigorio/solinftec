# -----------------------------------------------------------------------------
# (C) 2023 Higor Grigorio (higorgrigorio@gmail.com)  (MIT License)
# -----------------------------------------------------------------------------
import abc
from dataclasses import dataclass
from typing import TypedDict, Optional

from fastapi import Request, Response


@dataclass
class ControllerResponse(TypedDict):
    """
    The response type.
    """

    """
    The response code.
    """
    code: int

    """
    The response message.
    """
    message: Optional[str]

    """
    The response body.
    """
    body: Optional[dict]


class Controller(abc.ABC):
    request: Request
    response: Response

    async def execute(self, request: Request, response: Response) -> ControllerResponse:
        self.request = request
        self.response = response

        result = await self.do_execute()

        # set the response code
        response.status_code = result['code']

        return result

    @abc.abstractmethod
    async def do_execute(self) -> ControllerResponse:
        ...

    @staticmethod
    def ok(body: dict, message: str = '') -> ControllerResponse:
        return {
            'code': 200,
            'body': body,
            'message': message
        }

    @staticmethod
    def created(body: dict) -> ControllerResponse:
        return {
            'code': 201,
            'body': body,
            'message': 'Successfully created.'
        }

    @staticmethod
    def bad_request(message: str) -> ControllerResponse:
        return {
            'code': 400,
            'body': {},
            'message': message
        }

    @staticmethod
    def unauthorized(message: str) -> ControllerResponse:
        return {
            'code': 401,
            'body': {},
            'message': message
        }

    @staticmethod
    def forbidden(message: str) -> ControllerResponse:
        return {
            'code': 403,
            'body': {},
            'message': message
        }

    @staticmethod
    def not_found(message: str) -> ControllerResponse:
        return {
            'code': 404,
            'body': {},
            'message': message
        }

    @staticmethod
    def conflict(message: str) -> ControllerResponse:
        return {
            'code': 409,
            'body': {},
            'message': message
        }

    @staticmethod
    def error(message: str | Exception) -> ControllerResponse:
        if message and isinstance(message, Exception):
            message = str(message.args[0])

        return {
            'code': 500,
            'body': {},
            'message': message
        }

    @staticmethod
    def not_implemented(message: str) -> ControllerResponse:
        return {
            'code': 501,
            'body': {},
            'message': message
        }
