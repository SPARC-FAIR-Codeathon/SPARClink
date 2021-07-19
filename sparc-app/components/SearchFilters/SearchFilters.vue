<template>
  <el-dialog
    :visible="visible"
    :show-close="false"
    @open="onOpen"
    @close="closeDialog"
  >
    <bf-dialog-header slot="title" :title="dialogTitle" />

    <dialog-body>
      <template v-for="filter in filters">
        <div :key="filter.category">
          <h3>
            {{ filter.category }}
          </h3>
          <div class="filter__checkbox__wrap">
            <el-checkbox
              v-for="item in filter.filters"
              :key="`${item.category}_${item.key}`"
              v-model="item.value"
            >
              {{ item.label }}
            </el-checkbox>
          </div>
        </div>
      </template>
    </dialog-body>

    <div slot="footer" class="dialog-footer">
      <bf-button class="ghost" @click="clearAllFilters">
        Clear All
      </bf-button>
      <bf-button @click="applyFilters">
        Apply
      </bf-button>
    </div>
  </el-dialog>
</template>

<script>
import { clone } from 'ramda'
import BfDialogHeader from '@/components/bf-dialog-header/BfDialogHeader.vue'
import DialogBody from '@/components/dialog-body/DialogBody.vue'
import BfButton from '@/components/shared/BfButton/BfButton.vue'

export default {
  name: 'SearchFilters',

  components: { BfButton, BfDialogHeader, DialogBody },

  props: {
    value: {
      type: Array,
      default: () => [
        {
          category: '',
          items: [
            {
              label: '',
              value: null
            }
          ]
        }
      ]
    },
    visible: {
      type: Boolean,
      default: false
    },
    isLoading: {
      type: Boolean,
      default: false
    },
    dialogTitle: {
      type: String,
      default: ''
    }
  },

  data() {
    return {
      filters: []
    }
  },

  methods: {
    /**
     * Callback for opening filter
     * Copy the filters passed down to the component
     * to make a local copy for local CRUD
     */
    onOpen: function() {
      this.filters = clone(this.value)
    },

    /**
     * Closes the dialog
     */
    closeDialog: function() {
      this.$emit('update:visible', false)
    },

    /**
     * Apply filters
     */
    applyFilters: function() {
      this.$emit('input', this.filters)
      this.closeDialog()
    },

    /**
     * Clear all filters
     */
    clearAllFilters: function() {
      const resetFilters = this.filters.map(filter => {
        filter.filters.map(item => {
          return (item.value = false)
        })

        return filter
      })

      this.$emit('input', resetFilters)

      this.closeDialog()
    }
  }
}
</script>

<style lang="scss" scoped>
::v-deep {
  .dialog-body,
  .el-dialog__body {
    font-size: inherit;
  }
  .el-dialog__body {
    overflow: hidden;
    overflow-y: auto;
    max-height: 400px;
  }
}
h2 {
  font-size: 0.875em;
  font-weight: 500;
  margin-bottom: 1em;
}
h3 {
  color: #000;
  font-size: 0.75em;
  font-weight: 500;
  line-height: 1;
  margin-bottom: 0.8125em;
}
.filter__checkbox__wrap {
  display: block;
  padding-left: 1em;
}
.el-checkbox {
  display: flex;
  margin-bottom: 1em;
}
::v-deep .el-checkbox__label {
  font-size: 0.75rem;
  font-weight: 400;
  white-space: normal;
}
.active__filters-wrap {
  margin-bottom: 1em;
}
.active__filters,
.active__filters__category {
  display: inline;
}
.active__filters .el-tag {
  margin: 0.5em 1em 0.5em 0;
}
::v-deep .el-dialog {
  @media (max-width: 48em) {
    width: calc(100vw - 2em);
  }
}
</style>
