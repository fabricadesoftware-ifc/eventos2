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
    let eventSlug = null
    const slugFromEnv = process.env.EVENTOS2_FRONTEND_FORCE_SLUG
    if (process.server && slugFromEnv) {
      eventSlug = slugFromEnv
    } else {
      eventSlug = parseEventSlug(req.headers.host)
    }
    if (eventSlug === null) {
      error({ statusCode: 404, message: 'Event not found' })
      return
    }
    await dispatch('fetchEvent', eventSlug)
    if (state.event === null) {
      error({ statusCode: 404, message: 'Event not found' })
      return
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
      .loginWith('refresh', { data: { email, password } })
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
            userPublicId: this.$auth.user.public_id,
            eventSlug: state.event.slug
          }
        )
      } catch {}
    }
    commit('setEventRegistration', eventRegistrations[0] || null)
  },
  createEventRegistration({ commit, state }) {
    return this.$api.eventRegistration
      .register({
        eventSlug: state.event.slug
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
    return dayjs(state.event.starts_on)
  },
  eventEndDate(state) {
    if (state.event === null) {
      return null
    }
    return dayjs(state.event.ends_on)
  },
  eventUserRegistration(state) {
    return state.eventRegistration
  }
}
