export function createTrackSubmissionDocumentSlotAPIClient($axios) {
  return {
    getById(id) {
      return $axios.$get(`api/v1/track_submission_document_slots/${id}/`)
    },
    create({ trackSlug, name, name_english, starts_on, ends_on }) {
      return $axios.$post(`api/v1/track_submission_document_slots/`, {
        track_slug: trackSlug,
        name,
        name_english,
        starts_on,
        ends_on
      })
    },
    update(id, { name, name_english, starts_on, ends_on }) {
      return $axios.$put(`api/v1/track_submission_document_slots/${id}/`, {
        name,
        name_english,
        starts_on,
        ends_on
      })
    }
  }
}
