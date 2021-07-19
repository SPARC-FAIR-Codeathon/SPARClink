<template>
  <div class="resources">
    <breadcrumb :breadcrumb="breadcrumb" :title="title" />
    <page-hero>
      <h1>Tools &amp; Resources</h1>
      <!-- eslint-disable vue/no-v-html -->
      <!-- marked will sanitize the HTML injected -->
      <div v-html="parseMarkdown(fields.heroCopyLong)" />
      <search-controls-contentful
        placeholder="Search resources"
        path="/resources"
      />
      <img
        v-if="fields.heroImage"
        slot="image"
        class="page-hero-img"
        :src="fields.heroImage.fields.file.url"
      />
    </page-hero>
    <div class="page-wrap">
      <div class="container">
        <tab-nav
          :tabs="tabTypes"
          :active-tab="activeTab"
          @set-active-tab="setActiveTab"
        />
        <div class="page-wrap__results">
          <div class="resources-heading">
            <p>
              {{ currentResourceCount }} {{ resourceHeading }} | Showing
              <pagination-menu
                :page-size="resourceData.limit"
                @update-page-size="updateDataSearchLimit"
              />
              <el-pagination
                v-if="resourceData.limit < resourceData.total"
                :page-size="resourceData.limit"
                :pager-count="5"
                :current-page="curSearchPage"
                layout="prev, pager, next"
                :total="resourceData.total"
                @current-change="onPaginationPageChange"
              />
            </p>
          </div>
        </div>
        <div v-loading="isLoadingSearch" class="table-wrap">
          <resources-search-results :table-data="tableData" />
        </div>
        <div class="resources-heading">
          {{ currentResourceCount }} {{ resourceHeading }} | Showing
          <pagination-menu
            :page-size="resourceData.limit"
            @update-page-size="updateDataSearchLimit"
          />
          <el-pagination
            :page-size="resourceData.limit"
            :pager-count="5"
            :current-page="curSearchPage"
            layout="prev, pager, next"
            :total="resourceData.total"
            @current-change="onPaginationPageChange"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import Vue from 'vue';
import Breadcrumb from '@/components/Breadcrumb/Breadcrumb.vue'
import ResourcesSearchResults from '@/components/Resources/ResourcesSearchResults.vue'
import PageHero from '@/components/PageHero/PageHero.vue'
import PaginationMenu from '@/components/Pagination/PaginationMenu.vue'
import TabNav from '@/components/TabNav/TabNav.vue'
import createClient from '@/plugins/contentful.js'
import SearchControlsContentful from '@/components/SearchControlsContentful/SearchControlsContentful.vue';
import { Computed, Data, Methods, Resource } from '~/pages/resources/model';
import marked from '@/mixins/marked/index'

const client = createClient()

const resourceData: Data['resourceData'] = {
  limit: 10,
  skip: 0,
  items: [],
  total: 0,
  stringifySafe: () => '',
  toPlainObject: () => ({})
}

const tabTypes = [
  {
    label: 'All Resources',
    type: 'sparcPartners' as const
  },
  {
    label: 'Devices',
    type: 'Device' as const
  },
  {
    label: 'Databases',
    type: 'Databases' as const
  },
  {
    label: 'Information Services',
    type: 'Information Services' as const
  },
  {
    label: 'Software',
    type: 'Software' as const
  },
  {
    label: 'Biologicals',
    type: 'Biologicals' as const
  }
]

