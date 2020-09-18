export function createTrackAPIClient($axios) {
  return {
    getBySlug(slug) {
      return $axios.$get(`api/v1/tracks/${slug}/`)
    },
    create({ eventSlug, slug, name, name_english, starts_on, ends_on }) {
      return $axios.$post(`api/v1/tracks/`, {
        event_slug: eventSlug,
        slug,
        name,
        name_english,
        starts_on,
        ends_on
      })
    },
    update(
      currentSlug,
      { slug: newSlug, name, name_english, starts_on, ends_on }
    ) {
      return $axios.$put(`api/v1/tracks/${currentSlug}/`, {
        slug: newSlug,
        name,
        name_english,
        starts_on,
        ends_on
      })
    },
    listSubmissionDocumentSlots(slug) {
      return $axios.$get(`api/v1/tracks/${slug}/submission_document_slots/`)
    },
    listSubmissions(slug) {
      return $axios.$get(`api/v1/tracks/${slug}/submissions/`)
    }
  }
}
