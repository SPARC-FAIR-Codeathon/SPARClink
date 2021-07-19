<template>
  <div v-loading="loadingMarkdown" class="dataset-description-info">
    <div
      class="col-xs-12 description-container"
      v-html="parseMarkdown(markdown.markdownTop)"
    />
    <div class="description-container__protocol-block">
      <p>
        <strong>
          Protocol Links:
        </strong>
      </p>
      <div v-if="datasetRecords.length !== 0">
        <p v-for="record in datasetRecords" :key="record.properties.id">
          <a
            :href="record.properties.url"
            target="_blank"
            class="description-container__protocol-block--protocol-text"
          >
            {{ record.properties.url }}
          </a>
        </p>
      </div>
      <div
        v-else
        class="description-container__protocol-block--protocol-text-na"
      >
        <p>N/A</p>
      </div>
    </div>
    <div
      v-if="markdown.markdownBottom"
      class="col-xs-12 description-container"
      v-html="parseMarkdown(markdown.markdownBottom)"
    />
  </div>
</template>

<script>
import marked from '@/mixins/marked/index'

export default {
  name: 'DatasetDescriptionInfo',

  mixins: [marked],

  props: {
    loadingMarkdown: {
      type: Boolean,
      default: false
    },
    markdown: {
      type: Object,
      default: () => {}
    },
    datasetRecords: {
      type: Array,
      default: () => []
    }
  }
}
</script>

<style lang="scss" scoped>
@import '@/assets/_variables.scss';
.dataset-description-info {
  // Markdown styles
  .description-container {
    color: #000;
    font-size: 16px;
    line-height: 24px;

    h1,
    p,
    h2,
    h3,
    blockquote,
    h4,
    pre {
      max-width: 616px;
    }

    h1,
    h2,
    h3,
    h4,
    h5 {
      margin: 0 0 8px;
    }

    h1 {
      font-size: 32px;
      font-weight: bold;
      line-height: 40px;
    }

    p {
      margin-bottom: 16px;
    }

    img {
      height: auto;
      max-width: 170%;
      margin-bottom: 20px;
      flex-basis: 50%;
      margin-top: 24px;
    }

    h2 {
      font-size: 24px;
      font-weight: bold;
      line-height: 32px;
    }

    h3 {
      font-size: 20px;
      font-weight: bold;
      line-height: 24px;
      letter-spacing: 0px;
    }

    h4 {
      font-size: 16px;
      font-weight: bold;
      line-height: 24px;
      text-transform: uppercase;
      letter-spacing: 0px;
    }

    ul {
      margin: 0 0 16px;
      padding: 0 0 0 18px;
    }

    blockquote {
      font-weight: normal;
      line-height: 24px;
      font-size: 16px;
      border-left: 8px solid #2760ff;
      margin-left: 0;

      p {
        margin-left: 16px;
      }
    }
    pre {
      background-color: #f1f1f3;
      line-height: 24px;
      padding: 16px;

      code {
        font-weight: normal;
        font-size: 14px;
      }
    }

    &__protocol-block {
      margin-bottom: 16px;

      p {
        margin-bottom: 4px;
      }

      &--protocol-text {
        color: $median;
        text-decoration: none;
        font-weight: 500;
      }

      &--protocol-text-na {
        font-size: 0.875em;
      }
    }
  }
}
</style>
