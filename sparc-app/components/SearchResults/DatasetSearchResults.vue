<template>
  <el-table
    :data="tableData"
    :show-header="false"
    empty-text="No Results"
    @sort-change="onSortChange"
  >
    <el-table-column prop="banner" label="Image" width="160">
      <template slot-scope="scope">
        <nuxt-link
          :to="{
            name: 'datasets-datasetId',
            params: { datasetId: scope.row.id },
            query: {
              type: $route.query.type
            }
          }"
          class="img-dataset"
        >
          <img
            :src="scope.row.banner"
            :alt="`Banner for ${scope.row.name}`"
            height="128"
            width="128"
          />
          <sparc-pill v-if="scope.row.embargo">
            Embargoed
          </sparc-pill>
        </nuxt-link>
      </template>
    </el-table-column>
    <el-table-column
      min-width="400"
      sortable="custom"
      :sort-orders="sortOrders"
    >
      <template slot-scope="scope">
        <nuxt-link
          :to="{
            name: 'datasets-datasetId',
            params: { datasetId: scope.row.id },
            query: {
              type: $route.query.type
            }
          }"
        >
          {{ scope.row.name }}
        </nuxt-link>
        <div class="mt-8 mb-8">
          {{ scope.row.description }}
        </div>
        <table class="property-table">
          <tr
            v-for="(property, index) in PROPERTY_DATA"
            v-show="
              property.propPath === 'createdAt' ||
                getPropertyValue(tableMetadata.get(scope.row.doi), property)
            "
            :key="index"
          >
            <td class="property-name-column">
              {{ property.displayName }}
            </td>
            <td>
              {{
                property.propPath === 'createdAt'
                  ? formatDate(scope.row.createdAt) +
                    ' (Last updated ' +
                    formatDate(scope.row.updatedAt) +
                    ')'
                  : getPropertyValue(tableMetadata.get(scope.row.doi), property)
              }}
            </td>
          </tr>
        </table>
      </template>
    </el-table-column>
  </el-table>
</template>

<script>
import SparcPill from '@/components/SparcPill/SparcPill.vue'
import FormatDate from '@/mixins/format-date'
import StorageMetrics from '@/mixins/bf-storage-metrics'
import { onSortChange } from '@/pages/data/utils'
import { pathOr } from 'ramda'
import _ from 'lodash'

export default {
  name: 'DatasetSearchResults',

  components: { SparcPill },

  mixins: [FormatDate, StorageMetrics],

  props: {
    tableData: {
      type: Array,
      default: () => []
    },
    tableMetadata: {
      type: Map,
      default: () => new Map()
    }
  },

  data() {
    return {
      sortOrders: ['ascending', 'descending'],
      PROPERTY_DATA: [
        {
          displayName: 'Anatomical Structure',
          propPath: 'anatomy.organ'
        },
        {
          displayName: 'Species',
          propPath: 'organisms.primary[0].species.name'
        },
        {
          displayName: 'Techniques',
          propPath: 'item.techniques'
        },
        {
          displayName: 'Samples',
          propPath: 'item.statistics'
        },
        {
          displayName: 'Publication Date',
          propPath: 'createdAt'
        },
        {
          displayName: 'Includes',
          propPath: 'publication'
        }
      ]
    }
  },

  computed: {
    /**
     * Compute if the search results are for simulations
     * @returns {Boolean}
     */
    areSimulationResults: function() {
      const searchType = pathOr('', ['query', 'type'], this.$route)
      return searchType === 'simulation'
    }
  },

  methods: {
    getPropertyValue: function(item, property) {
      if (item == undefined) {
        return undefined
      }
      switch (property.displayName) {
        case 'Anatomical Structure': {
          const organs = _.get(item, property.propPath)
          return organs
            ? organs.map(item => _.upperFirst(item.name)).join(', ')
            : undefined
        }
        case 'Includes': {
          return _.get(item, property.propPath) ? undefined : 'Publications'
        }
        case 'Samples': {
          const sampleCount = _.get(item, property.propPath + '.samples.count')
          const subjectCount = _.get(
            item,
            property.propPath + '.subjects.count'
          )
          return sampleCount && subjectCount
            ? `${sampleCount} samples from ${subjectCount} subjects`
            : undefined
        }
        case 'Techniques': {
          const techniques = _.get(item, property.propPath)
          return techniques
            ? techniques
                .map(item => _.upperFirst(item.keyword))
                .join(', ')
                .replaceAll(' technique', '')
            : undefined
        }
        default: {
          return _.get(item, property.propPath)
        }
      }
    },

    onSortChange: function(payload) {
      onSortChange(this, payload)
    }
  }
}
</script>

<style lang="scss" scoped>
.el-table {
  width: 100%;
}

.el-table--enable-row-hover .el-table__body tr {
  background-color: transparent;
}

.img-dataset {
  display: block;
  position: relative;
  .sparc-pill {
    font-size: 0.75rem;
    position: absolute;
    right: 0.25rem;
    top: 0.5rem;
  }
  img {
    display: block;
  }
}
.property-table {
  td {
    background-color: transparent;
    padding: 0.25rem 0 0 0;
    border: none;
  }
  background-color: transparent;
  border: none;
  padding: 0;
}
// The outermost bottom border of the table. Element UI adds psuedo elements to create the bottom table border that we must hide to remove
table:not([class^='el-table__'])::before {
  display: none;
}
.property-name-column {
  width: 160px;
  font-weight: bold;
}
</style>
