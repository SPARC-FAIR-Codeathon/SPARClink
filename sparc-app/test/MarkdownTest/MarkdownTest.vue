<template>
  <div>
    <!-- eslint-disable vue/no-v-html -->
    <!-- marked will sanitize the HTML injected -->
    <div id="externalWrap" v-html="parseMarkdown(markdown)" />
    <div id="anchorWrap" v-html="parseMarkdown(markdownAnchor)" />
  </div>
</template>

<script>
import MarkedMixin from '@/mixins/marked'

export default {
  name: 'MarkdownTest',

  mixins: [MarkedMixin],

  data() {
    return {
      markdown: `[go to SPARC](https://sparc.science) \n # This is a heading`,
      markdownAnchor: `[Link to section](#foo) \n # Foo`
    }
  }
}
</script>

<style lang="scss" scoped></style>
