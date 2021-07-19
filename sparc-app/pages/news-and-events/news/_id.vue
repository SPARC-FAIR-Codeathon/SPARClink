<template>
  <news-events-page
    :page="page"
    :content="page.fields.copy"
    :breadcrumb="breadcrumb"
    :hero-title="page.fields.title"
    :hero-summary="page.fields.summary"
    type="news"
  >
    <template v-if="newsImage">
      <img :src="newsImage" :alt="newsImageAlt" />
      <hr />
    </template>

    <h3>Published Date</h3>
    <p>{{ publishedDate }}</p>

    <h3>External Link</h3>
    <p>
      <a :href="page.fields.url" target="_blank">
        {{ page.fields.title }}
      </a>
    </p>
  </news-events-page>
</template>

<script>
import { pathOr } from 'ramda'

import NewsEventsPage from '@/components/NewsEventsPage/NewsEventsPage'

import FormatDate from '@/mixins/format-date'

import createClient from '@/plugins/contentful.js'

const client = createClient()

export default {
  name: 'NewsPage',

  components: {
    NewsEventsPage
  },

  mixins: [FormatDate],

  async asyncData({ route }) {
    try {
      const page = await client.getEntry(route.params.id)
      return { page }
    } catch (error) {
      return {
        page: {
          fields: []
        }
      }
    }
  },

  data() {
    return {
      breadcrumb: [
        {
          label: 'Home',
          to: {
            name: 'index'
          }
        },
        {
          label: 'News & Events',
          to: {
            name: 'news-and-events'
          }
        }
      ]
    }
  },

  computed: {
    /**
     * Get news and event image
     * @returns {String}
     */
    newsImage: function() {
      return pathOr('', ['fields', 'image', 'fields', 'file', 'url'], this.page)
    },

    /**
     * Get news and event image alt tag
     * @returns {String}
     */
    newsImageAlt: function() {
      return pathOr('', ['fields', 'image', 'fields', 'title'], this.page)
    },

    /**
     * Compute and formate start date
     * @returns {String}
     */
    publishedDate: function() {
      return this.page.fields.publishedDate
        ? this.formatDate(this.page.fields.publishedDate)
        : ''
    }
  }
}
</script>
