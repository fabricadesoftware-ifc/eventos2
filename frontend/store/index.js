import dayjs from '~/utils/dayjs'
import { parseEventSlug } from '~/utils/url'

export const state = () => ({
  event: null,
  eventRegistration: null,
  locale: null
})

export const mutations = {
  setEvent(state, event) {
    state.event = event
  },
  setLocale(state, locale) {
    state.locale = locale
  },
  setEventRegistration(state, registration) {
    state.eventRegistration = registration
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
  fetchUser({ dispatch }) {
    return this.$auth.fetchUser().then(() => dispatch('fetchEventRegistration'))
  },
  loginUser({ dispatch }, { email, password }) {
    return this.$auth
      .loginWith('local', { data: { email, password } })
      .then(() => dispatch('fetchEventRegistration'))
  },
  logoutUser({ dispatch }) {
    return this.$auth.logout().then(() => dispatch('fetchEventRegistration'))
  },
  async fetchEventRegistration({ commit, state }) {
    let eventRegistrations = []
    if (state.event && this.$auth.user) {
      try {
        eventRegistrations = await this.$api.eventRegistration.listByUserAndEvent(
          {
            userId: this.$auth.user.id,
            eventId: state.event.id
          }
        )
      } catch {}
    }
    commit('setEventRegistration', eventRegistrations[0] || null)
  },
  createEventRegistration({ commit }, registrationTypeId) {
    return this.$api.eventRegistration
      .register({
        userId: this.$auth.user.id,
        registrationTypeId
      })
      .then(data => {
        commit('setEventRegistration', data)
      })
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
    if (state.eventRegistration === null) {
      return null
    }
    const registration = state.eventRegistration
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
