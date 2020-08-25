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
  async nuxtServerInit({ dispatch, state }, { app, error, req, $config }) {
    const eventSlug = $config.forceEventSlug || parseEventSlug(req.headers.host)
    if (eventSlug === null) {
      error({
        statusCode: 404,
        message: app.i18n.t('genericErrors.eventNotFound')
      })
      return
    }
    try {
      await dispatch('fetchEvent', eventSlug)
    } catch (err) {
      if (err.name === 'APIValidationError' || err.name === 'APIError') {
        error({
          statusCode: 404,
          message: app.i18n.t('genericErrors.eventNotFound')
        })
      } else {
        error({
          statusCode: (err.response && err.response.status) || err.code || null,
          message:
            (err.response && err.response.data) ||
            err.message ||
            app.i18n.t('genericErrors.network')
        })
      }
      return
    }
    await dispatch('fetchEventRegistration')
  },
  fetchEvent({ commit }, eventSlug) {
    return this.$api.event
      .getBySlug(eventSlug)
      .then(event => commit('setEvent', event))
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
