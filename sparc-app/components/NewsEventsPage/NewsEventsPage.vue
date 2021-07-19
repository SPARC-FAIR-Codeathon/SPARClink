<template>
  <div>
    <breadcrumb :breadcrumb="breadcrumb" :title="heroTitle" />
    <page-hero>
      <h1>{{ heroTitle }}</h1>
      <p>
        {{ heroSummary }}
      </p>
    </page-hero>
    <div class="page-wrap container">
      <div class="subpage">
        <!-- eslint-disable vue/no-v-html -->
        <!-- marked will sanitize the HTML injected -->
        <el-row :gutter="32">
          <el-col :xs="24" :sm="firstCol" class="details">
            <slot />

            <h3>Share</h3>
            <div class="share-links">
              <share-network
                network="facebook"
                :url="pageUrl"
                :title="heroTitle"
                :description="heroSummary"
              >
                <svg-icon name="icon-share-facebook" height="28" width="28" />
                <span class="visuallyhidden">Share on Facebook</span>
              </share-network>
              <share-network
                network="twitter"
                class="ml-8"
                :url="pageUrl"
                :title="heroTitle"
              >
                <svg-icon name="icon-share-twitter" height="28" width="28" />
                <span class="visuallyhidden">Share on Twitter</span>
              </share-network>
              <share-network
                network="linkedin"
                class="ml-8"
                :url="pageUrl"
                :title="heroTitle"
              >
                <svg-icon name="icon-share-linked" height="28" width="28" />
                <span class="visuallyhidden">Share on Linkedin</span>
              </share-network>
              <button
                @click="copyLink"
                class="ml-8 btn-copy-permalink"
              >
                <svg-icon name="icon-permalink" height="28" width="28" />
                <span class="visuallyhidden">Copy permalink</span>
              </button>
            </div>
          </el-col>
          <el-col :xs="24" :sm="secondCol">
            <div class="content" v-html="parseMarkdown(htmlContent)" />
          </el-col>
        </el-row>
      </div>

      <nuxt-link class="back-link" :to="{ name: backLink }">
        {{ backCopy }}
      </nuxt-link>
    </div>
  </div>
</template>

<script>
import { pathEq } from 'ramda'
import { successMessage, failMessage } from '@/utils/notification-messages'
import MarkedMixin from '@/mixins/marked'
import FormatDate from '@/mixins/format-date'
import Breadcrumb from '@/components/Breadcrumb/Breadcrumb'
import PageHero from '@/components/PageHero/PageHero'

export default {
  name: 'NewsEventsPage',

  components: {
    Breadcrumb,
    PageHero
  },

  mixins: [FormatDate, MarkedMixin],

  methods: {
    copyLink: function() {
      this.$copyText(`${process.env.ROOT_URL}${this.$route.fullPath}`).then(
        () => {
          this.$message(successMessage('Share link copied to clipboard.'))
      }, () => {
          this.$message(failMessage('Failed to copy share link.'))
      });
    },
  },

  props: {
    page: {
      type: Object,
      default: () => {
        return {}
      }
    },
    content: {
      type: String,
      default: ''
    },
    type: {
      type: String,
      default: ''
    },
    heroTitle: {
      type: String,
      default: ''
    },
    heroSummary: {
      type: String,
      default: ''
    },
    breadcrumb: {
      type: Array,
      default: () => {
        return []
      }
    }
  },

  computed: {
    /**
     * Compute HTML Content for the page
     * @returns {String}
     */
    htmlContent() {
      return this.content || ''
    },

    /**
     * Compute the first column's attributes
     * @returns {Object}
     */
    firstCol() {
      return this.type === 'event' ? { span: 12 } : { span: 12, push: 12 }
    },

    /**
     * Compute the first column's attributes
     * @returns {Object}
     */
    secondCol() {
      return this.type === 'event' ? { span: 12 } : { span: 12, pull: 12 }
    },

    /**
     * Compute back link, depending on the content type
     * @returns {String}
     */
    backLink() {
      return this.type === 'event'
        ? 'news-and-events-events'
        : 'news-and-events-news'
    },

    /**
     * Compute back link copy, depending on the content type
     * @returns {String}
     */
    backCopy() {
      const name = this.type === 'event' ? 'Events' : 'News'

      return `View All ${name} >`
    }
  }
}
</script>

<style lang="scss" scoped>
@import '@/assets/_variables.scss';

.content {
  & ::v-deep {
    color: $vestibular;
  }
  & ::v-deep p {
    margin-bottom: 1em;
  }
  & ::v-deep img,
  & ::v-deep video {
    height: auto;
    margin: 0.5em 0;
    max-width: 100%;
  }
}

.header {
  margin-bottom: 3em;
  .updated {
    color: #aaa;
  }
}
.details ::v-deep {
  font-size: 0.875rem;
  h3 {
    font-size: 0.875rem;
    font-weight: 500;
    line-height: 1.5rem;
    text-transform: uppercase;
  }
  img {
    height: auto;
    max-width: 100%;
  }
}
.share-links {
  display: flex;
}
.btn-copy-permalink {
  border: none;
  background: none;
  color: $median;
  cursor: pointer;
  padding: 0;
  &:active {
    outline: none;
  }
}
.back-link {
  color: $navy;
  font-weight: 700;
}
</style>
