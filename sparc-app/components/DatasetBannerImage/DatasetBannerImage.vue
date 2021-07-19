<template>
  <img
    ref="img"
    :src="bannerSrc"
    class="dataset-image"
    alt="Dataset Banner Image"
  />
</template>

<script>
import brokenImage from '@/static/images/icon-broken-image.svg'

export default {
  name: 'DatasetBannerImage',
  props: {
    src: {
      type: String,
      default: ''
    }
  },

  data() {
    return {
      bannerSrc: '',
      brokenImage
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

<style scoped lang="scss">
.dataset-image {
  width: 368px;
  height: 368px;
}
@media screen and (max-width: 360px) {
  .dataset-image {
    width: 288px;
    height: 288px;
    margin-left: 1rem;
  }
}

@media screen and (max-width: 320px) {
  .dataset-image {
    margin-left: 0;
  }
}
</style>
