<template>
  <div class="help-card">
    <h3>
      <nuxt-link class="help-link" :to="helpLink">
        {{ helpItem.fields ? helpItem.fields.title : '' }}
      </nuxt-link>
    </h3>
    <p
      v-html="
        highlightText(
          searchTerms,
          helpItem.fields ? helpItem.fields.summary : ''
        )
      "
    />
  </div>
</template>

<script>
import { pathOr } from 'ramda'

import HighlightText from '@/mixins/highlight-text'

export default {
  name: 'HelpCard',

  mixins: [HighlightText],

  props: {
    helpItem: {
      type: Object,
      default: () => {
        return {
          sys: {},
          fields: {}
        }
      }
    },
    searchTerms: {
      type: String,
      default: ''
    }
  },

  computed: {
    /**
     * Compute the link to the help article
     * This will use the slug if available, and fallback
     * to the ID of the entry if not
     * @returns {Object}
     */
    helpLink() {
      const sysId = pathOr('', ['sys', 'id'], this.helpItem)
      const helpId = pathOr(sysId, ['fields', 'slug'], this.helpItem)
      return { name: 'help-helpId', params: { helpId } }
    }
  }
}
</script>

<style lang="scss" scoped>
@import '@/assets/_variables.scss';
.help-card {
  h3 {
    margin-bottom: 0;
  }
}
.help-link {
  color: $median;
  font-size: 24px;
}
.help-link:not(:hover) {
  text-decoration: none;
}
</style>
