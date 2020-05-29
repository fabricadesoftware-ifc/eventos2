import pytest
from django.urls import reverse
from rest_framework import status

from eventos2.core.models import ActivityRegistration, EventRegistration


@pytest.mark.django_db
def test_register_valid(api_client, activity_factory, event_factory, user_factory):
    # DADO um usuário autenticado.
    user = user_factory(name="user", permissions=[])
    api_client.force_authenticate(user=user)

    # E DADO um evento no qual o usuário está registrado.
    event = event_factory(slug="event-a", owners=[])
    EventRegistration.objects.create(event=event, user=user)

    # E DADO uma activity.
    activity = activity_factory(event=event, slug="activity-a", owners=[])

    # QUANDO a API é chamada para registrar o usuário na activity.
    resp = api_client.post(
        reverse("activity-registration-list"), {"activity": activity.slug}
    )

    # ENTÃO a reposta deve ser de sucesso
    assert resp.status_code == status.HTTP_201_CREATED

    # E ENTÃO a registration deve ser criada.
    assert ActivityRegistration.objects.count() == 1
    assert ActivityRegistration.objects.first().event_registration.user == user


@pytest.mark.django_db
def test_register_duplicate(api_client, activity_factory, event_factory, user_factory):
    # DADO um usuário autenticado.
    user = user_factory(name="user", permissions=[])
    api_client.force_authenticate(user=user)

    # E DADO um evento no qual o usuário está registrado.
    event = event_factory(slug="event-a", owners=[])
    event_registration = EventRegistration.objects.create(event=event, user=user)

    # E DADO uma activity na qual o usuário já está registrado.
    activity = activity_factory(event=event, slug="activity-a", owners=[])
    ActivityRegistration.objects.create(
        activity=activity, event_registration=event_registration
    )

    # QUANDO a API é chamada para registrar o usuário na activity novamente.
    resp = api_client.post(
        reverse("activity-registration-list"), {"activity": activity.slug}
    )

    # ENTÃO a reposta deve ser de falha
    assert resp.status_code == status.HTTP_400_BAD_REQUEST

    # E ENTÃO a registration não deve ser duplicada.
    assert ActivityRegistration.objects.count() == 1


@pytest.mark.django_db
def test_register_not_registered_to_event(
    api_client, activity_factory, event_factory, user_factory
):
    # DADO um usuário autenticado.
    user = user_factory(name="user", permissions=[])
    api_client.force_authenticate(user=user)

    # E DADO um evento no qual o usuário não está registrado.
    event = event_factory(slug="event-a", owners=[])

    # E DADO uma activity.
    activity = activity_factory(event=event, slug="activity-a", owners=[])

    # QUANDO a API é chamada para registrar o usuário na activity.
    resp = api_client.post(
        reverse("activity-registration-list"), {"activity": activity.slug}
    )

    # ENTÃO a reposta deve ser de falha
    assert resp.status_code == status.HTTP_400_BAD_REQUEST

    # E ENTÃO a registration não deve ser criada.
    assert ActivityRegistration.objects.count() == 0


@pytest.mark.django_db
def test_register_unauthorized(api_client, activity_factory, event_factory):
    # DADO nenhum usuário autenticado.

    # E DADO um evento.
    event = event_factory(slug="event-a", owners=[])

    # E DADO uma activity.
    activity = activity_factory(event=event, slug="activity-a", owners=[])

    # QUANDO a API é chamada para registrar o usuário na activity.
    resp = api_client.post(
        reverse("activity-registration-list"), {"activity": activity.slug}
    )

    # ENTÃO a reposta deve ser de falta de permissões
    assert resp.status_code == status.HTTP_403_FORBIDDEN

    # E ENTÃO a registration não deve ser criada.
    assert ActivityRegistration.objects.count() == 0


@pytest.mark.django_db
def test_unregister_valid(api_client, activity_factory, event_factory, user_factory):
    # DADO um usuário autenticado.
    user = user_factory(name="user", permissions=[])
    api_client.force_authenticate(user=user)

    # E DADO um evento no qual o usuário está registrado.
    event = event_factory(slug="event-a", owners=[])
    event_registration = EventRegistration.objects.create(event=event, user=user)

    # E DADO uma activity na qual o usuário está registrado.
    activity = activity_factory(event=event, slug="activity-a", owners=[])
    registration = ActivityRegistration.objects.create(
        activity=activity, event_registration=event_registration
    )

    # QUANDO a API é chamada para remover o registro do usuário na activity.
    resp = api_client.delete(
        reverse("activity-registration-detail", args=[registration.id]),
    )

    # ENTÃO a reposta deve ser de sucesso
    assert resp.status_code == status.HTTP_204_NO_CONTENT

    # E ENTÃO a registration deve ser removida.
    assert ActivityRegistration.objects.count() == 0


@pytest.mark.django_db
def test_unregister_other_user_unauthorized(
    api_client, activity_factory, event_factory, user_factory
):
    # DADO um usuário autenticado.
    user = user_factory(name="user", permissions=[])
    api_client.force_authenticate(user=user)

    # E DADO um outro usuário alvo
    target_user = user_factory(name="target", permissions=[])

    # E DADO um evento no qual ambos usuários estão registrados.
    event = event_factory(slug="event-a", owners=[])
    EventRegistration.objects.create(event=event, user=user)
    target_event_registration = EventRegistration.objects.create(
        event=event, user=target_user
    )

    # E DADO uma activity na qual o usuário alvo já está registrado.
    activity = activity_factory(event=event, slug="activity-a", owners=[])
    target_activity_registration = ActivityRegistration.objects.create(
        activity=activity, event_registration=target_event_registration
    )

    # QUANDO a API é chamada para remover o registro do usuário alvo na activity.
    resp = api_client.delete(
        reverse("activity-registration-detail", args=[target_activity_registration.id]),
    )

    # ENTÃO a reposta deve ser de falta de permissões
    assert resp.status_code == status.HTTP_403_FORBIDDEN

    # E ENTÃO a registration deve permanecer inalterada no banco.
    assert ActivityRegistration.objects.count() == 1


@pytest.mark.django_db
def test_list_registrations_for_user_and_event(
    api_client, activity_factory, event_factory, user_factory
):
    # DADO um usuário autenticado.
    user = user_factory(name="user", permissions=[])
    api_client.force_authenticate(user=user)

    # E DADO dois eventos nos quais o usuário está registrado.
    event_a = event_factory(slug="event-a", owners=[])
    event_b = event_factory(slug="event-b", owners=[])
    event_registration_a = EventRegistration.objects.create(event=event_a, user=user)
    event_registration_b = EventRegistration.objects.create(event=event_b, user=user)

    # E DADO uma activity em cada evento.
    activity_a = activity_factory(event=event_a, slug="activity-a", owners=[])
    activity_b = activity_factory(event=event_b, slug="activity-b", owners=[])

    # E DADO duas inscrições do usuário, uma em cada activity.
    ActivityRegistration.objects.create(
        activity=activity_a, event_registration=event_registration_a
    )
    ActivityRegistration.objects.create(
        activity=activity_b, event_registration=event_registration_b
    )

    # QUANDO a API é chamada para listar as inscrições do usuário no evento A.
    resp = api_client.get(
        "{}?user_id={}&event_slug={}".format(
            reverse("activity-registration-list"), user.id, event_a.slug
        )
    )

    # ENTÃO apenas a inscrição do usuário na atividade do evento A será retornada.
    assert resp.status_code == status.HTTP_200_OK
    assert len(resp.data) == 1
    assert resp.data[0]["activity"]["slug"] == activity_a.slug
