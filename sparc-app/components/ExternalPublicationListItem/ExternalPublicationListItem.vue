<template>
  <div class="external-publication-list-item">
    <p v-if="citation" class="mb-0" v-html="$sanitize(citation, ['i', 'b'])" />
  </div>
</template>

<script>
export default {
  name: 'ExternalPublicationListItem',

  props: {
    publication: {
      type: Object,
      default: () => {
        return {
          doi: ''
        }
      }
    }
  },

  data() {
    return {
      citation: ''
    }
  },

  mounted() {
    this.getDoi()
  },

  methods: {
    /**
     * Get the DOI from doi.org
     */
    async getDoi() {
      this.citation = await this.$axios.$get(
        `https://doi.org/${this.publication.doi}`,
        {
          headers: {
            Accept: 'text/x-bibliography; style=apa; locale=en-US'
          }
        }
      )
    }
  }
}
</script>

<style lang="scss" scoped>
@import '../../assets/_variables.scss';
.external-publication-list-item {
  font-size: 0.875rem;
}
</style>
