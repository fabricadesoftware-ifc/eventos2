export const state = () => ({
  registrations: []
})

export const mutations = {
  setRegistrations(state, registrations) {
    state.registrations = registrations
  }
}

export const actions = {
  updateEvent({ dispatch, rootState }, data) {
    return this.$api.event
      .update(rootState.event.slug, data)
      .then(() => dispatch('fetchEvent', rootState.event.slug, { root: true }))
  },
  async fetchRegistrations({ commit, rootState }) {
    if (rootState.event === null) {
      return
    }

    await this.$api.event
      .getRegistrations(rootState.event.slug)
      .then(data => commit('setRegistrations', data))
  }
}

export const getters = {
  registrations(state) {
    return state.registrations
  }
}
