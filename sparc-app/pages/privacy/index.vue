<template>
  <markdown-page :header="header" :body="body" />
</template>

<script lang="ts">
import Vue from 'vue';
import {asyncMarkdown} from "~/components/MarkdownPage/asyncMarkdown";
import MarkdownPage from "~/components/MarkdownPage/MarkdownPage.vue";

export default Vue.extend<{ header: string, body: string }, never, never, never>({
  name: 'PrivacyPolicy',

  data() {
    return { header: '', body: '' }
  },

  components: {
    MarkdownPage
  },

  asyncData() {
    return asyncMarkdown(
      process.env.ctf_privacy_policy_id as string,
      'heroCopy',
      'privacyPolicyCopy'
    )
  }
})
</script>

<style lang="scss" scoped></style>
