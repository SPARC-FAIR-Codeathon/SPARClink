<template>
  <div class="content-markdown">
    <div class="page-wrap container">
      <div class="subpage">
        <el-row type="flex" justify="center">
          <el-col :row="24">
            <h2>{{ header }}</h2>
            <!-- eslint-disable vue/no-v-html -->
            <!-- marked will sanitize the HTML injected -->
            <div v-html="parseMarkdown(body)" />
          </el-col>
        </el-row>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import Vue from 'vue';
import MarkedMixin from '@/mixins/marked'

export default Vue.extend<never, never, never, { header: string, body: string }>({
  props: {
    header: {
      type: String,
      default: ''
    },
    body: {
      type: String,
      default: ''
    }
  },

  name: 'ContentMarkdown',

  mixins: [MarkedMixin],
})
</script>