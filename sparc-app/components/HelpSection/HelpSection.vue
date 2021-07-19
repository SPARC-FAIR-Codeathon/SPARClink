<template>
  <div class="page-wrap container">
    <div class="subpage">
      <el-row type="flex" :gutter="32">
        <el-col :xs="24" :md="22" :lg="18">
          <div class="help-section">
            <h2>
              {{ section.fields.title }}
            </h2>
            <div class="section">
              <div v-if="section.fields.helpDocuments.length === 0 && searchTerms.length > 0">
                <div>
                  No results found for <span class="search-term">"{{ searchTerms }}"</span>
                </div>
                <div>Please try entering another search term.</div>
              </div>
              <help-card
                v-for="(item, index) in section.fields.helpDocuments"
                :key="`${item}-${index}`"
                :help-item="item"
                :search-terms="searchTerms"
              />
            </div>
          </div>
        </el-col>
      </el-row>
    </div>
  </div>
</template>

<script lang="ts">
import Vue from 'vue';
import HelpCard from '@/components/HelpCard/HelpCard.vue'
import {HelpSection} from "~/pages/help/model";

export default Vue.extend<never, never, never, { section: HelpSection, searchTerms: string }>({
  name: 'HelpSection',
  components: {
    HelpCard
  },
  props: {
    section: {
      type: Object,
      default: () => {
        return {
          sys: {},
          fields: {}
        } as HelpSection
      }
    },
    searchTerms: {
      type: String,
      default: ''
    }
  }
})
</script>

<style lang="scss" scoped>
@import '@/assets/_variables.scss';
.help-section {
  margin: 0 auto 2em auto;
}
.search-term {
  font-weight: bold;
}
</style>
