<template>
  <div class="video-viewer-page">
    <div class="page-wrap container">
      <div class="subpage">
        <div class="page-heading">
          <h1>{{ fileName }}</h1>
        </div>
        <div class="file-detail">
          <strong class="file-detail__column">File Details</strong>
        </div>
        <div class="file-detail">
          <strong class="file-detail__column">Type</strong>
          <div class="file-detail__column">
            Video
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
        <client-only placeholder="Loading video ...">
          <div class="video-container">
            <video ref="vid" class="video" controls crossorigin playsinline>
              <source :src="video_src" type="video/mp4" size="1080" />
            </video>
          </div>
        </client-only>
      </detail-tabs>
    </div>
  </div>
</template>

<script>
import Plyr from 'plyr'

import DetailTabs from '@/components/DetailTabs/DetailTabs.vue'

export default {
  name: 'VideoViewerPage',

  components: {
    DetailTabs
  },

  data: () => {
    return {
      tabs: [
        {
          label: 'Video Viewer',
          type: 'video'
        }
      ],
      activeTab: 'video',
      file: {},
      traditional: true,
      backgroundToggle: true
    }
  },
  computed: {
    /**
     * Get the file name from the query parameter.
     * @returns String
     */
    fileName: function() {
      return this.$route.query.id
    },

    /**
     * Get the dataset id from the query parameter.
     * @returns Number
     */
    datasetId: function() {
      return this.$route.query.dataset_id
    },

    /**
     * Get the version number from the query parameter.
     * @returns Number
     */
    versionNumber: function() {
      return this.$route.query.dataset_version
    },

    video_src: function() {
      return `${process.env.portal_api}/s3-resource/${this.$route.query.file_path}`
    }
  },
  mounted() {
    this.player = new Plyr(this.$refs.vid)
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
<style lang="scss">
.video-container {
  padding-top: 8px;
}
.video {
  width: 100%;
}
</style>
