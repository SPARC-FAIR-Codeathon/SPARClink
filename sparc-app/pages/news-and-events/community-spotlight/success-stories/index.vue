<template>
  <div class="help-page">
    <breadcrumb :breadcrumb="breadcrumb" title="Success Stories" />
    <page-hero>
      <h1>Success Stories</h1>
      <br />
      <p>
        Learn how researchers have used the SPARC Program to advance
        neuromodulation of the ANS. Submit your success story
      </p>
    </page-hero>
    <div class="page-wrap container">
      <community-spotlight-listings :stories="shownStories" />
    </div>
    <pagination
      v-if="allStories.length > pageSize"
      :page-size="pageSize"
      :total-count="allStories.length"
      layout="prev, pager, next"
      @select-page="pageChange"
    />
  </div>
</template>

<script>
import createClient from '@/plugins/contentful.js'
import PageHero from '@/components/PageHero/PageHero.vue'
import Breadcrumb from '@/components/Breadcrumb/Breadcrumb.vue'
import Pagination from '@/components/Pagination/Pagination.vue'
import CommunitySpotlightListings from '@/components/CommunitySpotlight/CommunitySpotlightListings.vue'

const client = createClient()

export default {
  name: 'CommunityPage',

  components: {
    Breadcrumb,
    PageHero,
    CommunitySpotlightListings,
    Pagination
  },

  async asyncData() {
    const successData = await client.getEntries({
      content_type: 'successStory'
    })
    return {
      allStories: successData.items
    }
  },

  data() {
    return {
      allStories: [],
      pageSize: 4,
      page: 1,
      videoSrc: '',
      isLoadingSearch: false,
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
        },
        {
          label: 'Community Spotlight',
          to: {
            name: 'news-and-events-community-spotlight'
          }
        }
      ]
    }
  },

  computed: {
    shownStories: function() {
      return this.allStories.slice(
        (this.page - 1) * this.pageSize,
        this.page * this.pageSize
      )
    }
  },

  methods: {
    pageChange: function(val) {
      this.page = val
    }
  }
}
</script>

<style lang="scss" scoped>
@import '@/assets/_variables.scss';
.page-wrap {
  max-width: 80em;
}

.subpage {
  margin-bottom: 20px;
}
</style>
