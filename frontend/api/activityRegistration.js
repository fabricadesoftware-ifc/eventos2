export function createActivityRegistrationAPIClient($axios) {
  return {
    listByUserAndEvent({ userPublicId, eventSlug }) {
      return $axios.$get(`api/v1/activity_registrations/`, {
        params: {
          user_public_id: userPublicId,
          event_slug: eventSlug
        }
      })
    },
    register({ activitySlug }) {
      return $axios.$post(`api/v1/activity_registrations/`, {
        activity: activitySlug
      })
    },
    deregister({ registrationId }) {
      return $axios.$delete(`api/v1/activity_registrations/${registrationId}`)
    }
  }
}
