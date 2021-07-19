<template>
  <div class="file-detail-page">
    <div class="page-wrap container">
      <div class="subpage">
        <div class="page-heading">
          <h1>{{ file.name }}</h1>
          <div class="page-heading__button">
            <bf-button @click="requestDownloadFile(file)">
              Download
            </bf-button>
          </div>
        </div>
        <div class="file-detail">
          <strong class="file-detail__column">File Details</strong>
        </div>
        <div class="file-detail">
          <strong class="file-detail__column">Type</strong>
          <div class="file-detail__column">
            {{ file.fileType }}
          </div>
        </div>
        <div class="file-detail">
          <strong class="file-detail__column">Size</strong>
          <div class="file-detail__column">
            {{ formatMetric(file.size) }}
          </div>
        </div>
        <div class="file-detail">
          <strong class="file-detail__column">Date Created</strong>
          <div class="file-detail__column">
            {{ formatDate(file.createdAt) }}
          </div>
        </div>
        <div class="file-detail">
          <strong class="file-detail__column">Location</strong>
          <div class="file-detail__column">
            {{ location }}
          </div>
        </div>
      </div>
      <detail-tabs
        v-if="hasViewer"
        :tabs="tabs"
        :active-tab="activeTab"
        class="container"
        @set-active-tab="activeTab = $event"
      >
        <biolucida-viewer
          v-show="activeTab === 'viewer'"
          :data="biolucidaData"
        />
      </detail-tabs>
    </div>
  </div>
</template>

<script>
import BiolucidaViewer from '@/components/BiolucidaViewer/BiolucidaViewer'
import DetailTabs from '@/components/DetailTabs/DetailTabs.vue'
import BfButton from '@/components/shared/BfButton/BfButton.vue'

import BfStorageMetrics from '@/mixins/bf-storage-metrics'
import FormatDate from '@/mixins/format-date'
import RequestDownloadFile from '@/mixins/request-download-file'

export default {
  name: 'FileDetailPage',

  components: {
    BiolucidaViewer,
    DetailTabs,
    BfButton
  },

  mixins: [BfStorageMetrics, FormatDate, RequestDownloadFile],

  async asyncData({ route, $axios }) {
    const fileUrl = `${process.env.discover_api_host}/datasets/${route.params.datasetId}/versions/${route.params.datasetVersion}/files?path=${route.query.path}`

    const file = await $axios.$get(fileUrl)

    const sourcePackageId = file.sourcePackageId
    const biolucidaData = await $axios.$get(
      `${process.env.BL_SERVER_URL}/imagemap/sharelink/${sourcePackageId}`
    )

    const hasViewer = biolucidaData.status !== 'error'

    return {
      biolucidaData,
      file,
      hasViewer
    }
  },

  data: () => {
    return {
      biolucidaData: {
        biolucida_image_id: '',
        share_link: '',
        status: ''
      },
      tabs: [
        {
          label: 'Viewer',
          type: 'viewer'
        }
      ],
      activeTab: 'viewer',
      file: {}
    }
  },

  computed: {
    /**
     * Compute location of the file
     * @returns {String}
     */
    location: function() {
      return this.file.path.replace(`/${this.file.name}`, '')
    }
  }
}
</script>

<style scoped lang="scss">
.page {
  display: flex;
  margin-top: 7rem;

  p {
    color: #606266;
  }
}

.about {
  text-align: center;
  min-height: 50vh;
  margin-top: 9rem;
}

h1 {
  flex: 1;
  font-size: 1.5em;
  line-height: 2rem;
}
.page-heading {
  display: flex;
  flex-direction: column;
  margin-bottom: 1.375rem;
  @media (min-width: 48em) {
    flex-direction: row;
  }
}
.page-heading__button {
  flex-shrink: 0;
}

.file-detail {
  border-bottom: 1px solid #dbdfe6;
  flex-direction: column;
  font-size: 0.875em;
  display: flex;
  padding: 1rem 0.625rem;
  @media (min-width: 48em) {
    flex-direction: row;
  }
}
.file-detail__column {
  flex: 1;
}
</style>
