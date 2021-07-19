<template>
  <div>
    <breadcrumb :breadcrumb="breadcrumb" title="News" />
    <page-hero>
      <h1>Latest News</h1>
      <p>
        Check out the latest announcements about the SPARC Portal and the latest
        news about the SPARC program.
      </p>
    </page-hero>
    <div class="page-wrap container">
      <div ref="newsWrap" class="subpage">
        <news-list-item
          v-for="item in news.items"
          :key="item.sys.id"
          :item="item"
        />
      </div>
      <div class="metadata-table-pagination">
        <pagination
          :selected="curSearchPage"
          :page-size="news.limit"
          :total-count="news.total"
          @select-page="onPaginationPageChange"
        />
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import Vue from 'vue'

import Breadcrumb from '@/components/Breadcrumb/Breadcrumb.vue'
import PageHero from '@/components/PageHero/PageHero.vue'
import NewsListItem from '@/components/NewsListItem/NewsListItem.vue'
import Pagination from '@/components/Pagination/Pagination.vue'

import createClient from '@/plugins/contentful.js'

import { fetchNews, NewsData, NewsComputed, NewsMethods } from '../model'

const client = createClient()
const MAX_NEWS_ITEMS = 10

export default Vue.extend<NewsData, NewsMethods, NewsComputed, never>({
  name: 'NewsPage',

  components: {
    Breadcrumb,
    PageHero,
    NewsListItem,
    Pagination
  },

  async asyncData() {
    const news = await fetchNews(client, '', MAX_NEWS_ITEMS)

    return {
      news
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
     * Compute the current page based off the limit and the offset
     * @returns {Number}
     */
    curSearchPage: function() {
      return this.news.skip / this.news.limit + 1
    }
  },

  methods: {
    /**
     * Get more news for the new page
     * @param {Number} page
     */
    async onPaginationPageChange(page) {
      const { limit } = this.news
      const offset = (page - 1) * limit
      const response = await fetchNews(client, '', limit, offset)
      this.news = response
      this.$refs.newsWrap.scrollIntoView()
    }
  }
})
</script>

<style lang="scss" scoped>
.news-list-item {
  border-top: 2px solid #d8d8d8;
  padding: 1.5em 0;
  &:first-child {
    border: none;
    padding-top: 0;
  }
  &:last-child {
    padding-bottom: 0;
  }
}
.subpage {
  margin-bottom: 1.5rem;
}
.page-wrap {
  margin-bottom: 2.5rem;
}
::v-deep {
  .page-hero__copy {
    max-width: none;
  }
}
</style>
