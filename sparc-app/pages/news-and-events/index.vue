<template>
  <div class="events-page">
    <breadcrumb :breadcrumb="breadcrumb" :title="title" />
    <page-hero>
      <h1>{{ page.fields.page_title }}</h1>
      <!-- eslint-disable vue/no-v-html -->
      <!-- marked will sanitize the HTML injected -->
      <div v-html="parseMarkdown(page.fields.heroCopy)" />
      <search-controls-contentful
        placeholder="Search news and events"
        path="/news-and-events"
      />
      <img
        v-if="page.fields.heroImage"
        slot="image"
        class="page-hero-img"
        :src="page.fields.heroImage.fields.file.url"
      />
    </page-hero>

    <div class="page-wrap">
      <div class="container">
        <div v-if="Object.keys(featuredEvent).length" class="mb-48">
          <h2>Featured Event</h2>
          <featured-event :event="featuredEvent" />
        </div>

        <el-row :gutter="32">
          <el-col :sm="12">
            <h2>Latest News</h2>
            <div class="subpage news-wrap">
              <div>
                <news-list-item v-for="newsItem in news.items" :key="newsItem.sys.id" :item="newsItem" />

                <nuxt-link
                  class="btn-load-more mt-16"
                  :to="{
                    name: 'news-and-events-news'
                  }"
                >
                  View All News &gt;
                </nuxt-link>
              </div>
            </div>
          </el-col>
          <el-col :sm="12">
            <h2>Events</h2>
            <tab-nav
              :tabs="eventsTabs"
              :active-tab="activeTab"
              @set-active-tab="activeTab = $event"
            />
            <div class="events-wrap">
              <template v-if="activeTab === 'upcoming'">
                <div class="upcoming-events">
                  <event-card
                    v-for="event in upcomingEvents.items"
                    :key="event.sys.id"
                    :event="event"
                  />
                </div>

                <div class="show-all-upcoming-events">
                  <nuxt-link
                    class="show-all-upcoming-events__btn"
                    :to="{
                      name: 'news-and-events-events'
                    }"
                  >
                    Show All ({{ upcomingEvents.total }}) Events
                  </nuxt-link>
                </div>
              </template>

              <template v-if="activeTab === 'past'">
                <div class="past-events">
                  <event-card
                    v-for="event in pastEvents.items"
                    :key="event.sys.id"
                    :event="event"
                  />
                </div>

                <div class="show-all-upcoming-events">
                  <nuxt-link
                    class="show-all-upcoming-events__btn"
                    :to="{
                      name: 'news-and-events-events',
                      query: {
                        tab: 'past'
                      }
                    }"
                  >
                    Show All ({{ pastEvents.total }}) Past Events
                  </nuxt-link>
                </div>
              </template>
            </div>
          </el-col>
        </el-row>

        <h2>Community Spotlight</h2>
        <community-spotlight-listings :stories="shownStories" :in-news="true" />

        <h2>Stay Connected</h2>
        <div class="subpage">
          <el-row :gutter="32">
            <el-col :xs="24" :sm="12" class="newsletter-wrap">
              <h3 class="mb-24">Sign up to the SPARC Newsletter</h3>
              <p class="mb-40">Keep up to date with all the latest news and events from the SPARC portal.</p>
              <newsletter-form />
            </el-col>
            <el-col :xs="24" :sm="12" class="twitter-wrap">
              <div v-twitter-widgets>
                <a
                  class="twitter-timeline"
                  href="https://twitter.com/sparc_science?ref_src=twsrc%5Etfw"
                  data-height="500"
                  target="_blank"
                >
                  Tweets by sparc_science
                </a>
              </div>
            </el-col>
          </el-row>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import Vue from 'vue';
import Breadcrumb from '@/components/Breadcrumb/Breadcrumb.vue';
import TabNav from '@/components/TabNav/TabNav.vue';
import EventListItem from '@/components/EventListItem/EventListItem.vue';
import NewsListItem from '@/components/NewsListItem/NewsListItem.vue';
import EventCard from '@/components/EventCard/EventCard.vue';
import PageHero from '@/components/PageHero/PageHero.vue';
import SearchControlsContentful from '@/components/SearchControlsContentful/SearchControlsContentful.vue';
import NewsletterForm from '@/components/NewsletterForm/NewsletterForm.vue';
import FeaturedEvent from '@/components/FeaturedEvent/FeaturedEvent.vue';

import MarkedMixin from '@/mixins/marked'

import createClient from '@/plugins/contentful.js';

