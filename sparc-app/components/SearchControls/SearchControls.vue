<template>
  <div class="controls">
    <div class="control control-search-type">
      <el-select
        v-model="selectedType"
        size="large"
        style="width: 100%; height: 100%; margin: 0; padding: 0; border-radius: 0"
        placeholder="Select"
      >
        <el-option
          v-for="type in types"
          :key="type.key"
          :value="type.key"
          :label="type.label"
        />
      </el-select>
    </div>
    <div v-if="isSearchVisible" class="control control-search-input">
      <el-input
        v-model="terms"
        placeholder="Search..."
        suffix-icon="el-icon-search"
        @keyup.native.enter="submit"
      />
    </div>
    <div v-if="isSearchVisible" class="search-button">
      <el-button
        type="primary"
        class="view-search-results"
        @click.native="submit"
      >
        {{ submitText }}
      </el-button>
      <el-button
        v-if="isClearSearchVisible"
        class="btn-clear-search"
        @click.native="clearSearch"
      >
        Clear search
      </el-button>
    </div>
  </div>
</template>

<script>
import { pathOr } from 'ramda'

export default {
  props: {
    searchOnLoad: {
      type: Boolean,
      default: false
    },
    submitText: {
      type: String,
      default: 'View Results'
    },
    isClearSearchVisible: {
      type: Boolean,
      default: false
    },
    isSearchVisible: {
      type: Boolean,
      default: true
    }
  },

  data() {
    return {
      selectedType: 'datasets',
      loading: false,
      terms: null,
      types: [
        {
          label: 'SPARC Datasets',
          key: 'datasets'
        },
        {
          label: 'Simulation Models',
          key: 'sim_models'
        },
        {
          label: 'SPARC Protocols',
          key: 'protocols'
        },
        {
          label: 'Files',
          key: 'files'
        }
      ]
    }
  },
  watch: {
    selectedType: function(value) {
      if (value === 'embargo') {
        this.isSearchVisible = false
        this.submit()
      } else {
        this.isSearchVisible = true
        this.submit()
      }
    }
  },

  mounted: function() {
    if (this.searchOnLoad) {
      this.setSearchOnLoad()
    }
  },

  methods: {
    /**
     * Clear search
     */
    clearSearch: function() {
      this.terms = ''
      this.submit()
    },

    /**
     * Set search and execute search
     */
    setSearchOnLoad: function() {
      const terms = pathOr('', ['query', 'searchTerms'], this.$route)
      const type = pathOr('datasets', ['query', 'searchType'], this.$route)
      this.selectedType = type
      this.terms = terms
      this.submit()
    },

    submit() {
      this.$emit('query', this.selectedType, this.terms)
    }
  }
}
</script>

<style lang="scss" scoped>
.controls {
  align-items: center;
  display: flex;
}

.control {
  display: inline-block;
}

.search-control {
  border: 0;
  -webkit-appearance: none;
  width: 100%;
  height: 100%;
}

.control-search-type {
  margin-right: 8px;
  width: 180px;
}
.control-search-input {
  flex: 1;
  margin-right: 16px;
}

.search-button {
  .view-search-results {
    background: #24245b;
    border: 0;
    height: 40px;
  }
}

.btn-clear-search {
  background: none;
  border: none;
  color: #8300bf;
  padding: 0;
}
</style>
