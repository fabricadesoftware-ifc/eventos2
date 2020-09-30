export function createActivityAPIClient($axios) {
  return {
    getById(id) {
      return $axios.$get(`api/v1/activities/${id}/`)
    },
    create({ eventSlug, name, name_english, starts_on, ends_on }) {
      return $axios.$post(`api/v1/activities/`, {
        event_slug: eventSlug,
        name,
        name_english,
        starts_on,
        ends_on
      })
    },
    update(id, { name, name_english, starts_on, ends_on }) {
      return $axios.$put(`api/v1/activities/${id}/`, {
        name,
        name_english,
        starts_on,
        ends_on
      })
    },
    listRegistrations(id) {
      return $axios.$get(`api/v1/activities/${id}/registrations/`)
    }
  }
}
