export function createEventRegistrationAPIClient($axios) {
  return {
    listByUserAndEvent({ userPublicId, eventSlug }) {
      return $axios.$get(`api/v1/event_registrations/`, {
        params: {
          user_public_id: userPublicId,
          event_slug: eventSlug
        }
      })
    },
    register({ eventSlug }) {
      return $axios.$post(`api/v1/event_registrations/`, {
        event_slug: eventSlug
      })
    }
  }
}
