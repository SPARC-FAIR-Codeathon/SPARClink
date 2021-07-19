<template>
  <div class="events-page">
    content here
    <p>{{ testdata }}</p>
  </div>
</template>

<script lang="ts">
import Vue from "vue";
import Breadcrumb from "@/components/Breadcrumb/Breadcrumb.vue";

import MarkedMixin from "@/mixins/marked";

import createClient from "@/plugins/contentful.js";

import {
  Computed,
  Data,
  Methods,
  fetchData,
  fetchNews,
  PageEntry,
  NewsAndEventsComponent,
  NewsCollection,
  EventsCollection,
  StoryCollection,
} from "./model";

const client = createClient();
const MAX_PAST_EVENTS = 8;

export default Vue.extend<Data, Methods, Computed, never>({
  name: "SparcLink",

  mixins: [MarkedMixin],

  components: {
    Breadcrumb,
  },

  asyncData() {
    return fetchData(client, "", 2);
  },

  watch: {
    "$route.query": {
      handler: async function(this: NewsAndEventsComponent) {
        const {
          upcomingEvents,
          pastEvents,
          news,
          page,
          stories,
        } = await fetchData(client, this.$route.query.search as string, 2);
        this.upcomingEvents = upcomingEvents;
        this.pastEvents = pastEvents;
        this.news = news;
        this.page = page;
        this.stories = stories;
      },
      immediate: true,
    },
  },

  data: function() {
    return {
      title: "News & Events",
      breadcrumb: [
        {
          to: {
            name: "index",
          },
          label: "Home",
        },
      ],
      activeTab: "upcoming",
      eventsTabs: [
        {
          label: "Upcoming",
          type: "upcoming",
        },
        {
          label: "Past",
          type: "past",
        },
      ],
      upcomingEvents: {} as EventsCollection,
      pastEvents: {} as EventsCollection,
      news: {} as NewsCollection,
      page: {} as PageEntry,
      stories: {} as StoryCollection,
      testdata: 1,
    };
  },

  computed: {
    /**
     * Compute featured event
     * @returns {Object}
     */
    featuredEvent: function() {
      return this.page.fields.featuredEvent || {};
    },
    /**
     * Filter to only show two stories
     * @returns {Array}
     */
    shownStories: function() {
      return this.stories.items.slice(0, 2);
    },
  },
  
  methods: {
    /**
     * Get all news
     */
    getAllNews: async function() {
      const news = await fetchNews(
        client,
        this.$route.query.search as string,
        this.news.total,
        2
      );
      this.news = {
        ...this.news,
        items: { ...this.news.items, ...news.items },
      };
    },
  },
});
</script>

<style lang="scss" scoped>
@import "@/assets/_variables.scss";

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
.upcoming-events,
.past-events {
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
    color: $navy;
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
