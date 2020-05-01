export function createEventRegistrationAPIClient($axios) {
  return {
    listByUserAndEvent({ userId, eventId }) {
      return $axios.$get(`api/v1/event_registrations/`, {
        params: {
          user_id: userId,
          event_id: eventId
        }
      })
    },
    register({ eventId, userId }) {
      return $axios.$post(`api/v1/event_registrations/`, {
        event: eventId,
        user: userId
      })
    }
  }
}
