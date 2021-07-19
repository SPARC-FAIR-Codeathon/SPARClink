<template>
  <div class="dataset-metadata-info">
    <metadata-table :dataset-details="datasetDetails" />
  </div>
</template>

<script>
import MetadataTable from '@/components/MetadataTable/MetadataTable.vue'
export default {
  name: 'DatasetMetadataInfo',
  components: {
    MetadataTable
  },

  props: {
    datasetDetails: {
      type: Object,
      default: () => {}
    }
  }
}
</script>

<style lang="scss" scoped></style>
