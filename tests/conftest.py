import pytest
from django.contrib.auth.models import Permission
from rest_framework.test import APIClient

from eventos2.core.models import User


@pytest.fixture()
def api_client():
    """
    Instancia de cliente para teste do DRF.
    Faz requests com JSON, em vez de multipart/form-data.
    (como definido nas settings, REST_FRAMEWORK.TEST_REQUEST_DEFAULT_FORMAT)
    """
    return APIClient()


@pytest.fixture
def user_factory():
    def _factory(*, name, permissions):
        user = User.objects.create(email="{0}@example.com".format(name), username=name)
        user.set_password(name)
        user.save()

        for permission in permissions:
            app_label, codename = permission.split(".")
            user.user_permissions.add(
                Permission.objects.get(
                    content_type__app_label=app_label, codename=codename
                )
            )

        return user

    return _factory
