<template>
  <el-table
    :data="tableData"
    empty-text="No Results"
    @sort-change="onSortChange"
  >
    <el-table-column
      :fixed="true"
      sortable="custom"
      prop="fields.title"
      label="Title"
      :sort-orders="sortOrders"
      :width="titleColumnWidth"
    >
      <template slot-scope="scope">
        <nuxt-link
          :to="{
            name: 'projects-projectId',
            path: 'projects/:scope.row.sys.id',
            params: { projectId: scope.row.sys.id }
          }"
        >
          {{ scope.row.fields.title }}
        </nuxt-link>
      </template>
    </el-table-column>
    <el-table-column prop="fields.description" label="Description" width="648">
      <template slot-scope="scope">
        <p class="mobile-description">
          {{ getShortDescription(scope) }}
        </p>
      </template>
    </el-table-column>
    <el-table-column
      prop="fields.institution.fields.name"
      label="Lead Institution"
      width="200"
    >
      <template slot-scope="scope">
        <img
          class="img-project"
          :src="getImageSrc(scope)"
          :alt="getImageAlt(scope)"
        />
        {{ scope.row.fields.institution.fields.name }}
      </template>
    </el-table-column>
    <el-table-column
      sortable="custom"
      prop="fields.awardId"
      label="NIH Award"
      width="150"
    >
      <template slot-scope="scope">
        <a :href="getNihReporterUrl(scope)" target="_blank">
          {{ scope.row.fields.awardId }}
        </a>
      </template>
    </el-table-column>

    <el-table-column
      sortable="custom"
      prop="fields.principleInvestigator"
      label="Principal Investigator"
      width="250"
    />
  </el-table>
</template>

<script>
import Truncate from '@/mixins/truncate'
import { onSortChange } from '../../pages/data/utils'

export default {
  name: 'ProjectSearchResults',

  mixins: [Truncate],

  props: {
    tableData: {
      type: Array,
      default: () => []
    },
    titleColumnWidth: {
      type: Number,
      default: () => 300
    }
  },

  data() {
    return {
      sortOrders: ['ascending', 'descending']
    }
  },

  methods: {
    /**
     * Get image source
     * @param {Object} scope
     * @returns {String}
     */
    getImageSrc: function(scope) {
      return scope.row.fields.institution.fields.logo
        ? scope.row.fields.institution.fields.logo.fields.file.url
        : ''
    },
    /**
     * Get image source
     * @param {Object} scope
     * @returns {String}
     */
    getImageAlt: function(scope) {
      return scope.row.fields.institution.fields.logo
        ? scope.row.fields.institution.fields.logo.fields.file.description
        : `Logo for ${scope.row.fields.institution.fields.name}`
    },

    /**
     * Get NIH RePORT Url
     * @param {Object} scope
     * @returns {String}
     */
    getNihReporterUrl: function(scope) {
      return scope.row.fields.nihReporterUrl || '#'
    },

    /**
     * Get short description for dataset
     * @param {Object} scope
     * @returns {String}
     */
    getShortDescription: function(scope) {
      return scope.row.fields.shortDescription || ''
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
.img-project {
  height: auto;
  width: 100%;
}
.mobile-description {
  @media screen and (max-width: 48em) {
    margin-bottom: 0;
    font-size: 0.875em;
    -webkit-text-size-adjust: 100%;
  }
}
</style>
