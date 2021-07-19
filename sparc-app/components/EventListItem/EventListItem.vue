<template>
  <div class="event-list-item">
    <div class="event-content">
      <div class="image">
        <event-banner-image :src="bannerUrl" />
      </div>
      <div class="event-content-wrap">
        <h3>
          <a :href="event.fields.url" target="_blank">
            {{ event.fields.title }}
          </a>
        </h3>
        <div class="subtitle">
          <div>{{ event.fields.location }}</div>
        </div>
        <div class="details">
          <div class="detail">
            {{ event.fields.summary }}
          </div>
          <div class="detail eventinfo">
            {{ event.fields.eventType }} - SPARC Attendees:
            {{ event.fields.sparcAttendees }}
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { format, parseISO } from 'date-fns'
import { pathOr } from 'ramda'
import eventBannerImage from '@/components/EventBannerImage/EventBannerImage.vue'
import FormatDate from '@/mixins/format-date'

export default {
  name: 'EventCard',
  components: {
    eventBannerImage
  },
  mixins: [FormatDate],
  props: {
    event: {
      type: Object,
      default: () => {
        return {
          banner: '',
          description: '',
          name: '',
          image: {
            fields: {
              file: {
                url: ''
              }
            }
          }
        }
      }
    }
  },
  computed: {
    /**
     * Compute banner URL
     * @returns {String}
     */
    bannerUrl: function() {
      return pathOr(
        '',
        ['fields', 'image', 'fields', 'file', 'url'],
        this.event
      )
    },

    /**
     * Compute and formate start date
     * @returns {String}
     */
    startDate: function() {
      return format(parseISO(this.event.fields.startDate), 'MM/dd/yyyy')
    },

    /**
     * Compute and formate end date
     * @returns {String}
     */
    endDate: function() {
      return format(parseISO(this.event.fields.endDate), 'MM/dd/yyyy')
    }
  },
  methods: {}
}
</script>

<style lang="scss" scoped>
@import '@/assets/_variables.scss';
.event-list-item {
  border-radius: 3px 3px 0 0;
  background-color: white;
  margin-bottom: 5px;
}
h3 {
  color: $vagus;
  font-size: 18px;
  font-weight: 600;
  line-height: 1.2;
  word-break: break-word;
}
.subtitle {
  color: #000;
  font-size: 14px;
  font-weight: normal;
  line-height: 24px;
  margin-bottom: 16px;
}
.details {
  margin-top: 16px;
  display: flex;
  justify-content: flex-start;
  flex-wrap: wrap;
  .detail {
    align-items: center;
    display: flex;
    padding-right: 24px;
    color: #404554;
    font-size: 14px;
    font-weight: 400;
    letter-spacing: 0px;
    line-height: 16px;
    margin-bottom: 8px;
    .svg-icon {
      margin-right: 8px;
    }
    .eventinfo {
      margin-top: 8px;
    }
  }
}
.event-content {
  display: flex;
  flex-direction: row;
  img {
    display: block;
    width: 86px;
    height: 86px;
  }

  .image {
    margin: 2px;
  }

  .event-content-wrap {
    margin-left: 16px;
  }
}
.meta {
  border-top: solid 1px $pudendal;
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  padding: 8px 16px;
  .author {
    font-size: 12px;
    line-height: 14px;
  }
  .tags {
    font-size: 12px;
    line-height: 14px;
  }
}
a {
  &:focus {
    color: $vagus;
  }
}
</style>
