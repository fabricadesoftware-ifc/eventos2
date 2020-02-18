export function createEventRegistrationTypeAPIClient($axios) {
  return {
    create({ eventId, name, nameInEnglish }) {
      return $axios.$post(`api/v1/event_registration_types/`, {
        event: eventId,
        name,
        name_english: nameInEnglish
      })
    },
    update({ eventRegistrationTypeId, name, nameInEnglish }) {
      return $axios.$put(
        `api/v1/event_registration_types/${eventRegistrationTypeId}/`,
        {
          name,
          name_english: nameInEnglish
        }
      )
    },
    destroy(eventRegistrationTypeId) {
      return $axios.$delete(
        `api/v1/event_registration_types/${eventRegistrationTypeId}`
      )
    }
  }
}
