from django.apps import apps
from django.core.management import get_commands


def test_ptech_tools_is_installed_and_exports_export_db_command():
    assert apps.is_installed("ptech_tools")
    assert get_commands()["export_db"] == "ptech_tools"
