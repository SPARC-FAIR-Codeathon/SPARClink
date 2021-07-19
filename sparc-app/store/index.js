import createClient from '~/plugins/contentful'

export const state = () => ({
  disableScrolling: false,
  footerData: {},
  hasAcceptedGDPR: false
})

export const mutations = {
  UPDATE_DISABLED_SCROLLING(state, data) {
    state.disableScrolling = data
  },
  SET_FOOTER_DATA(state, data) {
    state.footerData = data
  },
  SET_HAS_ACCEPTED_GDPR(state, hasAcceptedGDPR) {
    state.hasAcceptedGDPR = hasAcceptedGDPR
  }
}

export const actions = {
  updateDisabledScrolling: ({ commit }, state) => {
    commit('UPDATE_DISABLED_SCROLLING', state)
  },
  setHasAcceptedGdpr: ({ commit }, state) => {
    commit('SET_HAS_ACCEPTED_GDPR', state)
  },
  async nuxtServerInit({ commit, dispatch }) {
    try {
      const client = createClient()
      const response = await client.getEntry(process.env.ctf_footer_copy_id)
      commit('SET_FOOTER_DATA', response.fields)

      // Load GDPR cookie info
      const hasAcceptedGDPR = this.$cookies.get('GDPR:accepted')
      dispatch('setHasAcceptedGdpr', hasAcceptedGDPR)
    } catch (e) {
      console.error(e)
    }
  }
}
