export function createTrackAPIClient($axios) {
  return {
    getById(id) {
      return $axios.$get(`api/v1/tracks/${id}/`)
    },
    create({ eventSlug, name, name_english, starts_on, ends_on }) {
      return $axios.$post(`api/v1/tracks/`, {
        event_slug: eventSlug,
        name,
        name_english,
        starts_on,
        ends_on
      })
    },
    update(id, { name, name_english, starts_on, ends_on }) {
      return $axios.$put(`api/v1/tracks/${id}/`, {
        name,
        name_english,
        starts_on,
        ends_on
      })
    },
    listSubmissionDocumentSlots(id) {
      return $axios.$get(`api/v1/tracks/${id}/submission_document_slots/`)
    },
    listSubmissions(id) {
      return $axios.$get(`api/v1/tracks/${id}/submissions/`)
    }
  }
}
