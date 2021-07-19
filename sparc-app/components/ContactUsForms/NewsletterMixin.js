export default {
  data() {
    return {
      hasError: false,
      isSubmitting: false
    }
  },

  methods: {
    /**
     * Subscribe to Newsletter
     */
    subscribeToNewsletter() {
      this.isSubmitting = true

      this.$axios
        .post(`${process.env.portal_api}/mailchimp`, {
          email_address: this.form.email,
          first_name: this.form.firstName,
          last_name: this.form.lastName
        })
        .then(response => {
          const { title } = response.data
          if (response.data.status > 200 && title !== 'Member Exists') {
            this.hasError = true
          } else {
            this.$emit('submit', this.form.firstName)
          }
        })
        .catch(() => {
          this.hasError = true
        })
        .finally(() => {
          this.isSubmitting = false
        })
    },

    /**
     * Validate name
     * @param {Object} rule
     * @param {String} value
     * @param {Function} callback
     */
    validateForNewsletter: function(rule, value, callback) {
      if (this.form.shouldSubscribe && value === '') {
        callback(new Error(rule.message))
      }
      callback()
    }
  }
}
