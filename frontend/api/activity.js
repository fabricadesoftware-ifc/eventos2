export function createActivityAPIClient($axios) {
  return {
    getBySlug(slug) {
      return $axios.$get(`api/v1/activities/${slug}/`)
    },
    create({ eventId, slug, name, name_english, starts_on, ends_on }) {
      return $axios.$post(`api/v1/activities/`, {
        event: eventId,
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
      return $axios.$put(`api/v1/activities/${currentSlug}/`, {
        slug: newSlug,
        name,
        name_english,
        starts_on,
        ends_on
      })
    }
  }
}
