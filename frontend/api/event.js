export function createEventAPIClient($axios) {
  return {
    getBySlug(slug) {
      return $axios.$get(`api/v1/events/${slug}/`)
    },
    getRegistrations(slug) {
      return $axios.$get(`api/v1/events/${slug}/registrations/`)
    },
    update(
      currentSlug,
      { slug: newSlug, name, name_english, starts_on, ends_on }
    ) {
      return $axios.$put(`api/v1/events/${currentSlug}/`, {
        slug: newSlug,
        name,
        name_english,
        starts_on,
        ends_on
      })
    }
  }
}
