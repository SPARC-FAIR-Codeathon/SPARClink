<template>
  <el-dropdown
    trigger="click"
    placement="bottom-start"
    @command="$emit('update-page-size', $event)"
    @visible-change="isMenuOpen = $event"
  >
    <button class="filter-dropdown el-dropdown-link">
      <span class="el-dropdown-text-link">
        {{ pageSize }}
      </span>
      <svg-icon
        class="ml-8 icon-arrow"
        name="icon-arrow"
        :dir="menuArrowDir"
        height="10"
        width="10"
      />
    </button>
    <el-dropdown-menu slot="dropdown" class="bf-menu">
      <el-dropdown-item
        v-for="option in pageSizeOptions"
        :key="option"
        class="icon-item"
        :command="option"
      >
        {{ option }}
        <svg-icon
          v-if="pageSize === option"
          icon="icon-check"
          class="item-icon-check"
          width="20"
          height="20"
        />
      </el-dropdown-item>
    </el-dropdown-menu>
  </el-dropdown>
</template>

<script>
export default {
  name: 'PaginationMenu',

  props: {
    paginationItemLabel: {
      type: String,
      default: 'Items'
    },
    pageSize: {
      type: Number,
      default: 10
    },
    pageSizeOptions: {
      type: Array,
      default: () => {
        return [10, 20, 50, 'View All']
      }
    }
  },

  data: function() {
    return {
      isMenuOpen: false
    }
  },

  computed: {
    /**
     * Compute dataset filter arrow direction
     * @returns {String}
     */
    menuArrowDir: function() {
      return this.isMenuOpen ? 'up' : 'down'
    }
  }
}
</script>

<style lang="scss" scoped>
@import '../../assets/_variables.scss';

.filter-dropdown {
  display: flex;
  align-items: center;
  border-radius: 4px;
  border: solid 1px $medium-gray;
  background-color: transparent;
  font-size: 14px;
  font-weight: bold;
  color: $median;
  margin-left: 5px;
}

.icon-arrow {
  color: $medium-gray;
  height: 5px;
  width: 8px;
}

.el-dropdown-link {
  cursor: pointer;
  outline: none;
}

.el-dropdown-text-link {
  margin-right: -6px;
  padding-top: 3px;
  padding-bottom: 3px;
}
</style>
