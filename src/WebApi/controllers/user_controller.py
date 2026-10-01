from http import HTTPStatus

from ASPythonCore.http import Controller, get


class UserController(Controller):
    @get("/users")
    def get_users(self):
        return self.response(HTTPStatus.OK, "users found :D")

    @get("/users2")
    def get_users2(self):
        return self.response(HTTPStatus.NOT_FOUND, "users found :D")


controller = UserController()
controller.get_users()
