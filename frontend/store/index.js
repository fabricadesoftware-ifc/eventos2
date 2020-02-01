import dayjs from '~/utils/dayjs'
import { parseEventSlug } from '~/utils/url'

export const state = () => ({
  event: null,
  userEventRegistration: null,
  locale: null
})

export const mutations = {
  setEvent(state, event) {
    state.event = event
  },
  setLocale(state, locale) {
    state.locale = locale
  },
  setUserEventRegistration(state, registration) {
    state.userEventRegistration = registration
  }
}

export const actions = {
  async nuxtServerInit({ dispatch, state }, { error, req }) {
    const eventSlug = parseEventSlug(req.headers.host)
    if (eventSlug === null) {
      error({ statusCode: 404, message: 'Event not found' })
    }
    await dispatch('fetchEvent', eventSlug)
    if (state.event === null) {
      error({ statusCode: 404, message: 'Event not found' })
    }
    await dispatch('fetchEventRegistration')
  },
  async fetchEvent({ commit }, eventSlug) {
    let event = null
    try {
      event = await this.$api.event.getBySlug(eventSlug)
    } catch {}
    commit('setEvent', event)
  },
  async fetchEventRegistration({ commit, state }) {
    let eventRegistration = null
    if (state.event && this.$auth.user) {
      try {
        const eventRegistrations = await this.$api.eventRegistration.listByUserAndEvent(
          {
            userId: this.$auth.user.id,
            eventId: state.event.id
          }
        )
        if (eventRegistrations.length > 0) {
          eventRegistration = eventRegistrations[0]
        }
      } catch {}
    }

    commit('setUserEventRegistration', eventRegistration)
  }
}

export const getters = {
  eventName(state) {
    if (state.event === null) {
      return null
    }
    if (state.locale === 'en' && state.event.name_english) {
      return state.event.name_english
    }
    return state.event.name
  },
  eventStartDate(state) {
    if (state.event === null) {
      return null
    }
    return dayjs(state.event.starts_on).locale(state.locale)
  },
  eventEndDate(state) {
    if (state.event === null) {
      return null
    }
    return dayjs(state.event.ends_on).locale(state.locale)
  },
  eventRegistrationTypes(state) {
    if (state.event === null) {
      return null
    }
    return state.event.registration_types.map(registrationType => {
      let localizedName = registrationType.name
      if (state.locale === 'en' && registrationType.name_english) {
        localizedName = registrationType.name_english
      }
      return {
        id: registrationType.id,
        name: localizedName
      }
    })
  },
  eventUserRegistration(state) {
    if (state.userEventRegistration === null) {
      return null
    }
    const registration = state.userEventRegistration
    let localizedName = registration.registration_type.name
    if (state.locale === 'en' && registration.registration_type.name_english) {
      localizedName = registration.registration_type.name_english
    }
    return {
      registration_type: {
        id: registration.registration_type.id,
        name: localizedName
      }
    }
  }
}
