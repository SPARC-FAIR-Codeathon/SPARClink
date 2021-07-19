<template>
  <el-dialog
    :visible="visible"
    :show-close="false"
    class="version-history-dialog"
    width="772px"
    height="600px"
    @close="closeDialog"
  >
    <bf-dialog-header slot="title" title="Version History" />

    <div class="version-history-container">
      <el-row class="table-header" type="flex" justify="center">
        <el-col :span="6">
          Version
        </el-col>
        <el-col :span="6">
          Date Published
        </el-col>
        <el-col :span="10" :push="2">
          DOI
        </el-col>
      </el-row>
      <el-row
        v-for="version in versions"
        :key="version.doi"
        class="table-rows"
        type="flex"
        justify="center"
      >
        <el-col :span="6">
          <router-link
            :to="{
              name: 'version',
              params: {
                version: version.version,
                datasetId
              },
              query: {
                type: 'dataset'
              }
            }"
            @click.native="$emit('update:visible', false)"
          >
            Version {{ version.version }}
          </router-link>
        </el-col>
        <el-col :span="6">
          {{ formatDate(version.createdAt) }}
        </el-col>
        <el-col :span="10" :push="2">
          {{ version.doi }}
        </el-col>
      </el-row>
    </div>
  </el-dialog>
</template>

<script>
import BfDialogHeader from '@/components/bf-dialog-header/BfDialogHeader.vue'

import FormatDate from '@/mixins/format-date'

export default {
  name: 'VersionHistory',

  components: {
    BfDialogHeader
  },

  mixins: [FormatDate],

  props: {
    visible: {
      type: Boolean,
      default: false
    },

    datasetId: {
      type: Number,
      default: 0
    },

    latestVersion: {
      type: Number,
      default: 0
    },

    versions: {
      type: Array,
      default: () => []
    }
  },

  methods: {
    /**
     * Closes the dialog
     */
    closeDialog() {
      this.$emit('close-version-dialog')
      // scroll version history list to top
      const scrollEl = this.$el.querySelector('.el-dialog__body')
      scrollEl.scrollTop = 0
    }
  }
}
</script>

<style lang="scss" scoped>
.version-history-dialog {
  .version-history-container {
    height: 290px;
    font-size: 0.875rem;
    line-height: 1rem;

    .table-header {
      background-color: #f9f9f9;
      color: #404554;
      font-weight: 600;
      padding: 0.75rem 1.5rem;
      margin-left: 0px !important;
    }

    .table-rows {
      color: #000000;
      padding: 0.75rem 1.5rem;
      border-top: solid 1px #dadada;
      margin-left: 0px !important;

      a {
        text-decoration: underline;

        &:focus {
          color: #1c46bd;
        }
      }
    }
  }

  ::v-deep .el-dialog {
    width: 616px !important;
    height: 350px;
    .el-dialog__header {
      background-color: #f1f1f3;
      padding-top: 1rem;
      border-radius: 0.25rem 0.25rem 0px 0px;
      padding-bottom: 0.5rem;

      .bf-dialog-header {
        .bf-dialog-header-title {
          font-size: 0.875rem;
          font-weight: bold;
          line-height: 1rem;
        }

        .icon-close {
          margin-bottom: 0.3125rem;
          .svg-icon {
            width: 1rem !important;
            height: 1rem !important;
          }
        }
      }
    }
    .el-dialog__body {
      padding: 0;
      overflow: scroll;
    }
  }
}
</style>
