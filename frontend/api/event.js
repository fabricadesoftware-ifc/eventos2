export function createEventAPIClient($axios) {
  return {
    getBySlug(slug) {
      return $axios.$get(`api/v1/events/${slug}/`)
    }
  }
}
