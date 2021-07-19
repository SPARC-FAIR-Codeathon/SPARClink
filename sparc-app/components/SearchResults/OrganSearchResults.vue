<template>
  <el-table :data="tableData" empty-text="No Results" @sort-change="onSortChange">
    <el-table-column
      :fixed="true"
      sortable="custom"
      prop="fields.name"
      label="Title"
      :width="titleColumnWidth"
    >
      <template slot-scope="scope">
        <nuxt-link
          :to="{
            name: 'organs-organId',
            params: { organId: scope.row.sys.id }
          }"
        >
          {{ scope.row.fields.name }}
        </nuxt-link>
      </template>
    </el-table-column>
    <el-table-column :fixed="true" prop="fields.title" label="Banner">
      <template slot-scope="scope">
        <nuxt-link
          :to="{
            name: 'organs-organId',
            params: { organId: scope.row.sys.id }
          }"
        >
          <img
            :src="getImageSrc(scope)"
            :alt="getImageAlt(scope)"
            height="128"
            width="128"
          />
        </nuxt-link>
      </template>
    </el-table-column>
  </el-table>
</template>

<script>
import { pathOr } from 'ramda'
import { onSortChange } from '../../pages/data/utils'

export default {
  name: 'OrganSearchResults',

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

  methods: {
    /**
     * Get image source
     * @param {Object} scope
     * @returns {String}
     */
    getImageSrc: function(scope) {
      return pathOr(
        '',
        ['row', 'fields', 'bannerImage', 'fields', 'file', 'url'],
        scope
      )
    },
    /**
     * Get image source
     * @param {Object} scope
     * @returns {String}
     */
    getImageAlt: function(scope) {
      return pathOr(
        '',
        ['row', 'fields', 'bannerImage', 'fields', 'file', 'description'],
        scope
      )
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
</style>
