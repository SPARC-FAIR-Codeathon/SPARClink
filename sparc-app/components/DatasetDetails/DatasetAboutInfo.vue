<template>
  <div class="dataset-about-info">
    <div class="dataset-about-info__container">
      <h3>Last Updated</h3>
      <p>{{ updatedDate }}</p>
      <h3>Corresponding Author</h3>
      <p>
        {{ datasetOwnerName }}<br />
        {{ datasetOwnerEmail }}
      </p>
      <h3>Dataset DOI</h3>
      <p>
        <a
          class="dataset-about-info__container--doi-link mb-16"
          :href="doi"
          target="_blank"
        >
          {{ doi }}
        </a>
      </p>
      <h3>NIH Award</h3>
      <p>{{ getSparcAwardNumber }}</p>
      <template v-if="primaryPublication">
        <h3> Primary Publication</h3>
        <external-pub-link :publication="primaryPublication" />
      </template>
      <p />
      <h3>Tags</h3>
      <div v-if="datasetTags.length !== 0">
        <tag-list :tags="datasetTags" />
      </div>
      <div v-else>
        <p>N/A</p>
      </div>

      <div v-if="externalPublications.length" class="row mt-24">
        <div class="col-xs-12">
          <h3>References</h3>
          <external-publication-list-item
            v-for="publication in externalPublications"
            :key="publication.doi"
            class="mb-16"
            :publication="publication"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { compose, propOr, head } from 'ramda'

import ExternalPublicationListItem from '@/components/ExternalPublicationListItem/ExternalPublicationListItem.vue'
import ExternalPubLink from '@/components/ExternalPubLink/ExternalPubLink'
import TagList from '@/components/TagList/TagList.vue'

export default {
  name: 'DatasetAboutInfo',

  components: {
    ExternalPublicationListItem,
    ExternalPubLink,
    TagList
  },
  props: {
    updatedDate: {
      type: String,
      default: ''
    },

    doi: {
      type: String,
      default: ''
    },

    datasetTags: {
      type: Array,
      default: () => []
    },

    datasetOwnerName: {
      type: String,
      default: ''
    },

    datasetOwnerEmail: {
      type: String,
      default: ''
    },

    externalPublications: {
      type: Array,
      default: () => []
    }
  },

  data() {
    return {
      sparcAwardNumber: ''
    }
  },

  computed: {
    /**
     * Gets the sparc award number
     * @return {String}
     */
    getSparcAwardNumber: function() {
      return this.sparcAwardNumber !== '' ? this.sparcAwardNumber : 'N/A'
    },

    /**
     * Url to get records for model
     * @returns {String}
     */
    getRecordsUrl: function() {
      return `${process.env.discover_api_host}/search/records?datasetId=${this.$route.params.datasetId}`
    },
    primaryPublication: function() {
	      const valObj = this.externalPublications.filter(function(elem) {
	        return elem.relationshipType == 'IsDescribedBy'
	      })
	      return valObj.length > 0 ? valObj[0] : null
	    }
  },

  watch: {
    getRecordsUrl: {
      handler: function(val) {
        if (val) {
          this.getDatasetRecords()
        }
      },
      immediate: true
    }
  },

  methods: {
    /**
     * Retrievs the metadata records for a dataset to get the sparc award number
     */
    getDatasetRecords: async function() {
      try {
        const summary = await this.$axios
          .$get(`${this.getRecordsUrl}&model=summary`)
          .catch(
            // handle error
            (this.errorLoading = true)
          )
        const award = await this.$axios
          .$get(`${this.getRecordsUrl}&model=award`)
          .catch(
            // handle error
            (this.errorLoading = true)
          )

        const summaryId = compose(
          propOr('', 'hasAwardNumber'),
          propOr([], 'properties'),
          head,
          propOr([], 'records')
        )(summary)

        const awardId = compose(
          propOr('', 'award_id'),
          propOr([], 'properties'),
          head,
          propOr([], 'records')
        )(award)

        this.sparcAwardNumber = summaryId || awardId
      } catch (e) {
        console.error(e)
      }
    }
  }
}
</script>

<style lang="scss" scoped>
@import '@/assets/_variables.scss';
.dataset-about-info {
  &__container {
    h3 {
      font-size: 0.875em;
      font-weight: 500;
      line-height: 1em;
      color: black;
    }

    p {
      font-size: 0.875em;
      font-weight: normal;
      line-height: 24px;
      color: black;
    }

    &--citation {
      height: 100%;
      background: $washed-gray;
      padding-left: 1rem;
      padding-right: 1rem;
      margin-bottom: 1.5rem;
      .copy-button {
        margin: 1.875rem 0 1rem 0;
        background: #f9f2fc;
        border: 1px solid $median;
        cursor: pointer;
        color: $median;
        &:hover {
          color: #1a1489;
        }
      }
    }

    .info-citation {
      font-size: 14px;
      font-weight: normal;
      line-height: 24px;
      color: black;
      margin-top: 1rem;
    }

    &--citation-links {
      border-bottom: 1px solid #e4e7ed;
      display: flex;
      flex-wrap: wrap;
      list-style: none;
      padding: 0;
      li {
        margin-right: 0.5rem;
        :hover {
          border-bottom: 2px solid $median;
          padding-bottom: 0.094rem;
        }
        a {
          color: black;
          text-decoration: none;
          padding: 0 0.5rem;
          cursor: pointer;
          &.active-citation {
            color: $median;
            border-bottom: 2px solid $median;
            padding-bottom: 0.094rem;
          }
        }
      }
    }

    &--protocol-text {
      color: black;
      text-decoration: none;
      font-size: 0.875em;
      line-height: 24px;
      font-weight: normal;
    }

    &--protocol-text-na {
      p {
        margin-bottom: 0;
      }
    }

    .protocol-block {
      margin-bottom: 1rem;
    }

    &--doi-link {
      color: $median;
      text-decoration: none;
      font-weight: 500;
    }
  }
}
</style>
