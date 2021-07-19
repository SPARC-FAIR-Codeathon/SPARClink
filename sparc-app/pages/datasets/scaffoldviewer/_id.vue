<template>
  <div class="scaffold-viewer-page">
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
            3D Scaffold
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
        <el-row :gutter="16">
          <el-col :offset="22" :span="4" :sm="firstCol" class="details">
            <button class="ml-8 btn-copy-permalink-solid" @click="copyLink">
              <svg-icon name="icon-permalink" height="28" width="28" />
              <span class="visuallyhidden">Copy permalink</span>
            </button>
          </el-col>
        </el-row>
        <client-only placeholder="Loading scaffold ...">
          <div class="scaffoldvuer-container">
            <ScaffoldVuer
              ref="scaffoldvuer"
              :state="state"
              :display-markers="displayMarkers"
              :url="scaffoldUrl"
              :background-toggle="backgroundToggle"
              :region="region"
              :view-u-r-l="viewURL"
            />
          </div>
        </client-only>
      </detail-tabs>
    </div>
  </div>
</template>

<script>
// :scaffold-selected="scaffoldSelected"
import DetailTabs from '@/components/DetailTabs/DetailTabs.vue'
import { successMessage, failMessage } from '@/utils/notification-messages'

export default {
  name: 'ScaffoldViewerPage',

  components: {
    DetailTabs,
    ScaffoldVuer: process.client
      ? () => import('@abi-software/scaffoldvuer').then(m => m.ScaffoldVuer)
      : null
  },
  async fetch() {
    //Get id for retrieving state on the server,
    //Id is prioritized before viewURL and region.
    let uuid = this.$route.query.id
    if (uuid) {
      if (this.currentId != uuid) {
        this.currentId = uuid
        let url = this.api + 'scaffold/getstate'
        await fetch(url, {
          method: 'POST',
          headers: {
            'Content-type': 'application/json'
          },
          body: JSON.stringify({ uuid: uuid })
        })
          .then(response => response.json())
          .then(data => {
            this.state = data.state
          })
      }
    } else if (this.$route.query.viewURL) {
      this.viewURL = this.$route.query.viewURL
    } else if (this.$route.query.region) {
      this.region = this.$route.query.region
    }
  },
  data: () => {
    return {
      tabs: [
        {
          label: 'Scaffold Viewer',
          type: 'scaffold'
        }
      ],
      activeTab: 'scaffold',
      file: {},
      displayMarkers: false,
      backgroundToggle: true,
      state: undefined,
      region: '',
      viewURL: ''
    }
  },

  computed: {
    /**
     * Get the file name from the scaffold query parameter.
     * @returns String
     */
    fileName: function() {
      const scaffold = this.$route.query.scaffold
      let name =
        scaffold.substring(scaffold.lastIndexOf('/') + 1, scaffold.length) ||
        scaffold
      let nameWE = name.substring(0, name.lastIndexOf('.')) || name
      return nameWE
    },

    /**
     * Get the dataset id from the scaffold query parameter.
     * @returns Number
     */
    datasetId: function() {
      const scaffold = this.$route.query.scaffold
      const id = scaffold.substring(0, scaffold.indexOf('/')) || ''
      return id
    },
    /**
     * Get the version scaffold query parameter.
     * @returns Number
     */
    versionNumber: function() {
      const scaffold = this.$route.query.scaffold
      const postId =
        scaffold.substring(scaffold.indexOf('/') + 1, scaffold.length) || ''
      const version = postId.substring(0, postId.indexOf('/')) || ''
      return version
    },

    /**
     * Return the url for the scaffold metadata file.
     * @returns String
     */
    scaffoldUrl: function() {
      return `${process.env.portal_api}/s3-resource/${this.$route.query.scaffold}`
    }
  },
  watch: {
    '$route.query': '$fetch'
  },
  fetchOnServer: false,
  created: function() {
    this.currentId = undefined
    this.api = process.env.portal_api
    let lastChar = this.api.substr(-1)
    if (lastChar != '/') {
      this.api = this.api + '/'
    }
  },
  methods: {
    copyLink: function() {
      this.$message(successMessage('Share link is being generated.'))
      let url = this.api + `scaffold/getshareid`
      let state = this.$refs.scaffoldvuer.getState()
      // Dont need the url here
      if (state && state.url) delete state['url']
      fetch(url, {
        method: 'POST',
        headers: {
          'Content-type': 'application/json'
        },
        body: JSON.stringify({ state: state })
      })
        .then(response => response.json())
        .then(data => {
          if (data.uuid) {
            //Remove other scaffold queries
            delete this.$route.query['viewURL']
            delete this.$route.query['region']
            this.currentId = data.uuid
            //Update and copy the url
            this.$router.replace(
              { query: { ...this.$route.query, id: data.uuid } },
              //Callback once the router replace is done, essential
              //for copying the correct url.
              () => {
                this.$copyText(
                  `${process.env.ROOT_URL}${this.$route.fullPath}`
                ).then(
                  () => {
                    this.$message(
                      successMessage('Share link copied to clipboard.')
                    )
                  },
                  () => {
                    this.$message(failMessage('Failed to copy share link.'))
                  }
                )
              }
            )
          }
        })
        .catch(() => {
          this.$message(failMessage('Failed to get a share link.'))
        })
    }
  }
}
</script>

<style scoped lang="scss">
@import '@/assets/_variables.scss';

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

.btn-copy-permalink-solid {
  border-radius: 30px;
  background: #8300bf;
  color: white;
  cursor: pointer;
  padding: 0;
  border: none;
  transform: scale(0.9);
  svg {
    transform: scale(1.25);
  }
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
.btn-copy-permalink {
  border: none;
  background: none;
  color: $median;
  cursor: pointer;
  padding: 0;
  &:active {
    outline: none;
  }
}
.container ::v-deep {
  font-size: 0.875rem;
  h3 {
    font-size: 0.875rem;
    font-weight: 500;
    line-height: 1.5rem;
    text-transform: uppercase;
    margin-top: 16px;
  }
  img {
    height: auto;
    max-width: 100%;
  }
}
</style>
<style lang="scss">
.scaffoldvuer-container {
  height: 90vh;
  max-width: calc(100% - 48px);
  left: 24px;
  overflow: hidden;
  position: relative;
  @import '~@abi-software/scaffoldvuer/dist/scaffoldvuer';
}

.time-slider-container .el-tabs__content {
  height: 40px;
}

.time-slider-container .el-slider__marks-text {
  margin-top: 6px!important;
}

.time-slider-tooltip {
  padding: 6px 4px !important;
  font-family: "Asap", sans-serif;
  font-size: 12px !important;
  color: rgb(48, 49, 51) !important;
  background-color: #f3ecf6 !important;
  border: 1px solid #8300bf !important;
  white-space: nowrap !important;
  min-width: unset !important;
}

.scaffold_viewer_dropdown .el-select-dropdown__item {
  white-space: nowrap;
  text-align: left;
  font-family: "Asap", sans-serif;
}

</style>
