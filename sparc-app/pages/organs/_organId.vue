<template>
  <div class="organ-details">
    <details-header
      :subtitle="pageData.fields.subtitle"
      :title="pageData.fields.name"
      :description="pageData.fields.description"
      :breadcrumb="breadcrumb"
      :full-description="true"
    >
      <img slot="banner image" :src="bannerImage" :alt="bannerImageAlt" />
    </details-header>
    <detail-tabs
      :tabs="tabs"
      :active-tab="activeTab"
      class="container"
      @set-active-tab="setActiveTab"
    >
      <dataset-search-results
        v-show="activeTab === 'datasets'"
        :table-data="datasets"
        @sort-change="onDatasetSortChange"
      />
      <project-search-results
        v-show="activeTab === 'projects'"
        :table-data="projectTableData"
        @sort-change="onProjectsSortChange"
      />
    </detail-tabs>
  </div>
</template>

<script>
import { clone, path, pathOr, propOr } from 'ramda'

import DetailsHeader from '@/components/DetailsHeader/DetailsHeader.vue'
import DetailTabs from '@/components/DetailTabs/DetailTabs.vue'

import ProjectSearchResults from '@/components/SearchResults/ProjectSearchResults.vue'
import DatasetSearchResults from '@/components/SearchResults/DatasetSearchResults.vue'

import createClient from '@/plugins/contentful.js'

import toQueryParams from '@/utils/toQueryParams.js'

const client = createClient()

const tabs = [
  {
    label: 'Datasets',
    type: 'datasets'
  }
]

const datasetsOrder = {
  orderBy: 'date',
  orderDirection: 'asc',
  limit: '100'
}

const projectsOrder = {
  orderBy: 'fields.title',
  orderDirection: 'asc',
  limit: '100'
}

/**
 * Get datasets with sorting
 * @param {Object} pageData
 * @param {Object} $axios
 * @param {Object} orderBy
 * @returns {Array}
 */
const getDatasets = async (pageData, orderBy, $axios) => {
  const organName = pathOr('', ['fields', 'name'], pageData)

  const projectSection = pathOr(
    organName,
    ['fields', 'projectSection', 'fields', 'title'],
    pageData
  )

  const queryParams = toQueryParams({
    query: projectSection.toLowerCase(),
    ...orderBy
  })

  return await $axios.$get(
    `${process.env.discover_api_host}/search/datasets?${queryParams}`
  )
}

/**
 * Get projects with sorting
 * @param {Object} pageData
 * @param {Object} projectsOrder
 * @returns {Array}
 */
const getProjects = async (pageData, projectsOrder) => {
  try {
    const projectSectionId = path(
      ['fields', 'projectSection', 'sys', 'id'],
      pageData
    )

    const order =
      projectsOrder.orderDirection === 'asc'
        ? projectsOrder.orderBy
        : `-${projectsOrder.orderBy}`

    // Get related projects
    return projectSectionId
      ? await client
          .getEntries({
            content_type: process.env.ctf_project_id,
            order,
            links_to_entry: projectSectionId
          })
          .catch(() => {
            return []
          })
      : []
  } catch (error) {
    return []
  }
}

export default {
  name: 'OrganDetails',

  components: {
    DetailsHeader,
    DetailTabs,
    ProjectSearchResults,
    DatasetSearchResults
  },

  async asyncData({ route, $axios }) {
    // Get page content
    const pageData = await client.getEntry(route.params.organId)

    // Get related projects
    const projects = await getProjects(pageData, projectsOrder)

    // Get related datasets
    const datasets = await getDatasets(pageData, datasetsOrder, $axios)

    const tabsData = clone(tabs)

    if (projects.total > 0) {
      tabsData.push({
        label: 'Projects',
        type: 'projects'
      })
    }

    const projectTableData = propOr([], 'items', projects)

    return {
      pageData,
      datasets: datasets.datasets,
      projectTableData,
      tabs: tabsData
    }
  },

  data() {
    return {
      tabs: [],
      activeTab: 'datasets',
      datasetsOrder: { ...datasetsOrder },
      projectsOrder: { ...projectsOrder },
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
              type: 'organ'
            }
          },
          label: 'Find Data'
        }
      ]
    }
  },

  computed: {
    /**
     * Compute banner image
     * @returns {String}
     */
    bannerImage: function() {
      return pathOr(
        '',
        ['fields', 'bannerImage', 'fields', 'file', 'url'],
        this.pageData
      )
    },

    /**
     * Compute banner image alt tag
     * @returns {String}
     */
    bannerImageAlt: function() {
      return pathOr(
        '',
        ['fields', 'bannerImage', 'fields', 'description'],
        this.pageData
      )
    }
  },

  methods: {
    /**
     * Sets active tab
     * @param {String} activeLabel
     */
    setActiveTab: function(activeLabel) {
      this.activeTab = activeLabel
    },

    /**
     * Set sort for datasets and get new datsets
     * @param {Object} sortData
     */
    onDatasetSortChange: async function(sortData) {
      const orderDirection = sortData.order === 'ascending' ? 'asc' : 'desc'
      const orderBy = sortData.prop === 'createdAt' ? 'date' : sortData.prop

      this.datasetsOrder = {
        ...this.datasetsOrder,
        orderDirection,
        orderBy
      }

      const datasets = await getDatasets(
        this.pageData,
        this.datasetsOrder,
        this.$axios
      )

      this.datasets = datasets.datasets
    },

    /**
     * Set sort for projects and get new projects
     * @param {Object} sortData
     */
    onProjectsSortChange: async function(sortData) {
      const orderDirection = sortData.order === 'ascending' ? 'asc' : 'desc'
      const orderBy = sortData.prop === 'createdAt' ? 'date' : sortData.prop

      this.projectsOrder = {
        ...this.onProjectSortChange,
        orderDirection,
        orderBy
      }

      const projects = await getProjects(this.pageData, this.projectsOrder)

      this.projectTableData = projects.items || []
    }
  }
}
</script>

<style lang="scss" scoped>
::v-deep {
  .el-table td {
    vertical-align: top;
  }
}
</style>
