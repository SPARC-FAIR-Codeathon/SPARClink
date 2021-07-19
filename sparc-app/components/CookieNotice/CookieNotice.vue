<template>
  <div class="cookie-notice">
    <div class="container">
      <div class="cookie-notice__content">
        <div class="cookie-notice__copy">
          <h2>
            This website uses cookies to ensure that you get the best
            experience.
          </h2>
          <p>
            To learn more, please refer to the
            <nuxt-link to="privacy">
              Privacy Policy.
            </nuxt-link>
            By closing this banner or clicking accept, you agree to the use of
            cookies.
          </p>
          <a href="#" @click.prevent="openAccessibilityDialog">Accessibility Standards</a>
        </div>
        <div>
          <bf-button class="primary" @click="closeNotice">
            Accept
          </bf-button>
        </div>
      </div>
    </div>
    <button class="btn-close" @click="closeNotice">
      <svg-icon name="icon-remove" height="10" width="10" />
    </button>
    <accessibility-dialog
      :visible.sync="accessibilityDialogVisible"
      @close="closeAccessibilityDialog"
    />
  </div>
</template>

<script>
import AccessibilityDialog from '@/components/AccessibilityDialog/AccessibilityDialog.vue'
import BfButton from '@/components/shared/BfButton/BfButton'
export default {
  name: 'CookieNotice',

  components: {
    BfButton,
    AccessibilityDialog
  },

  data() {
    return {
      accessibilityDialogVisible: false
    }
  },

  methods: {
    /**
     * Close notice and accept the policy
     */
    closeNotice: function() {
      const today = new Date()
      const expirationDate = new Date(today.setDate(today.getDate() + 30))
      this.$cookies.set('GDPR:accepted', true, { expires: expirationDate })
      this.$store.dispatch('setHasAcceptedGdpr', true)
    },

    /**
     * Opens Accessibility Dialog
     */
    openAccessibilityDialog: function() {
      this.accessibilityDialogVisible = true
    },

     /**
      * Closes Accessibility Dialog
      */
    closeAccessibilityDialog: function() {
      this.accessibilityDialogVisible = false
    }
  }
}
</script>

<style lang="scss" scoped>
@import '../../assets/_variables.scss';
.cookie-notice {
  background: #fff;
  bottom: 0;
  box-shadow: 0px -2px 8px 0px rgba(0, 0, 0, 0.07);
  color: $navy;
  left: 0;
  right: 0;
  padding: 2rem 0;
  position: fixed;
  z-index: 9;
}
.cookie-notice__content {
  max-width: 80%;
  @media (min-width: 48em) {
    align-items: center;
    display: flex;
    max-width: none;
    justify-content: space-between;
  }
}
.cookie-notice__copy {
  margin-bottom: 1em;
  @media (min-width: 48em) {
    margin: 0 1em 0 0;
    max-width: 53.75em;
  }
}
h2 {
  font-size: 1.1em;
  margin: 0;
  line-height: 1.2;
  @media (min-width: 48em) {
    font-size: 1.5em;
  }
}
a {
  font-size: 1em;
}
p {
  font-size: 0.875em;
  line-height: 1.2;
  margin: 0;
}
.btn-close {
  background: none;
  border: none;
  cursor: pointer;
  padding: 0.25em;
  position: absolute;
  right: 0.25rem;
  top: 0.25rem;
}
</style>
