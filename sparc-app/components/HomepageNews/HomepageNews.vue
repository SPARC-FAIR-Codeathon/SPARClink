<template>
  <div class="featured-datasets container">
    <div class="home-container">
      <h2>
        <nuxt-link to="/news-and-events">
          News &amp; Upcoming Events
        </nuxt-link>
      </h2>
      <sparc-card
        v-for="(item, idx) in upcomingNews"
        :key="item.sys.id"
        :image-align="idx % 2 ? 'right' : ''"
      >
        <template slot="image">
          <nuxt-link
            v-if="item.fields.requiresADetailsPage"
            :to="nuxtLink(item)"
            class="sparc-card__image"
            :style="`background-image: url(${getImageSrc(item)})`"
          >
            <img
              class="visuallyhidden"
              :src="getImageSrc(item)"
              :alt="getImageAlt(item)"
            />
          </nuxt-link>
          <template v-else>
            <a
              v-if="item.fields.url"
              :href="item.fields.url"
              target="_blank"
              class="sparc-card__image"
              :style="`background-image: url(${getImageSrc(item)})`"
            >
              <img
                class="visuallyhidden"
                :src="getImageSrc(item)"
                :alt="getImageAlt(item)"
              />
            </a>
            <div
              v-else
              class="sparc-card__image"
              :style="`background-image: url(${getImageSrc(item)})`"
            >
              <img
                class="visuallyhidden"
                :src="getImageSrc(item)"
                :alt="getImageAlt(item)"
              />
            </div>
          </template>
        </template>
        <div>
          <h3>
            <nuxt-link
              v-if="item.fields.requiresADetailsPage"
              :to="nuxtLink(item)"
            >
              {{ item.fields.title }}
            </nuxt-link>
            <a
              v-else
              :href="item.fields.url"
              :target="isInternalLink('item.fields.url') ? '_self' : '_blank'"
            >
              {{ item.fields.title }}
            </a>
          </h3>
          <div class="sparc-card__detail">
            <svg-icon name="icon-calendar" height="16" width="16" />
            <p>{{ eventDate(item) }}</p>
            <template v-if="item.fields.location">
              <svg-icon
                class="sparc-card__detail--location"
                name="icon-map"
                height="16"
                width="16"
              />
              <p>{{ item.fields.location }}</p>
            </template>
          </div>
          <!-- eslint-disable vue/no-v-html -->
          <!-- marked will sanitize the HTML injected -->
          <div v-html="parseMarkdown(item.fields.summary)" />
        </div>
        <nuxt-link v-if="item.fields.requiresADetailsPage" :to="nuxtLink(item)">
          <el-button size="medium">
            Learn More
          </el-button>
        </nuxt-link>
        <a
          v-else
          :href="item.fields.url"
          :target="isInternalLink('item.fields.url') ? '_self' : '_blank'"
        >
          <el-button size="medium">
            Learn More
          </el-button>
        </a>
      </sparc-card>
    </div>
  </div>
</template>

<script>
import { pathOr } from 'ramda'

import SparcCard from '@/components/SparcCard/SparcCard.vue'

import MarkedMixin from '@/mixins/marked'
import FormatDate from '@/mixins/format-date'
import { isInternalLink } from '@/mixins/marked/index'

export default {
  name: 'HomepageNews',

  components: {
    SparcCard
  },

  mixins: [MarkedMixin, FormatDate],

  props: {
    news: {
      type: Array,
      default: () => []
    }
  },

  computed: {
    /**
     * Filter news to remove past events
     * @returns {Array}
     */
    upcomingNews: function() {
      return this.news.filter(event => this.isUpcoming(event))
    }
  },

  methods: {
    isInternalLink,

    /**
     * Get image source
     * @param {Object} item
     * @returns {String}
     */
    getImageSrc: function(item) {
      return pathOr('', ['fields', 'image', 'fields', 'file', 'url'], item)
    },
    /**
     * Get image source
     * @param {Object} item
     * @returns {String}
     */
    getImageAlt: function(item) {
      return pathOr(
        '',
        ['fields', 'image', 'fields', 'file', 'description'],
        item
      )
    },
    /**
     * Get event date range, if there is no end date, default to start date
     * @returns {String}
     */
    eventDate: function(event) {
      const startDate = this.formatDate(event.fields.startDate || '')
      const endDate = this.formatDate(event.fields.endDate || '')
      return startDate === endDate || !endDate
        ? startDate
        : `${startDate} - ${endDate}`
    },
    /**
     * Check if an event is upcoming, if there is no end date, default to start date
     * @param {Object} item
     * @returns {Boolean}
     */
    isUpcoming: function(item) {
      const today = new Date()
      const checkDate = item.fields.endDate || item.fields.startDate || ''
      return checkDate ? Date.parse(checkDate) > Date.parse(today) : true
    },

    /**
     * Create nuxt link based on type
     * @param {Object} item
     * @returns {Object}
     */
    nuxtLink: function(item) {
      const name =
        item.sys.contentType.sys.id === 'news'
          ? 'news-and-events-news-id'
          : 'news-and-events-events-id'
      return {
        name,
        params: { id: item.sys.id }
      }
    }
  }
}
</script>

<style lang="scss" scoped>
@import '../../assets/_variables.scss';
.home-container {
  padding-left: 1rem;
  padding-right: 1rem;
  @media (min-width: 768px) {
    padding-left: 6rem;
    padding-right: 6rem;
  }
}
h2 a:not(:hover) {
  color: #000;
  text-decoration: none;
}
.sparc-card {
  margin-bottom: 24px;
  @media (min-width: 768px) {
    margin-bottom: 40px;
  }
  h3 {
    font-size: 1.333333333em;
  }
  &__detail {
    align-items: baseline;
    display: flex;
    margin-bottom: 0.625rem;
    .svg-icon {
      flex-shrink: 0;
      margin-right: 0.5rem;
    }
    p {
      margin-bottom: 0rem;
    }
    &--location {
      margin-left: 1.25rem;
    }
  }
}
</style>
