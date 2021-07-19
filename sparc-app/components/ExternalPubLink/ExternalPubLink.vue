<template>
  <div class="external-publication-list-item">
    <a
      class="dataset-about-info__container--doi-link mb-16"
      :href="linkFromDoi(publication.doi)"
      target="_blank"
    >
      {{ title }}
    </a>
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
      title: ''
    }
  },

  created() {
    this.getTitle()
  },

  methods: {
    /**
     * Get the Title from doi.org
     */
    getTitle() {
      fetch(this.linkFromDoi(this.publication.doi), {
        method: 'GET',
        headers: { Accept: 'application/json'}
      })
        .then(response => response.json())
        .then(json => {
          this.title = json.title
          this.loading = false
        })
    },

    linkFromDoi(doi){
      return `https://doi.org/${doi}`
    }
  }
}
</script>
