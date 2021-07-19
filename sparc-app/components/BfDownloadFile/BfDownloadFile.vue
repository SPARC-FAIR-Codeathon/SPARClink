<template>
  <div>
    <el-button @click="onDownloadClick">
      Download
    </el-button>
    <form id="zipForm" ref="zipForm" method="POST" :action="zipitUrl">
      <input v-model="zipData" type="hidden" name="data" />
    </form>
    <el-dialog
      :visible.sync="confirmDownloadVisible"
      :show-close="false"
      @close="closeConfirmDownload"
    >
      <div slot="title" class="bf-dialog-header">
        <span class="bf-dialog-header-title">Confirm Download</span>
        <button class="icon-close btn" @click="closeConfirmDownload">
          <svg-icon icon="icon-remove" height="12" width="12" />
        </button>
      </div>

      <div class="bf-dialog-body">
        <div v-if="showReduceSize" class="mb-24">
          <p>
            The file(s) you are trying to download exceed the limit of
            {{ maxDownloadSize }}. Please reduce the number of files selected
            and try again.
          </p>
          <el-table :show-header="false" :border="false" :data="selected">
            <el-table-column prop="name" />
            <el-table-column align="right">
              <template slot-scope="scope">
                {{ formatMetric(scope.row.size) }}
                <button class="btn btn-remove">
                  <svg-icon
                    color="#bdbdbd #404554"
                    icon="icon-remove"
                    height="12"
                    width="12"
                    @click="$emit('remove-selection', scope.row)"
                  />
                </button>
              </template>
            </el-table-column>
          </el-table>
        </div>
        <div v-if="selected.length > 1" class="download-name">
          <label for="downloadName">
            File Name
          </label>
          <el-input id="downloadName" v-model="archiveName" />
          <span>.zip</span>
        </div>
      </div>

      <div slot="footer" class="dialog-footer">
        <el-button class="secondary" @click="closeConfirmDownload">
          Cancel
        </el-button>
        <el-button :disabled="downloadDisabled" @click="confirmDownload">
          Download
        </el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import StorageMetrics from '@/mixins/bf-storage-metrics'

const DEFAULT_ARCHIVE_NAME = 'sparc-portal-data'

export default {
  name: 'BfDownloadFile',

  mixins: [StorageMetrics],

  props: {
    selected: {
      type: Array,
      default: () => {
        return []
      }
    },
    dataset: {
      type: Object,
      default: () => {
        return {}
      }
    }
  },

  data() {
    return {
      zipData: '',
      confirmDownloadVisible: false,
      archiveName: DEFAULT_ARCHIVE_NAME,
      showReduceSize: false,
      downloadConfirmed: false
    }
  },

  computed: {
    /**
     * Compute URL for zipit service
     * @returns {String}
     */
    zipitUrl: function() {
      return process.env.zipit_api_host
    },

    /**
     * download is disabled if the total size is greater than the threshold, or no rows are selected
     * @returns {Boolean}
     */
    downloadDisabled() {
      if (this.selected.length === 0) return true
      const totalSize = this.selected.reduce(
        (total, node) => total + node.size || 0,
        0
      )

      return totalSize > process.env.max_download_size
    },

    /**
     * determines whether the confirm download dialog should open
     * @returns {Boolean}
     */
    shouldConfirmDownload() {
      return (
        this.downloadDisabled ||
        (this.selected.length > 1 && !this.downloadConfirmed)
      )
    },

    /**
     * Compute max size for download
     * @returns {Number}
     */
    maxDownloadSize() {
      return this.formatMetric(process.env.max_download_size)
    }
  },

  methods: {
    /**
     * Show the confirm dialog if downloading multiple files
     * Otherwise, just download the file
     */
    onDownloadClick() {
      if (this.shouldConfirmDownload) {
        this.showReduceSize = this.downloadDisabled
        this.confirmDownloadVisible = true
      } else {
        this.executeDownload()
      }
    },

    /**
     * Confirm to start the download, or show the
     */
    confirmDownload() {
      this.downloadConfirmed = true
      this.onDownloadClick()
    },

    executeDownload() {
      const mainPayload = {
        paths: this.selected.map(f => f.path),
        datasetId: this.dataset.id,
        version: this.dataset.version
      }

      const archiveNamePayload =
        this.archiveName && this.selected.length > 1
          ? { archiveName: this.archiveName }
          : {}

      const payload = {
        ...mainPayload,
        ...archiveNamePayload
      }

      this.zipData = JSON.stringify(payload, undefined)
      this.$nextTick(() => {
        this.$refs.zipForm.submit() // eslint-disable-line no-undef
      })
      this.closeConfirmDownload()
    },

    closeConfirmDownload() {
      this.archiveName = DEFAULT_ARCHIVE_NAME
      this.downloadConfirmed = false
      this.showReduceSize = false
      this.confirmDownloadVisible = false
    }
  }
}
</script>

<style lang="scss" scoped>
.btn {
  background: none;
  border: none;
  color: #000;
  cursor: pointer;
  &:active {
    outline: none;
  }
}
.btn-remove {
  box-sizing: border-box;
  height: 1rem;
  width: 1rem;
}
.bf-dialog-header {
  align-items: center;
  display: flex;
  position: relative;
}
.bf-dialog-header-title {
  flex: 1;
  font-size: 18px;
  font-weight: 400;
  line-height: 1;
  margin-right: 8px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  color: #000;
}

.bf-dialog-body {
  word-break: normal;
}

.download-name {
  display: flex;
  align-items: center;
  label {
    min-width: 64px;
  }
  ::v-deep .el-input {
    margin: 0 8px;
  }
}
</style>
