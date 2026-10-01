import importlib
import pkgutil

from ASPythonCore.http import Controller


class WebApplication:
    BASE_PACKAGE = "WebApi"

    services: list[type]

    def __init__(self) -> None:
        self._load_project_modules()

    def _load_project_modules(self):
        print("Loading modules...")

        try:
            app_package = importlib.import_module(self.BASE_PACKAGE)
            app_packages = pkgutil.walk_packages(
                app_package.__path__, app_package.__name__ + "."
            )

            for _file_path, package_name, _is_package in app_packages:
                importlib.import_module(package_name)

        except ModuleNotFoundError as exception:
            raise ModuleNotFoundError(
                "Couldn't found configured BASE_PACKAGE module."
            ) from exception

    def add_controllers(self) -> WebApplication:
        print("Setting up controllers...")

        registered_controllers = Controller.__subclasses__()

        for controller_class in registered_controllers:
            new_controller = controller_class()
            new_controller.expose_endpoints()

        return self
