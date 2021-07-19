<template>
  <div class="events-page">
    <breadcrumb :breadcrumb="breadcrumb" :title="title" />
    <page-hero>
      <h1>Events</h1>
      <p>
        Check out the latest events associated with the SPARC Portal
      </p>
    </page-hero>
    <div class="page-wrap">
      <div class="container">
        <div v-if="Object.keys(featuredEvent).length" class="mb-40">
          <h2>Featured Event</h2>
          <featured-event :event="featuredEvent" />
        </div>

        <h2>Events</h2>
        <tab-nav
          :tabs="eventsTabs"
          :active-tab="activeTab"
          @set-active-tab="setActiveTab"
        />
        <div class="events-wrap">
          <template v-if="activeTab === 'upcoming'">
            <div class="upcoming-events">
              <event-card
                v-for="event in displayedUpcomingEvents"
                :key="event.sys.id"
                :event="event"
              />
            </div>

            <div class="show-all-upcoming-events">
              <a
                v-if="
                  !isShowingAllUpcomingEvents &&
                    upcomingEvents.length != displayedUpcomingEvents.length
                "
                class="show-all-upcoming-events__btn"
                href="#"
                @click.prevent="isShowingAllUpcomingEvents = true"
              >
                Show All ({{ upcomingEvents.length }}) Upcoming Events
                <svg-icon name="icon-sort-desc" height="10" width="10" />
              </a>
            </div>
          </template>

          <template v-if="activeTab === 'past'">
            <div class="past-events">
              <event-card
                v-for="event in displayedPastEvents"
                :key="event.sys.id"
                :event="event"
              />
            </div>

            <div class="show-all-upcoming-events">
              <a
                v-if="
                  !isShowingAllPastEvents &&
                    pastEvents.length != displayedPastEvents.length
                "
                class="show-all-upcoming-events__btn"
                href="#"
                @click.prevent="isShowingAllPastEvents = true"
              >
                Show All ({{ pastEvents.length }}) Past Events
                <svg-icon name="icon-sort-desc" height="10" width="10" />
              </a>
            </div>
          </template>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { pathOr } from 'ramda'

import Breadcrumb from '@/components/Breadcrumb/Breadcrumb.vue'
import EventCard from '@/components/EventCard/EventCard'
import PageHero from '@/components/PageHero/PageHero.vue'
import TabNav from '@/components/TabNav/TabNav.vue'
import FeaturedEvent from '@/components/FeaturedEvent/FeaturedEvent.vue'

import createClient from '@/plugins/contentful.js'

const client = createClient()
const MAX_PAST_EVENTS = 8

/**
 * Get featured event from the News and Events page
 * @returns {Object}
 */
const getFeaturedEvent = async () => {
  try {
    const newsAndEventsPage = await client.getEntry(
      process.env.ctf_news_and_events_page_id
    )

    return pathOr({}, ['fields', 'featuredEvent'], newsAndEventsPage)
  } catch (error) {
    return {}
  }
}

/**
 * Get upcoming events
 * @param {Object} featuredEvent
 * @returns {Array}
 */
const getUpcomingEvents = async featuredEvent => {
  try {
    const todaysDate = new Date()
    return await client.getEntries({
      content_type: process.env.ctf_event_id,
      order: 'fields.startDate',
      'fields.startDate[gte]': todaysDate.toISOString(),
      'sys.id[nin]': pathOr(null, ['sys', 'id'], featuredEvent)
    })
  } catch (error) {
    return []
  }
}

/**
 * Get upcoming events
 * @returns {Array}
 */
const getPastEvents = async () => {
  try {
    const todaysDate = new Date()
    return await client.getEntries({
      content_type: process.env.ctf_event_id,
      order: 'fields.startDate',
      'fields.startDate[lt]': todaysDate.toISOString()
    })
  } catch (error) {
    return []
  }
}

const getEvents = async () => {
  try {
    const featuredEvent = await getFeaturedEvent()

    const upcomingEvents = await getUpcomingEvents(featuredEvent)

    const pastEvents = await getPastEvents()

    return {
      upcomingEvents: upcomingEvents.items,
      pastEvents: pastEvents.items,
      featuredEvent
    }
  } catch {
    return {
      upcomingEvents: [],
      pastEvents: [],
      featuredEvent: []
    }
  }
}

export default {
  name: 'EventsPage',

  components: {
    Breadcrumb,
    EventCard,
    PageHero,
    TabNav,
    FeaturedEvent
  },

  async asyncData() {
    const events = await getEvents()

    return {
      ...events
    }
  },

  data: function() {
    return {
      title: 'Events',
      breadcrumb: [
        {
          to: {
            name: 'index'
          },
          label: 'Home'
        },
        {
          to: {
            name: 'news-and-events'
          },
          label: 'News & Events'
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
      upcomingEvents: [],
      pastEvents: [],
      isShowingAllUpcomingEvents: false,
      isShowingAllPastEvents: false
    }
  },

  computed: {
    /**
     * Compute upcoming events
     * Used to display four events in the upcoming tab
     * @returns {Array}
     */
    displayedUpcomingEvents: function() {
      return this.isShowingAllUpcomingEvents
        ? this.upcomingEvents
        : this.upcomingEvents.slice(0, 4)
    },

    /**
     * Compute past events to display based on
     * current chunk value
     * @returns {Array}
     */
    displayedPastEvents: function() {
      return this.isShowingAllPastEvents
        ? this.pastEvents
        : this.pastEvents.slice(0, 4)
    }
  },

  watch: {
    '$route.query.tab': {
      handler(val) {
        if (val) {
          this.activeTab = val
        }
      },
      immediate: true
    }
  },

  methods: {
    /**
     * Set active tab by changing the router query param
     * @param {String} tab
     */
    setActiveTab(tab) {
      this.$router.push({
        query: { tab }
      })
    }
  }
}
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
.event-card {
  margin-bottom: 2em;
}

.upcoming-events,
.past-events {
  display: flex;
  flex-wrap: wrap;
  margin: 0 -1em;
}
.upcoming-event {
  margin: 0 1em 2em;
  @media (min-width: 48em) {
    width: calc(50% - 4.125em); // Account for the margins and the border
  }
  @media (min-width: 64em) {
    width: calc(25% - 4.125em); // Account for the margins and the border
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

.events-wrap {
  margin-bottom: 2.625em;
}
</style>
