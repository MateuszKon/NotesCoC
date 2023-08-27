from functools import wraps
from typing import Any

from flask import current_app, redirect, request, url_for
from flask.typing import ResponseReturnValue
from flask_jwt_extended import verify_jwt_in_request
from flask_jwt_extended.exceptions import UserClaimsVerificationError
from flask_jwt_extended.exceptions import NoAuthorizationError
from flask_jwt_extended.view_decorators import LocationType

from NotesApp.routes.i_request import ResponseData


def token_not_valid(next_url: str = None) -> ResponseReturnValue:
    """Action on token not existing or expired

    :param next_url: path of original request (to be redirected after
    login)
    :return: redirect response
    """
    return redirect(url_for("login_user", next=next_url))


def jwt_required_with_redirect(
        admin: bool = False,
        optional: bool = False,
        fresh: bool = False,
        refresh: bool = False,
        locations: LocationType = None,
        verify_type: bool = True,
) -> Any:
    """
    A decorator to protect a Flask endpoint with JSON Web Tokens.
    Extends behaviour of jwt_required function of flask_jwt_extended

    :param admin: require jwt with admin scope
    :param optional: as in jwt_required
    :param fresh: as in jwt_required
    :param refresh: as in jwt_required
    :param locations: as in jwt_required
    :param verify_type: as in jwt_required
    :return: as in jwt_required
    """
    def wrapper(fun):
        @wraps(fun)
        def decorator(*args, **kwargs):
            try:
                jwt_header, jwt_data = verify_jwt_in_request(
                    optional,
                    fresh,
                    refresh,
                    locations,
                    verify_type
                )
            except NoAuthorizationError:
                return token_not_valid(request.path)

            verify_jwt_admin_claim(jwt_header, jwt_data, admin)
            return current_app.ensure_sync(fun)(*args, **kwargs)

        return decorator

    return wrapper


def verify_jwt_admin_claim(jwt_header: dict, jwt_data: dict, admin: bool):
    if admin and jwt_data.get("admin") is None:
        error_msg = "User admin claim verification failed"
        raise UserClaimsVerificationError(error_msg, jwt_header, jwt_data)


def token_expired_redirection_callback(
        jwt_header: dict,
        jwt_data: dict
) -> ResponseReturnValue:
    return token_not_valid(request.path)


def access_denied_response():
    return ResponseData(
        resource={'message': 'User admin claim verification failed'},
        status_code=405,
    )
