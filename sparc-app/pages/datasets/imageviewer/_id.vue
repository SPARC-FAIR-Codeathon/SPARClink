<template>
  <div class="file-detail-page">
    <div class="page-wrap container">
      <div class="subpage">
        <div class="page-heading">
          <h1>{{ imageName }}</h1>
        </div>
        <div class="file-detail">
          <strong class="file-detail__column">File Details</strong>
        </div>
        <div class="file-detail">
          <strong class="file-detail__column">Description</strong>
          <div class="file-detail__column">
            {{ imageInfo.description }}
          </div>
        </div>
        <div class="file-detail">
          <strong class="file-detail__column">Type</strong>
          <div class="file-detail__column">
            {{ imageType }}
          </div>
        </div>
        <div class="file-detail">
          <strong class="file-detail__column">Dataset id</strong>
          <div class="file-detail__column">
            {{ datasetId }}
          </div>
        </div>
        <div class="file-detail">
          <strong class="file-detail__column">Version</strong>
          <div class="file-detail__column">
            {{ versionNumber }}
          </div>
        </div>
      </div>
      <detail-tabs
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
import biolucida from '@/services/biolucida'

import BiolucidaViewer from '@/components/BiolucidaViewer/BiolucidaViewer'
import DetailTabs from '@/components/DetailTabs/DetailTabs.vue'

export default {
  name: 'ImageViewerPage',

  components: {
    BiolucidaViewer,
    DetailTabs
  },

  async asyncData({ route }) {
    const response = await biolucida.getImageInfo(route.params.id)
    const imageInfo = response.data

    return {
      imageInfo
    }
  },

  data: () => {
    return {
      tabs: [
        {
          label: 'Image Viewer',
          type: 'viewer'
        }
      ],
      activeTab: 'viewer',
      file: {}
    }
  },

  computed: {
    /**
     * Compute biolucida data
     * @returns {Object}
     */
    biolucidaData: function() {
      return {
        biolucida_image_id: '',
        share_link: process.env.BL_SHARE_LINK_PREFIX + this.$route.query.view,
        status: ''
      }
    },

    /**
     * Return the dataset id from the route query.
     * @returns String
     */
    datasetId: function() {
      return this.$route.query.dataset_id
    },

    /**
     * Return the version number from the route query.
     * @returns String
     */
    versionNumber: function() {
      return this.$route.query.dataset_version
    },

    /**
     * Return the image name without extension from the image information.
     * @returns String
     */
    imageName: function() {
      let imageName = this.imageInfo.name
      return imageName.substring(0, imageName.lastIndexOf('.')) || imageName
    },

    /**
     * Return the type of an image.
     * @returns String
     */
    imageType: function() {
      return this.imageInfo.name.toUpperCase().endsWith('JPX')
        ? '3D JPEG Image'
        : '2D JPEG Image'
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
