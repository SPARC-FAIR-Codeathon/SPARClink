<template>
  <div id="container" class="mb-16">
    <el-row :gutter="20">
      <el-col :span="8">
        <img class="banner-image" :src="dataset.banner" :alt="'image could not load'" />
      </el-col>
      <el-col :span="16">
        <nuxt-link
          class="dataset-name"
          :to="{
            name: 'datasets-datasetId',
            params: {
              datasetId: id
            }
          }"
        >
          {{ dataset.name }}
        </nuxt-link>
        <div class="dataset-description mt-8">
          {{ dataset.description }}
        </div>
      </el-col>
    </el-row>
  </div>
</template>

<script>
export default {
  name: 'DatasetCard',
  props: {
    id: {
      type: Number,
      default: 0
    }
  },
  watch: {
    id: function (val) {
      this.getDiscoverData(val)
    }
  },
  methods: {
    getDiscoverData: function (id) {
       this.$axios
        .$get(`${process.env.discover_api_host}/datasets/${id}`)
        .then(response => {
          this.dataset = response
        })
        .catch(() => {
          this.hasError = true
        })
        .finally(() => {
          this.isLoading = false
        })
    }
  },
  data: function() {
    return {
      dataset: {},
      hasError: false,
      isLoading: true
    }
  },
  mounted: function(){
    this.getDiscoverData(this.id)
  }
}
</script>

<style lang="scss" scoped>

.banner-image {
  display: block;
  width: 100%;
  max-height: 200px;
}

.dataset-name {
  font-size: 14px;
  line-height: 20px;
  font-weight: 600;
  text-decoration: underline;
}

.dataset-description {
  font-size: 14px;
  line-height: 20px;
  word-wrap: break-word;
}
</style>
