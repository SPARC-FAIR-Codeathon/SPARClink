<template>
  <div class="pagination">
    <el-pagination
      :page-size="pageSize"
      :page-count="pageCount"
      layout="prev, pager, next"
      :total="totalCount"
      @current-change="selectPage"
    />
  </div>
</template>

<script>
export default {
  name: 'Pagination',
  props: {
    selected: {
      type: Number,
      default: 1
    },
    pageSize: {
      type: Number,
      default: 20
    },
    totalCount: {
      type: Number,
      default: 0
    }
  },
  computed: {
    pageCount: function() {
      return Math.ceil(this.totalCount / this.pageSize)
    }
  },
  methods: {
    /**
     * Emit select-page event
     */
    selectPage: function(page) {
      this.$emit('select-page', page)
    }
  }
}
</script>

<style lang="scss">
.pagination {
  padding-top: 1em;
  text-align: center;

  button.btn-prev {
    background: none;
  }

  button.btn-next {
    background: none;
  }

  li.more,
  li.number {
    background: none;
  }
}
</style>