import { Computed, Data, Methods, fetchData, fetchNews, PageEntry, NewsAndEventsComponent, NewsCollection, EventsCollection, StoryCollection } from './model';
import CommunitySpotlightListings from '~/components/CommunitySpotlight/CommunitySpotlightListings.vue';

const client = createClient()
const MAX_PAST_EVENTS = 8

export default Vue.extend<Data, Methods, Computed, never>({
  name: 'NewsAndEventPage',

  mixins: [
    MarkedMixin
  ],

  components: {
    Breadcrumb,
    EventCard,
    EventListItem,
    PageHero,
    NewsListItem,
    TabNav,
    SearchControlsContentful,
    NewsletterForm,
    FeaturedEvent,
    CommunitySpotlightListings
  },

  asyncData() {
    return fetchData(client, '', 2)
  },

  watch: {
    '$route.query': {
      handler: async function(this: NewsAndEventsComponent) {
        const { upcomingEvents, pastEvents, news, page, stories } = await fetchData(client, this.$route.query.search as string, 2)
        this.upcomingEvents = upcomingEvents;
        this.pastEvents = pastEvents;
        this.news = news;
        this.page = page;
        this.stories = stories;
      },
      immediate: true
    }
  },

  data: function() {
    return {
      title: 'News & Events',
      breadcrumb: [
        {
          to: {
            name: 'index'
          },
          label: 'Home'
        }
      ],
      activeTab: 'upcoming',
      eventsTabs: [
        {
          label: 'Upcoming',
          type: 'upcoming'
        },
        {
          label: 'Past',
          type: 'past'
        }
      ],
      upcomingEvents: {} as EventsCollection,
      pastEvents: {} as EventsCollection,
      news: {} as NewsCollection,
      page: {} as PageEntry,
      stories: {} as StoryCollection
    }
  },

  computed: {
    /**
     * Compute featured event
     * @returns {Object}
     */
    featuredEvent: function() {
      return this.page.fields.featuredEvent || {}
    },
    /**
     * Filter to only show two stories
     * @returns {Array}
     */
    shownStories: function() {
      return this.stories.items.slice(0,2)
    }
  },

  methods: {
    /**
     * Get all news
     */
    getAllNews: async function() {
      const news = await fetchNews(client, this.$route.query.search as string, this.news.total, 2)
      this.news = { ...this.news, items: { ...this.news.items, ...news.items } }
    }
  }
})
</script>

<style lang="scss" scoped>
@import '@/assets/_variables.scss';

h2 {
  font-size: 1.5rem;
  line-height: 2.25rem;
}

h3 {
  color: $navy;
  font-size: 1.375rem;
  line-height: 2rem;
}
.subpage {
  @media (min-width: 48em) {
    margin: 3rem 0;
  }
  &.news-wrap {
    @media (min-width: 48em) {
      margin: 2rem 0 0;
    }
  }
}
.event-card {
  margin-bottom: 2em;
}
::v-deep .details-tabs__container {
  background: none;
  border: none;
  margin: 1em 0;
  padding: 0;
}
.upcoming-events, .past-events {
  display: flex;
  flex-wrap: wrap;
  margin: 0 -1em;
}
.upcoming-event {
  margin: 0 1rem 1rem;
  width: 100%;
  @media (min-width: 48em) {
    width: calc(50% - 4.125em); // Account for the margins and the border
  }
}
.show-all-upcoming-events {
  text-align: center;
  &__btn {
    align-items: center;
    color: $navy;
    display: inline-flex;
    font-weight: 500;
    text-decoration: none;
    &:hover,
    &:focus {
      text-decoration: underline;
    }
  }
  .svg-icon {
    margin-left: 0.5rem;
  }
}

.show-more-past-events {
  text-align: center;
  &__btn {
    display: inline-flex;
    border: 1px solid $dark-gray;
    border-radius: 5px;
    text-decoration: none;
    padding: 8px 10px;
    font-size: 11pt;
    font-weight: bold;
    color: $dark-gray;
  }
}
.events-wrap {
  margin-bottom: 2.625em;
}
.news-list-item {
  border-bottom: 2px solid #d8d8d8;
  padding: 1.5em 0;
  &:first-child {
    padding-top: 0;
  }
}
.newsletter-wrap {
  font-size: 1.125rem;
  line-height: 1.5rem;
  margin-bottom: 2rem;
  @media (min-width: 48em) {
    margin-bottom: 0;
  }
  p {
    color: $navy
  }
}
.twitter-wrap {
  @media (min-width: 48em) {
    border-left: 2px solid #d8d8d8;
  }
}

.btn-load-more {
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
