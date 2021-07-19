<template>
  <div class="dataset-files-info">
    <p class="dataset-link">
      <nuxt-link
        :to="{
          name: 'help-helpId',
          params: {
            helpId: ctfDatasetNavigationInfoPageId
          }
        }"
        class="dataset-link"
      >
        Learn more about navigating a SPARC dataset
      </nuxt-link>
    </p>
    <files-table :dataset-details="datasetDetails" :osparc-viewers="osparcViewers" />
  </div>
</template>

<script>
import FilesTable from '@/components/FilesTable/FilesTable.vue'
export default {
  name: 'DatasetFilesInfo',

  components: {
    FilesTable
  },

  props: {
    datasetDetails: {
      type: Object,
      default: () => {}
    },
    osparcViewers: {
      type: Object,
      default: () => {}
    }
  },

  data() {
    return {
      ctfDatasetNavigationInfoPageId:
        process.env.ctf_dataset_navigation_info_page_id
    }
  }
}
</script>
