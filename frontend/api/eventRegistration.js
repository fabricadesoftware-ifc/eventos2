export function createEventRegistrationAPIClient($axios) {
  return {
    listByUserAndEvent({ userId, eventSlug }) {
      return $axios.$get(`api/v1/event_registrations/`, {
        params: {
          user_id: userId,
          event_slug: eventSlug
        }
      })
    },
    register({ eventSlug }) {
      return $axios.$post(`api/v1/event_registrations/`, {
        event: eventSlug
      })
    }
  }
}
