<template>
  <div class="data-table">
    <div :class="tableClass" class="table">
      <el-table :data="tableData">
        <el-table-column fixed prop="date" label="Date" width="150" />
        <el-table-column prop="name" label="Name" width="120" />
        <el-table-column prop="state" label="State" width="120" />
        <el-table-column prop="city" label="City" width="120" />
        <el-table-column prop="address" label="Address" width="300" />
        <el-table-column prop="zip" label="Zip" width="120" />
        <el-table-column fixed="right" label="Operations" width="120">
          <template>
            <el-button type="text" size="small" @click="handleClick">
              Detail
            </el-button>
            <el-button type="text" size="small">
              Edit
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>
    <div class="pages">
      <pagination :total-count="totalCount" />
    </div>
  </div>
</template>

<script>
import Pagination from '../Pagination/Pagination.vue'

export default {
  name: 'DataTable',
  components: {
    Pagination
  },
  props: {
    tableClass: {
      type: String,
      default: ''
    },
    totalCount: {
      type: Number,
      default: 0
    }
  }
}
</script>

<style lang="scss">
.data-table {
  .table {
    padding: 0.5em;
    background: white;
  }
}
</style>
