<template>
  <el-table :data="tableData" empty-text="No Results">
    <el-table-column :fixed="true" prop="image_id" label="ID">
      <template slot-scope="scope">
        <nuxt-link
          :to="{
            name: 'datasets-viewer-id',
            params: {
              id: scope.row.image_id
            },
            query: {
              viewer: viewerId(scope.row.share_link)
            }
          }"
        >
          {{ scope.row.image_id }}
        </nuxt-link>
      </template>
    </el-table-column>
  </el-table>
</template>

<script>
export default {
  name: 'ImagesTable',

  props: {
    tableData: {
      type: Array,
      default: () => []
    }
  },

  methods: {
    /**
     * Get the viewer ID from the share link
     * @param {String} shareLink
     * @returns {String}
     */
    viewerId: function(shareLink) {
      const linkParts = shareLink.split(process.env.BL_SHARE_LINK_PREFIX)

      return linkParts[1]
    }
  }
}
</script>

<style lang="scss" scoped>
.el-table {
  width: 100%;
}
.img-image {
  height: auto;
  width: 100%;
}
</style>
