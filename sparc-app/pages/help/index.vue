<template>
  <div class="help-page">
    <breadcrumb :breadcrumb="breadcrumb" :title="allHelpData.title" />
    <help-hero :title="allHelpData.title" :summary="allHelpData.summary" />
    <div v-loading="isLoadingSearch">
      <help-section
        v-for="item in helpData.sections"
        :key="item.sys.id"
        class="help-section"
        :section="item"
        :searchTerms="searchTerms"
      />
    </div>
  </div>
</template>

<script lang="ts">
import Vue from 'vue';
import { Route } from 'vue-router';
import createClient from '@/plugins/contentful.js'
import {Data, HelpData, HelpDocument, Methods} from "./model";
import HelpSection from "@/components/HelpSection/HelpSection.vue";
import HelpHero from "@/components/HelpHero/HelpHero.vue";
import Breadcrumb from '@/components/Breadcrumb/Breadcrumb.vue'

const client = createClient()


export default Vue.extend<Data, Methods, never, never>({
  name: 'HelpPage',

  components: {
    Breadcrumb,
    HelpSection,
    HelpHero
  },

  mounted: function(this: Methods & { $route: Route }) {
    this.doSearch(this.$route.query.search as string | undefined)
  },

  watch: {
    '$route.query.search': function(this: Methods & { $route: Route }) {
      /**
       * Clear table data so the new table that is rendered can
       * properly render data and account for any missing data
       */
      this.doSearch(this.$route.query.search as string | undefined)
    }
  },

  data() {
    return {
      allHelpData: {},
      helpData: {},
      isLoadingSearch: false,
      searchTerms: '',
      breadcrumb: [
        {
          to: {
            name: 'index'
          },
          label: 'Home'
        }
      ]
    }
  },

  async asyncData() {
    const { fields } = await client.getEntry<HelpData>(process.env.ctf_support_page_id as string, { include: 2 })
    return {
      allHelpData: fields,
      helpData: {},
      isLoadingSearch: false,
      searchTerms: '',
    }
  },

  methods: {
    doSearch: async function(this: Data, terms) {
      this.isLoadingSearch = true;
      this.searchTerms = terms;
      try {
        if (terms) {
          const { items } = await client
            .getEntries<HelpDocument>({
              content_type: 'helpDocument',
              query: terms
            })

          this.helpData = {
            ...this.allHelpData,
            sections: (this.allHelpData.sections ?? []).map(section => ({
              ...section,
              fields: {
                ...section.fields,
                helpDocuments: section.fields.helpDocuments
                  .filter(hd => items.find(r => r.sys.id === hd.sys.id))
              }
            }))
          }

        } else {
          this.helpData = this.allHelpData
        }
      } catch (e) {
        console.error(e)
      } finally {
        this.isLoadingSearch = false
      }
    }
  }


})
</script>

<style lang="scss" scoped>
@import '@/assets/_variables.scss';
.page-hero {
  background-color: #292b66;
  background-image: none;
  h2 {
    font-size: 2rem;
    font-weight: 500;
    margin-bottom: 1rem;
  }
}
::v-deep h2 {
  font-size: 1.5em;
  font-weight: 500;
  line-height: 2rem;
  margin-bottom: 2rem;
  @media (min-width: 768px) {
    font-size: 1.5em;
    margin-bottom: 2rem;
  }
}
</style>
