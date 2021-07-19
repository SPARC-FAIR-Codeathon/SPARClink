import EventBus from '@/static/js/event-bus'
import Logger from '@/mixins/logger'
import { prop, propOr } from 'ramda'

const _isString = x => Object.prototype.toString.call(x) === '[object String]'

const _trimValues = obj => {
  Object.keys(obj).forEach(key => {
    if (_isString(obj[key])) {
      obj[key] = obj[key].trim()
    }
  })
}

export default {
  mixins: [Logger],
  data() {
    return {
      method: 'GET',
      body: null,
      isLoading: true
    }
  },
  methods: {
    /**
     * Sends an XHR request
     * @param {Object} opts
     * @returns {Promise}
     */
    sendXhr: function(url, opts, returnRawResponse = false) {
      if (!url) {
        return Promise.reject(new Error('Url is missing!'))
      }

      this.isLoading = true
      this.method = propOr('GET', 'method', opts)

      const optsHeader = propOr(null, 'header', opts)
      const headers = optsHeader || { 'Content-type': 'application/json' }

      const optsBody = propOr('', 'body', opts)
      let requestOpts = { headers, method: this.method }

      if (optsBody) {
        if (typeof optsBody === 'object') {
          _trimValues(optsBody)
        }
        this.body = JSON.stringify(optsBody)
        requestOpts = {
          requestOpts,
          body: this.body
        }
      }

      return fetch(url, requestOpts).then(resp => {
        if (resp.status >= 400) {
          return Promise.reject(resp)
        }

        // most common cases work processing the response as json, otherwise we have the option to parse per usecase
        if (returnRawResponse) {
          return this.finishLoading(resp)
        }

        // if the payload cannot be converted to json, return a clone of the original response
        return resp
          .json()
          .then(this.finishLoading.bind(this))
          .catch(() => this.finishLoading(resp))
      })
    },
    /**
     * Update isLoading on $nextTick
     * @param {Object} json
     * @returns {Object}
     */
    finishLoading: function(json) {
      this.$nextTick(() => {
        this.isLoading = false
      })
      return json
    },
    /**
     * Handles ajax errors
     * @param {Object} err
     */
    handleXhrError: function(err) {
      this.isLoading = false
      const status = prop('status', err)
      // logout
      if (status === 401) {
        return this.handleLogout()
      }
      // unauthorized
      if (status === 403) {
        console.error('unauthorized')
        // return this.$router.replace({name: 'datasets-list'})
      }
      // emit ajaxError
      EventBus.$emit('ajaxError', err)
    }
  }
}
