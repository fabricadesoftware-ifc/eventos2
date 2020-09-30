import pytest
from django.urls import reverse
from rest_framework import status

from eventos2.core.models import ActivityRegistration, EventRegistration


@pytest.mark.django_db
def test_register_valid(api_client, activity_factory, event_factory, user_factory):
    # DADO um usuário autenticado, um evento no qual ele está registrado,
    # e uma activity no evento.
    user = user_factory(name="user", permissions=[])
    api_client.force_authenticate(user=user)
    event = event_factory(slug="event-a", owners=[])
    EventRegistration.objects.create(event=event, user=user)
    activity = activity_factory(event=event, name="Activity A", owners=[])

    # QUANDO a API é chamada para registrar o usuário na activity.
    resp = api_client.post(
        reverse("activity-registration-list"), {"activity": activity.id}
    )

    # ENTÃO a reposta deve ser de sucesso
    assert resp.status_code == status.HTTP_200_OK
    # E ENTÃO a registration deve ser criada.
    assert ActivityRegistration.objects.count() == 1
    assert ActivityRegistration.objects.first().event_registration.user == user


@pytest.mark.django_db
def test_register_duplicate(api_client, activity_factory, event_factory, user_factory):
    # DADO um usuário autenticado, e um evento no qual ele está registrado.
    user = user_factory(name="user", permissions=[])
    api_client.force_authenticate(user=user)
    event = event_factory(slug="event-a", owners=[])
    event_registration = EventRegistration.objects.create(event=event, user=user)
    # E DADO uma activity na qual o usuário já está registrado.
    activity = activity_factory(event=event, name="Activity A", owners=[])
    ActivityRegistration.objects.create(
        activity=activity, event_registration=event_registration
    )

    # QUANDO a API é chamada para registrar o usuário na activity novamente.
    resp = api_client.post(
        reverse("activity-registration-list"), {"activity": activity.id}
    )

    # ENTÃO a reposta deve ser de falha
    assert resp.status_code == status.HTTP_400_BAD_REQUEST
    # E ENTÃO a registration não deve ser duplicada.
    assert ActivityRegistration.objects.count() == 1


@pytest.mark.django_db
def test_register_not_registered_to_event(
    api_client, activity_factory, event_factory, user_factory
):
    # DADO um usuário autenticado, um evento no qual ele não está registrado,
    # e uma activity no evento.
    user = user_factory(name="user", permissions=[])
    api_client.force_authenticate(user=user)
    event = event_factory(slug="event-a", owners=[])
    activity = activity_factory(event=event, name="Activity A", owners=[])

    # QUANDO a API é chamada para registrar o usuário na activity.
    resp = api_client.post(
        reverse("activity-registration-list"), {"activity": activity.id}
    )

    # ENTÃO a reposta deve ser de falta de permissões
    assert resp.status_code == status.HTTP_403_FORBIDDEN
    # E ENTÃO a registration não deve ser criada.
    assert ActivityRegistration.objects.count() == 0


@pytest.mark.django_db
def test_register_out_of_registration_period(
    api_client,
    activity_factory,
    event_factory,
    user_factory,
    freezer,
    parse_to_aware_datetime,
):
    # DADO um usuário autenticado, um evento no qual ele está registrado,
    # e uma activity no evento.
    user = user_factory(name="user", permissions=[])
    api_client.force_authenticate(user=user)
    event = event_factory(
        slug="event-a",
        owners=[],
        starts_on=parse_to_aware_datetime("2020-01-01"),
        ends_on=parse_to_aware_datetime("2020-02-02"),
    )
    EventRegistration.objects.create(event=event, user=user)
    activity = activity_factory(
        event=event,
        name="Activity A",
        owners=[],
        starts_on=event.starts_on,
        ends_on=event.ends_on,
    )
    # E DADO que já passou o tempo de inscrição.
    freezer.move_to(parse_to_aware_datetime("2020-03-03"))

    # QUANDO a API é chamada para registrar o usuário na activity.
    resp = api_client.post(
        reverse("activity-registration-list"), {"activity": activity.id}
    )

    # ENTÃO a reposta de falha deve conter o erro no campo activity.
    assert resp.status_code == status.HTTP_400_BAD_REQUEST
    assert len(resp.data["activity"]) != 0
    # E ENTÃO a registration não deve ser criada.
    assert ActivityRegistration.objects.count() == 0


@pytest.mark.django_db
def test_unregister_valid(api_client, activity_factory, event_factory, user_factory):
    # DADO um usuário autenticado, e um evento no qual ele está registrado.
    user = user_factory(name="user", permissions=[])
    api_client.force_authenticate(user=user)
    event = event_factory(slug="event-a", owners=[])
    event_registration = EventRegistration.objects.create(event=event, user=user)
    # E DADO uma activity na qual o usuário está registrado.
    activity = activity_factory(event=event, name="Activity A", owners=[])
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
    activity = activity_factory(event=event, name="Activity A", owners=[])
    target_activity_registration = ActivityRegistration.objects.create(
        activity=activity, event_registration=target_event_registration
    )

    # QUANDO a API é chamada para remover o registro do usuário alvo na activity.
    resp = api_client.delete(
        reverse("activity-registration-detail", args=[target_activity_registration.id]),
    )

    # ENTÃO a reposta deve ser de falta de permissões
    assert resp.status_code == status.HTTP_403_FORBIDDEN
    # E ENTÃO a registration deve permanecer inalterada.
    assert ActivityRegistration.objects.count() == 1


@pytest.mark.django_db
def test_list_registrations_for_user_and_event(
    api_client, activity_factory, event_factory, user_factory
):
    # DADO um usuário autenticado, e dois eventos nos quais o usuário está registrado.
    user = user_factory(name="user", permissions=[])
    api_client.force_authenticate(user=user)
    event_a = event_factory(slug="event-a", owners=[])
    event_b = event_factory(slug="event-b", owners=[])
    event_registration_a = EventRegistration.objects.create(event=event_a, user=user)
    event_registration_b = EventRegistration.objects.create(event=event_b, user=user)
    # E DADO uma activity em cada evento, nas quais o usuaŕio está registrado.
    activity_a = activity_factory(event=event_a, name="Activity A", owners=[])
    activity_b = activity_factory(event=event_b, name="Activity B", owners=[])
    ActivityRegistration.objects.create(
        activity=activity_a, event_registration=event_registration_a
    )
    ActivityRegistration.objects.create(
        activity=activity_b, event_registration=event_registration_b
    )

    # QUANDO a API é chamada para listar as inscrições do usuário no evento A.
    resp = api_client.get(
        "{}?user_public_id={}&event_slug={}".format(
            reverse("activity-registration-list"), user.public_id, event_a.slug
        )
    )

    # ENTÃO apenas a inscrição do usuário na atividade do evento A será retornada.
    assert resp.status_code == status.HTTP_200_OK
    assert len(resp.data) == 1
    assert resp.data[0]["activity"]["id"] == activity_a.id