export default Vue.extend<Data, Methods, Computed, never>({
  name: 'Resources',

  mixins: [marked],

  components: {
    SearchControlsContentful,
    Breadcrumb,
    ResourcesSearchResults,
    PageHero,
    PaginationMenu,
    TabNav
  },

  asyncData() {
      // Get page content
      return client.getEntry(process.env.ctf_resource_hero_id as string)
      .then(({ fields }) => {
        return {
          fields,
        }
      })
      .catch(console.error)
  },

  data() {
    return {
      title: 'Tools & Resources',
      breadcrumb: [
        {
          to: {
            name: 'index'
          },
          label: 'Home'
        }
      ],
      activeTab: 'sparcPartners',
      resourceData,
      tabTypes,
      isLoadingSearch: false
    }
  },

  computed: {
    /**
     * Returns the current displayed number of resources
     * @returns {Number}
     */
    currentResourceCount: function() {
      return this.resourceData.total
    },

    /**
     * Returns data that is displayed in table
     * @returns {Array}
     */
    tableData: function() {
      return this.resourceData.items
    },

    /**
     * Compute the current search page based off the limit and the offset
     */
    curSearchPage: function() {
      return this.resourceData.skip / this.resourceData.limit + 1
    },

    /**
     * Compute singular or plural resource heading based on count
     */
    resourceHeading: function() {
      return this.currentResourceCount > 1 ? 'resources' : 'resource'
    }
  },

  watch: {
    '$route.query': function() {
      this.fetchResults()
    },

  },

  /**
   * Check the searchType param in the route and set it if it doesn't exist
   */
  mounted: function() {
    if (!this.$route.query.type) {
      const firstTabType = tabTypes[0].type

      this.$router.replace({ query: { type: firstTabType } })
    } else {
      this.fetchResults()
    }
  },

  methods: {
    /**
     * Update search limit based on pagination number selection
     * @param {Number} limit
     */
    updateDataSearchLimit: function(limit) {
      this.resourceData.skip = 0
      if (typeof limit === 'string') {
        this.resourceData.limit = this.resourceData.total
      } else {
        this.resourceData.limit = limit
      }
      this.fetchResults()
    },
    /**
     * Fetches resource results
     */
    fetchResults: function() {
      this.isLoadingSearch = true

      const entries = {
        content_type: 'sparcPartners',
        limit: this.resourceData.limit,
        skip: this.resourceData.skip,
        order: 'fields.name',
        include: 2,
        query: this.$route.query.search,
        'fields.resourceType': this.$route.query.type === 'sparcPartners'
          ? undefined
          : this.$route.query.type
      }

      client
        .getEntries<Resource>(entries)
        .then(response => {
          this.resourceData = response
        })
        .catch(console.error)
        .finally(() => {
          this.isLoadingSearch = false
        })
    },

    /**
     * Update offset
     */
    onPaginationPageChange: function(page) {
      const offset = (page - 1) * this.resourceData.limit
      this.resourceData.skip = offset

      this.fetchResults()
    },

    /**
     * Set active tab
     */
    setActiveTab: function(tab) {
      this.activeTab = tab
      this.resourceData.skip = 0
      this.$router.push({
        name: 'resources',
        query: {
          ...this.$route.query,
          type: tab
        }
      })
    }
  }
})
</script>

<style lang="scss" scoped>
@import '@/assets/_variables.scss';
.resources {
  .table-wrap {
    background: #fff;
    border: 1px solid rgb(228, 231, 237);
    padding: 16px;
  }

  .resources-heading {
    margin-top: 1rem;
  }

  ::v-deep .el-pagination {
    margin-top: -2.5em;
    text-align: right;
    background-color: transparent;
    button {
      background-color: transparent;
    }
  }

  .page-wrap {
    &__results {
      font-size: 0.875em;
      font-weight: normal;
      line-height: 1em;

      @media screen and (max-width: 768px) {
        margin-left: 0.9375rem;
      }

      p {
        margin-top: 1.5rem;
      }
    }
  }

  &__tabs {
    display: flex;
    list-style: none;
    overflow: auto;
    margin: 0;
    padding: 0;
    @media (max-width: 48em) {
      padding: 0;
      margin: 1rem 0 0;
    }
    @media (max-width: 1024px) {
      padding: 0;
    }
    li {
      margin: 0 0.625em;
      @media (min-width: 48em) {
        margin: 0 2.25em;
      }
      &:first-child {
        margin-left: 0;
      }
    }
    &--button {
      background: none;
      border-bottom: 2px solid transparent;
      color: #fff;
      cursor: pointer;
      display: block;
      font-size: 1em;
      font-weight: 500;
      outline: none;
      padding: 0;
      text-decoration: none;
      text-transform: uppercase;
      @media (min-width: 48em) {
        font-size: 0.875em;
        font-weight: normal;
        text-transform: none;
      }
      &:hover,
      &:focus,
      &.active {
        border-bottom-color: #fff;
        font-weight: 500;
      }
    }
  }
}
</style>
