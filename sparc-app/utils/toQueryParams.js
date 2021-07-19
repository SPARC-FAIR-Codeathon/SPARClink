/**
 * Turn a key value pair into a query param
 * @param {String} key
 * @param {String} value
 * @returns {String}
 */
const toParam = (key, value) => {
  return `${key}=${encodeURIComponent(value)}`
}

/**
 * Take an object and transform it into URL query parameters
 * @param {Object} params
 * @returns {String}
 */
const toQueryParams = params =>
  Object.keys(params)
    .map(key => {
      if (Array.isArray(params[key])) {
        return params[key]
          .map(param => {
            return toParam(key, param)
          })
          .join('&')
      }

      return toParam(key, params[key])
    })
    .join('&')

export default toQueryParams
