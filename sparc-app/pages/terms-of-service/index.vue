<template>
  <markdown-page :header="header" :body="body" />
</template>

<script lang="ts">
import Vue from 'vue';
import MarkdownPage from '~/components/MarkdownPage/MarkdownPage.vue'
import {asyncMarkdown} from "~/components/MarkdownPage/asyncMarkdown";
export default Vue.extend<{ header: string, body: string }, never, never, never>({
  name: 'TermsOfService',

  data() {
    return { header: '', body: '' }
  },

  components: {
    MarkdownPage
  },

  asyncData() {
    return asyncMarkdown(
      process.env.ctf_terms_id as string,
      'heroCopy',
      'termsOfServiceCopy'
    )
  }
})
</script>
