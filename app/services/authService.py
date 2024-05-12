from flask import session
import app.exceptions.apiExceptions as exceptions


def validateLogin():
    if "user" in session:
        return session["user"]
    else:
        return exceptions.throwUserNotAuthenticatedException()