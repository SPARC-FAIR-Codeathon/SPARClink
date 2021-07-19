<template>
  <div class="project-details">
    <details-header
      :subtitle="projectSection"
      :title="fields.title"
      :description="fields.description"
      :full-description="true"
      :breadcrumb="breadcrumb"
    >
      <img
        slot="banner image"
        :src="getImageSrc"
        :alt="getImageAlt"
        height="368"
        width="368"
      />
      <div slot="meta content" class="details-header__container--content-meta">
        <div class="content-meta__item">
          <h3>NIH Award</h3>
          <p>{{ fields.awardId }}</p>
        </div>
        <div class="content-meta__item">
          <h3>Principal Investigator</h3>
          <p>{{ fields.principleInvestigator }}</p>
        </div>
        <div class="content-meta__item">
          <h3>Institution</h3>
          <p>{{ fields.institution.fields.name }}</p>
        </div>
      </div>
      <div slot="meta content" class="details-header__container--content-links">
        <button>
          <a :href="fields.nihReporterUrl" target="_blank">
            View on NIH Website
          </a>
        </button>
      </div>
    </details-header>
    <detail-tabs
      :tabs="tabs"
      :active-tab="activeTab"
      class="container"
      @set-active-tab="setActiveTab"
    >
      <dataset-search-results
        v-show="activeTab === 'datasets'"
        :table-data="datasets.datasets"
      />
    </detail-tabs>
  </div>
</template>

<script>
import DetailsHeader from '@/components/DetailsHeader/DetailsHeader.vue'
import DetailTabs from '@/components/DetailTabs/DetailTabs.vue'
import DatasetSearchResults from '@/components/SearchResults/DatasetSearchResults.vue'

import createClient from '@/plugins/contentful.js'

const client = createClient()

export default {
  name: 'ProjectDetails',
  components: {
    DatasetSearchResults,
    DetailsHeader,
    DetailTabs
  },

  async asyncData({ route, $axios }) {
    try {
      const project = await client.getEntry(route.params.projectId)

      const datasets = await $axios
        .$get(`${process.env.portal_api}/project/${project.fields.awardId}`)
        .catch(() => {
          return {}
        })

      return {
        fields: project.fields,
        datasets
      }
    } catch (e) {
      console.error(e)
    }
  },

  data() {
    return {
      datasets: {
        datasets: [],
        limit: 0,
        offset: 0,
        totalCount: 0
      },
      tabs: [
        {
          label: 'Datasets',
          type: 'datasets'
        }
      ],
      activeTab: 'datasets',
      breadcrumb: [
        {
          to: {
            name: 'index'
          },
          label: 'Home'
        },
        {
          to: {
            name: 'data',
            query: {
              type: 'sparcAward'
            }
          },
          label: 'Find Data'
        }
      ]
    }
  },

  computed: {
    /**
     * Get image Source
     * @returns {String}
     */
    getImageSrc: function() {
      return this.fields.institution.fields.logo
        ? this.fields.institution.fields.logo.fields.file.url
        : ''
    },

    /**
     * Get image source
     * @returns {String}
     */
    getImageAlt: function() {
      return this.fields.institution.fields.logo
        ? this.fields.institution.fields.logo.fields.file.description
        : ''
    },
    /**
     * Compute subtitle based on its project section
     * @returns {String}
     */
    projectSection: function() {
      return this.fields.projectSection
        ? this.fields.projectSection.fields.title
        : ''
    }
  },

  methods: {
    /**
     * Sets active tab
     * @param {String} activeLabel
     */
    setActiveTab: function(activeLabel) {
      this.activeTab = activeLabel
    }
  }
}
</script>

<style lang="scss" scoped>
@import '../../assets/_variables.scss';
.project-details {
  &__page-route {
    background: $purple-gray;
    height: 2.5rem;
    margin-top: 0;
    p {
      font-size: 14px;
      font-weight: 500;
      line-height: 16px;
      padding-left: 2rem;
      padding-top: 0.75rem;
      margin-top: 0;
      color: $midnight;
    }

    a {
      text-decoration: none;
      color: $midnight;
    }
  }
}
@media screen and (max-width: 768px) {
  .project-details {
    &__page-route {
      height: 3.5rem;
    }
  }
}
</style>
