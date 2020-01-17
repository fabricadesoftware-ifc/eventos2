import dayjs from '~/utils/dayjs'
import { parseEventSlug } from '~/utils/url'

export const state = () => ({
  event: null,
  locale: null
})

export const mutations = {
  setEvent(state, event) {
    state.event = event
  },
  setLocale(state, locale) {
    state.locale = locale
  }
}

export const actions = {
  nuxtServerInit({ commit }, { app, error, req }) {
    const eventSlug = parseEventSlug(req.headers.host)
    if (eventSlug === null) {
      commit('setEvent', null)
      error({ statusCode: 404, message: 'Event not found' })
      return
    }

    return app.$api.event
      .getBySlug(eventSlug)
      .then(event => commit('setEvent', event))
      .catch(() => error({ statusCode: 404, message: 'Event not found' }))
  }
}

export const getters = {
  eventName(state) {
    if (state.event === null) {
      return null
    }
    return state.locale === 'en' ? state.event.name_english : state.event.name
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
  }
}
