export default {
  methods: {
    /**
     * Returns an instance of console
     * @param {Array} fnArgs to pass to console
     * @param {String} fnName method to use, i.e., warn, log, error, trace, etc.
     * @param {Boolean} disabled turns logging off completely
     * @returns {Object} console function or no-op
     */
    logger: function(fnArgs, fnName = 'log', disabled = false) {
      if (disabled) {
        return
      }
      const msg = Array.isArray(fnArgs) ? fnArgs : [fnArgs]
      const isProduction = location.href.indexOf('data.sparc.science') >= 0
      /* eslint-disable no-console */
      if (!isProduction && typeof console[fnName] === 'function') {
        console[fnName].apply(console, msg)
      }
      /* eslint-enable no-console */
    }
  }
}
