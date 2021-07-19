<template>
  <img
    ref="img"
    :src="bannerSrc"
    class="event-image"
    alt="Event Banner Image"
  />
</template>

<script>
export default {
  name: 'EventBannerImage',
  props: {
    src: {
      type: String,
      default: ''
    }
  },

  data() {
    return {
      bannerSrc: ''
      //   publicPath: process.env.BASE_URL || '/'
    }
  },

  computed: {
    /**
     * Compute broken image path
     * @return {String}
     */
    brokenImage: function() {
      return `@/static/images/icon-broken-image.svg`
    }
  },

  watch: {
    src: {
      handler: function(val) {
        this.bannerSrc = val
      },
      immediate: true
    }
  },

  mounted: function() {
    // Add listener for onerror
    this.$refs.img.onerror = this.onError
  },

  methods: {
    /**
     * Set the source as the brokenImage URL
     */
    onError: function() {
      this.bannerSrc = this.brokenImage
    }
  }
}
</script>
<style lang="scss" scoped>
img {
  height: auto;
  max-width: 400px;
  width: 100%;
}
</style>
