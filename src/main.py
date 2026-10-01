from ASPythonCore.web_application import WebApplication


def setup_framework():
    _web_app = WebApplication().add_controllers()


if __name__ == "__main__":
    setup_framework()
