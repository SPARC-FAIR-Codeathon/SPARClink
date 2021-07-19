<template>
  <el-table :data="tableData" empty-text="No Results">
    <el-table-column
      :fixed="true"
      prop="fields.title"
      label="Title"
      width="300"
    >
      <template slot-scope="scope">
        <nuxt-link
          :to="{
            name: 'events-eventId',
            params: { eventId: scope.row.sys.id }
          }"
        >
          {{ scope.row.fields.title }}
        </nuxt-link>
      </template>
    </el-table-column>
    <el-table-column prop="fields.eventType" label="Event Type" />
    <el-table-column prop="fields.location" label="Location" />
  </el-table>
</template>

<script>
export default {
  name: 'EventSearchResults',

  props: {
    tableData: {
      type: Array,
      default: () => []
    }
  }
}
</script>

<style lang="scss" scoped>
.el-table {
  width: 100%;
}
</style>
