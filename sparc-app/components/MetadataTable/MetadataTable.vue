<template>
  <div class="metadata-table">
    <div class="metadata-table-dropdown">
      <el-select v-model="value" @change="getMetadataRecords">
        <el-option
          v-for="(model, index) in models"
          :key="`${model}-${index}`"
          :label="model.modelName"
          :value="model.modelName"
        />
      </el-select>
    </div>
    <div class="metadata-table-content">
      <div v-if="hasError" class="error-wrap">
        <p>Sorry, an error has occurred</p>
        <el-button type="primary" @click="getMetadataRecords">
          Try again
        </el-button>
      </div>
      <el-table
        v-else
        v-loading="isLoading"
        :data="properties"
        :default-sort="{ prop: 'name', order: 'ascending' }"
      >
        <el-table-column
          v-for="heading in headings"
          :key="heading"
          :prop="heading"
          :label="heading"
          min-width="300"
        />
      </el-table>
    </div>
    <div class="metadata-table-pagination">
      <pagination
        :selected="page"
        :page-size="limit"
        :total-count="totalCount"
        @select-page="selectPage"
      />
    </div>
  </div>
</template>

<script>
import { propOr, head } from 'ramda'
import Pagination from '../Pagination/Pagination.vue'
export default {
  name: 'MetadataTable',
  components: {
    Pagination
  },
  props: {
    datasetDetails: {
      type: Object,
      default: () => {}
    }
  },
  data() {
    return {
      isLoading: true,
      models: [],
      records: [],
      properties: [],
      headings: [],
      defaultModel: '',
      dropdownSelection: false,
      limit: 10,
      offset: 0,
      totalCount: 0,
      page: 1,
      value: '',
      hasError: false
    }
  },

  computed: {
    /**
     * Url to get records for model
     * @returns {String}
     */
    getRecordsUrl: function() {
      if (!this.dropdownSelection) {
        this.defaultModel = propOr('', 'modelName', head(this.models))
        this.value = this.defaultModel
      }
      const datasetId = propOr('', 'id', this.datasetDetails)
      return `${process.env.bf_api_host}/discover/search/records?datasetId=${datasetId}&model=${this.defaultModel}`
    }
  },

  watch: {
    /**
     * Watches getRecordsUrl before making endpoint call
     */
    getRecordsUrl: {
      handler: function(val) {
        if (val) {
          this.getMetadataRecords()
        }
      },
      immediate: true
    },
    /**
     * Watches datasetDetails object before assigning models array
     */
    datasetDetails: {
      handler: function(val) {
        if (val) {
          this.models = propOr([], 'modelCount', this.datasetDetails)
        }
      },
      immediate: true
    }
  },

  methods: {
    /**
     * Gets the metadata records for a dataset
     * @param {String} model
     */
    getMetadataRecords: function(model = '') {
      if (model !== '') {
        this.dropdownSelection = true
        this.defaultModel = model
      }
      this.offset = (this.page - 1) * this.limit
      this.$axios
        .$get(`${this.getRecordsUrl}&limit=${this.limit}&offset=${this.offset}`)
        .then(response => {
          this.isLoading = false
          this.headings = []
          this.properties = []
          this.totalCount = response.totalCount
          this.records = propOr([], 'records', response)
          const properties = propOr({}, 'properties', head(this.records))
          // just to get the property names for the table since they're all
          // the same across records
          for (let key in properties) {
            this.headings.push(key)
          }

          // now to get the properties
          this.records.forEach(record => {
            const properties = propOr({}, 'properties', record)
            this.properties.push(properties)
          })
        })
        .catch(
          // handle error
          (this.errorLoading = true)
        )
    },

    /**
     * Selects a page for pagination
     */
    selectPage: function(index) {
      this.page = index
      this.getMetadataRecords()
    }
  }
}
</script>

<style lang="scss" scoped>
.metadata-table-content {
  background: #fff;
  padding: 16px;
  margin-top: 20px;
  margin-bottom: 10px;
}

.metadata-table-dropdown {
  margin-top: 8px;
  margin-bottom: 5px;
}

.metadata-table-pagination {
  margin-bottom: 10px;
}
</style>
