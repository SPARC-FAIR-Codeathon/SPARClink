<template>
  <div class="breadcrumb">
    <p>
      <template v-for="item in breadcrumb">
        <nuxt-link :key="item.label" :to="item.to">
          {{ item.label }}
        </nuxt-link>
        >
      </template>
      {{ formatTitle(title) }}
    </p>
  </div>
</template>

<script lang="ts">
import Vue from 'vue'

import { Methods, Props } from './model'

export default Vue.extend<never, Methods, never, Props>({
  name: 'Breadcrumb',

  props: {
    breadcrumb: {
      type: Array,
      default: () => []
    },
    title: {
      type: String,
      default: ''
    }
  },

  methods: {
    /**
     * Formats breadcrumb length
     * @param {String} breadcrumb
     */
    formatTitle: function(title) {
      return title.length > 32 ? title.substring(0, 32) + '...' : title
    }
  }
})
</script>

<style lang="scss">
@import '../../assets/_variables.scss';
.breadcrumb {
  background: $purple-gray;
  height: 2.5rem;
  margin-top: 0;
  p {
    font-size: 14px;
    font-weight: 500;
    line-height: 16px;
    padding-left: 1rem;
    padding-top: 0.75rem;
    margin-top: 0;
    color: $midnight;
  }

  a {
    text-decoration: none;
    color: $midnight;
  }
}
</style>
