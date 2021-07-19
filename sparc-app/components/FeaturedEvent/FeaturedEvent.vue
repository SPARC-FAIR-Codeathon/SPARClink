<template>
  <sparc-card>
    <template slot="image">
      <nuxt-link
        v-if="event.fields.requiresADetailsPage"
        :to="{
          name: 'news-and-events-events-id',
          params: { id: event.sys.id }
        }"
        class="sparc-card__image"
        :style="`background-image: url(${imageSrc})`"
      >
        <img class="visuallyhidden" :src="imageSrc" :alt="imageAlt" />
      </nuxt-link>
      <template v-else>
        <a
          v-if="event.fields.url"
          :href="event.fields.url"
          target="_blank"
          class="sparc-card__image"
          :style="`background-image: url(${imageSrc})`"
        >
          <img class="visuallyhidden" :src="imageSrc" :alt="imageAlt" />
        </a>
        <div
          v-else
          class="sparc-card__image"
          :style="`background-image: url(${imageSrc})`"
        >
          <img class="visuallyhidden" :src="imageSrc" :alt="imageAlt" />
        </div>
      </template>
    </template>

    <div>
      <h3>
        <nuxt-link
          v-if="event.fields.requiresADetailsPage"
          :to="{
            name: 'news-and-events-events-id',
            params: { id: event.sys.id }
          }"
        >
          {{ event.fields.title }}
        </nuxt-link>
        <template v-else>
          <a v-if="event.fields.url" :href="event.fields.url" target="_blank">
            {{ event.fields.title }}
          </a>
          <div v-else>
            {{ event.fields.title }}
          </div>
        </template>
      </h3>
      <div class="sparc-card__detail">
        <svg-icon name="icon-calendar" height="16" width="16" />
        <p>{{ eventDate }}</p>
        <template v-if="event.fields.location">
          <svg-icon
            class="sparc-card__detail--location"
            name="icon-map"
            height="16"
            width="16"
          />
          <p>{{ event.fields.location }}</p>
        </template>
      </div>
      <!-- eslint-disable vue/no-v-html -->
      <!-- marked will sanitize the HTML injected -->
      <div v-html="parseMarkdown(event.fields.summary)" />
    </div>
    <nuxt-link
      v-if="event.fields.requiresADetailsPage"
      :to="{
        name: 'news-and-events-events-id',
        params: { id: event.sys.id }
      }"
      class="btn-permalink"
    >
      <el-button size="medium">
        Learn More
      </el-button>
    </nuxt-link>

    <a v-else :href="event.fields.url" target="_blank" class="btn-permalink">
      <el-button size="medium">
        Learn More
      </el-button>
    </a>
  </sparc-card>
</template>

<script>
import { pathOr } from 'ramda'

import SparcCard from '@/components/SparcCard/SparcCard.vue'

import FormatDate from '@/mixins/format-date'
import MarkedMixin from '@/mixins/marked'

export default {
  name: 'FeaturedEvent',

  components: {
    SparcCard
  },

  mixins: [MarkedMixin, FormatDate],

  props: {
    event: {
      type: Object,
      default: () => {
        return {}
      }
    }
  },

  computed: {
    /**
     * Get image source
     * @returns {String}
     */
    imageSrc: function() {
      return pathOr(
        '',
        ['fields', 'image', 'fields', 'file', 'url'],
        this.event
      )
    },
    /**
     * Get image source
     * @returns {String}
     */
    imageAlt: function() {
      return pathOr(
        '',
        ['fields', 'image', 'fields', 'file', 'description'],
        this.event
      )
    },

    /**
     * Get event date range, if there is no end date, default to start date
     * @returns {String}
     */
    eventDate: function() {
      const startDate = this.formatDate(this.event.fields.startDate || '')
      const endDate = this.formatDate(this.event.fields.endDate || '')
      return startDate === endDate || !endDate
        ? startDate
        : `${startDate} - ${endDate}`
    }
  }
}
</script>

<style lang="scss" scoped>
.sparc-card {
  h3 {
    font-size: 1.5rem;
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
  .btn-permalink {
    margin-top: 1.5rem;
  }
}
::v-deep .sparc-card__content-wrap {
  flex: 2.5;
  &__content {
    box-sizing: border-box;
    justify-content: normal;
    min-height: 17.562rem;
    padding: 2rem 2.5rem;
  }
}
</style>
