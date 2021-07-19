<template>
  <div class="events-page">
    <breadcrumb :breadcrumb="breadcrumb" :title="title" />
    <page-hero>
      <h1>{{ title }}</h1>
      <br />
      <p>
        {{ entry.summary }}
      </p>
    </page-hero>
    <div class="page-wrap container">
      <div class="subpage">
        <el-row :gutter="38">
          <el-col :sm="13">
            <div class="content" v-html="renderedStory" />
          </el-col>
          <el-col :sm="11">
            <div class="banner-wrapper">
              <iframe
                v-if="entry.youtubeUrl"
                class="banner-asset"
                :src="embeddedVideoSrc"
                allowfullscreen
                allowtransparency
                allow="autoplay"
                frameBorder="0"
              />
              <img
                v-else-if="entry.files"
                class="banner-asset"
                :src="entry.files[0].fields.file.url"
                :alt="entry.files[0].description"
              />
            </div>
            <div class="seperator-path" />
            <div class="story-bold-field">
              Author
            </div>
            <div class="story-field">
              {{ entry.name }}
            </div>
            <br />
            <template v-if="entry.publishDate">
              <div class="story-bold-field">
                Published Date
              </div>
              <div class="story-field">
                {{ formatDate(entry.publishDate) }}
              </div>
              <br />
            </template>
            <template v-if="entry.teamMemberNames">
              <div class="story-bold-field">
                Team Members
              </div>
              <div
                v-for="(item, index) in entry.teamMemberNames"
                :key="'name' + index"
                class="story-field"
              >
                {{ item }}
                <template v-if="entry.teamMemberOrcidIds && entry.teamMemberOrcidIds.length - 1 > index">
                  ({{ entry.teamMemberOrcidIds[index] }})
                </template>
              </div>
              <br />
            </template>
            <template v-if="entry.references">
              <div class="story-bold-field">
                Supporting information
              </div>
              <div
                v-for="(item, index) in entry.references"
                :key="'reference' + index"
                class="story-field"
              >
                <a :href="item" target="_blank">{{ item }}</a>
              </div>
              <br />
            </template>
            <div class="story-bold-field">
              Share
            </div>
            <div class="share-links">
              <share-network
                network="facebook"
                :url="pageUrl"
                :title="title"
              >
                <svg-icon name="icon-share-facebook" height="28" width="28" />
                <span class="visuallyhidden">Share on Facebook</span>
              </share-network>
              <share-network
                network="twitter"
                class="ml-8"
                :url="pageUrl"
                :title="title"
              >
                <svg-icon name="icon-share-twitter" height="28" width="28" />
                <span class="visuallyhidden">Share on Twitter</span>
              </share-network>
              <share-network
                network="linkedin"
                class="ml-8"
                :url="pageUrl"
                :title="title"
              >
                <svg-icon name="icon-share-linked" height="28" width="28" />
                <span class="visuallyhidden">Share on Linkedin</span>
              </share-network>
              <button class="ml-8 btn-copy-permalink" @click="copyLink">
                <svg-icon name="icon-permalink" height="28" width="28" />
                <span class="visuallyhidden">Copy permalink</span>
              </button>
            </div>
            <div class="seperator-path" />
            <template v-if="entry.associatedDatasets">
              <div class="story-bold-field">
                Associated Datasets
              </div>
              <br />
              <div
                v-for="(datasetUrl, index) in entry.associatedDatasets"
                :key="'dataset' + index"
                class="story-field"
              >
                <dataset-card :id="datasetIdFromUrl(datasetUrl)" />
              </div>
            </template>
          </el-col>
        </el-row>
      </div>
      <nuxt-link
        class="community-link mt-16"
        :to="{
          name: 'news-and-events-community-spotlight'
        }"
      >
        View All Community Spotlights &gt;
      </nuxt-link>
    </div>
  </div>
</template>

<script>
import { documentToHtmlString } from '@contentful/rich-text-html-renderer'
import { BLOCKS } from '@contentful/rich-text-types'
import { successMessage, failMessage } from '@/utils/notification-messages'
import Breadcrumb from '@/components/Breadcrumb/Breadcrumb.vue'
import PageHero from '@/components/PageHero/PageHero.vue'
import DatasetCard from '@/components/DatasetCard/DatasetCard.vue'
import createClient from '@/plugins/contentful.js'
import youtubeEmbeddedSource from '@/mixins/youtube-embedded-src'
import FormatDate from '@/mixins/format-date'

