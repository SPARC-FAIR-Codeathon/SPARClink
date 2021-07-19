<template>
  <nuxt-link
    v-if="isInternalLink(link.fields.url || '')"
    :to="link.fields.url"
    data-jest="nuxt-link"
  >
    {{ link.fields.title }}
  </nuxt-link>
  <a v-else :href="link.fields.longUrl || link.fields.url" target="_blank">
    {{ link.fields.title }}
  </a>
</template>

<script>
import { isInternalLink } from '@/mixins/marked/index'

export default {
  name: 'FooterLink',

  props: {
    link: {
      type: Object,
      default: () => {
        return {
          sys: {},
          fields: {}
        }
      }
    }
  },

  methods: {
    isInternalLink
  }
}
</script>