// options for rendering contentful rich text. Modified from:
// https://www.contentful.com/blog/2021/04/14/rendering-linked-assets-entries-in-contentful/
const options = {
  renderNode: {
    [BLOCKS.EMBEDDED_ENTRY]: node => {
      if (node.data.target.sys.contentType.sys.id === 'videoEmbed') {
        return `
        <div style="position:relative;padding-bottom:56.25%;height:0;">
          <iframe
            src="${youtubeEmbeddedSource(node.data.target.fields.embedUrl)}"
            frameBorder="0"
            scrolling="no"
            title="${node.data.target.fields.title}"
            allowFullScreen="true"
            allowtransparency="true"
          />
        </div>`
      }
    },
    [BLOCKS.EMBEDDED_ASSET]: node => {
      const fields = node.data.target.fields
      if (fields.file.contentType.includes('video')){
        return `
        <div style="position:relative;padding-bottom:56.25%;height:0;">
          <video id="video" controls="" autoplay="false" name="media"><source src="${fields.file.url}" type="${fields.file.contentType}"></video>
        </div>`
      } else if (fields.file.contentType.includes('image')) {
        return `<img src="${fields.file.url}" height="${fields.file.details.image.height}" width="${fields.file.details.image.width}" alt="${fields.description}"/>`
      }
    }
  }
}

const client = createClient()

export default {
  name: 'StoryPage',
  components: {
    DatasetCard,
    Breadcrumb,
    PageHero
  },
  mixins: [FormatDate],
  async asyncData({ route }) {
    try {
      const results = await client.getEntries({
        content_type: 'successStory',
        'fields.storyRoute[match]': route.params.id,
        include: 1,
      })
      return {
        entry: results.items[0].fields,
        slug: route.params.slug,
        title: results.items[0].fields.storyTitle
      }
    } catch (error) {
      return {
        title: '',
        entry: {},
        slug: ''
      }
    }
  },
  data: function() {
    return {
      title: '',
      entry: {},
      slug: '',
      breadcrumb: [
        {
          label: 'Home',
          to: {
            name: 'index'
          }
        },
        {
          label: 'News & Events',
          to: {
            name: 'news-and-events'
          }
        },
        {
          label: 'Community Spotlight',
          to: {
            name: 'news-and-events-community-spotlight'
          }
        }
      ]
    }
  },
  computed: {
    pageUrl: function() {
      return `${process.env.ROOT_URL}${this.$route.fullPath}`
    },
    renderedStory: function() {
      if (this.entry.story) {
        return documentToHtmlString(this.entry.story, options)
      }
      return ''
    },
    embeddedVideoSrc: function() {
      return youtubeEmbeddedSource(this.entry.youtubeUrl)
    }
  },
  methods: {
    // Retrieve dataset id form sparc.science, discover.pennsieve, or just the id
    datasetIdFromUrl: function(url) {
      if (!url.includes('/')) return Number(url)
      let datasetId = url.split('/').pop()
      if (datasetId.includes('?')) datasetId = datasetId.split('?')[0]
      return Number(datasetId)
    },
    copyLink: function() {
      this.$copyText(this.pageUrl).then(
        () => {
          this.$message(successMessage('Share link copied to clipboard.'))
        },
        () => {
          this.$message(failMessage('Failed to copy share link.'))
        }
      )
    }
  }
}
</script>

<style lang="scss" scoped>
@import '@/assets/_variables.scss';

.page-wrap {
  max-width: 66.75rem;
  @media (max-width: 48em) {
    width: auto;
  }
}

.banner-wrapper {
  position: relative;
  padding-bottom: 56.25%; /* 16:9 */
  height: 0;
}

.banner-wrapper .banner-asset {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
}

.iframe-wrapper {
  position: relative;
  padding-bottom: 56.25%; /* 16:9 */
  height: 0;
  min-width: 25.68rem;
}

// Used for sizing iframes that are in the content

.content {
  & ::v-deep {
    color: $vestibular;
  }
  & ::v-deep p {
    margin-bottom: 1em;
  }
  & ::v-deep img {
    height: auto;
    margin: 0.5em 0;
    max-width: 100%;
  }
  & ::v-deep iframe {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
  }
  & ::v-deep video {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
  }
  @media (max-width: 48em) {
    margin-bottom: 2rem;
  }
}

.seperator-path {
  width: 100%;
  height: 2px;
  background: rgb(216, 216, 216);
  border-radius: 0px;
  margin-top: 32px;
  margin-bottom: 32px;
}

.story-bold-field {
  color: rgb(0, 0, 0);
  font-family: Asap;
  font-size: 14px;
  font-weight: 600;
  text-transform: uppercase;
}

.story-field {
  font-family: Asap;
  font-size: 14px;
  line-height: 24px;
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

.header {
  margin-bottom: 3em;
  .updated {
    color: #aaa;
  }
}

.community-link {
  background: none;
  border: none;
  color: $navy;
  cursor: pointer;
  display: block;
  font-size: 1rem;
  font-weight: 700;
  padding: 0;
  &:hover,
  &:active {
    text-decoration: underline;
  }
}
</style>
