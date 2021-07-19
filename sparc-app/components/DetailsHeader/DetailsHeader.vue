<template>
  <div class="details-header">
    <breadcrumb :breadcrumb="breadcrumb" :title="title" />
    <div class="container">
      <div class="details-header__container">
        <div class="details-header__container--image">
          <slot name="banner image" />
        </div>
        <div class="details-header__container--content">
          <h3>
            {{ subtitle }}
          </h3>
          <h2 class="details-header__container--content-title-default">
            {{ formatTitle(title) }}
          </h2>
          <h2 class="details-header__container--content-title-mobile">
            {{ formatMobileTitle(title) }}
          </h2>
          <p class="details-header__container--content-description-default">
            {{ fullDescription ? description : formatDescription(description) }}
          </p>
          <p class="details-header__container--content-description-mobile">
            {{
              fullDescription
                ? description
                : formatMobileDescription(description)
            }}
          </p>
          <slot name="meta content" />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import Breadcrumb from '@/components/Breadcrumb/Breadcrumb'
export default {
  name: 'DetailsHeader',

  components: {
    Breadcrumb
  },

  props: {
    breadcrumb: {
      type: Array,
      default: () => []
    },
    subtitle: {
      type: String,
      default: ''
    },
    title: {
      type: String,
      default: ''
    },
    description: {
      type: String,
      default: ''
    },
    fullDescription: {
      type: Boolean,
      default: false
    }
  },

  methods: {
    /**
     * Formats title length for regular viewports
     * @param {String} title
     */
    formatTitle: function(title) {
      return title.length > 150 ? title.substring(0, 150) + '...' : title
    },

    /**
     * Formats title length for mobile viewports
     * @param {String} title
     */
    formatMobileTitle: function(title) {
      return title.length > 90 ? title.substring(0, 90) + '...' : title
    },

    /**
     * Formats description based on length for regular viewports
     * @param {String} description
     */
    formatDescription: function(description) {
      return description.length > 540
        ? description.substring(0, 540) + '...'
        : description
    },

    /**
     * Formats description based on length for mobile viewports
     * @param {String}
     */
    formatMobileDescription: function(description) {
      return description.length > 260
        ? description.substring(0, 260) + '...'
        : description
    }
  }
}
</script>

<style lang="scss" scoped>
@import '../../assets/_variables.scss';
.details-header {
  &__container {
    display: flex;
    flex-direction: row;
    border: solid 1px $cloudy;
    padding: 2rem;
    background: white;
    margin: 1.25rem 0 2rem;
    &--image {
      flex-shrink: 0;
      margin-right: 1rem;
      width: 100%;
      @media (min-width: 48em) {
        height: 368px;
        width: 368px;
      }
      .dataset-image {
        border: solid 1px $cloudy;
      }
      img {
        display: block;
        width: 100%;
        height: auto;
      }
    }
    &--content {
      h3 {
        text-transform: uppercase;
        font-weight: 500;
        line-height: 24px;
        font-size: 14px;
        color: $medium-gray;
      }
    }
    &--content-title-default {
      font-weight: 500;
      font-size: 24px;
      line-height: 32px;
    }
    &--content-title-mobile {
      display: none;
    }
    &--content-description-default {
      font-size: 14px;
      font-weight: normal;
      line-height: 24px;
      margin-bottom: 5rem;
    }
    &--content-description-mobile {
      display: none;
    }
    &--content-meta {
      display: flex;
      flex-direction: row;
      align-items: flex-start;
    }

    &--content-links {
      a {
        font-size: 12px;
        color: $median;
        font-weight: bold;
        line-height: 24px;
        margin-left: 1rem;
      }
      button {
        background: $median;
        height: 2.5rem;
        width: 12rem;
        border-radius: 4px;
        a {
          color: white;
          font-size: 14px;
          font-weight: 500;
          text-transform: uppercase;
          text-decoration: none;
          margin-left: 0;
        }
      }
    }
    .content-meta__item {
      margin-right: 5.3rem;
      h3 {
        color: black;
        margin-bottom: -4rem;
      }
      p {
        padding-top: 3rem;
        margin-top: 0.5rem;
      }
    }
  }
}

@media screen and (max-width: 768px) {
  .details-header {
    margin: 0;
    margin-top: 0;
    &__page-route {
      height: 100%;
      p {
        padding-bottom: 0.75rem;
      }
    }
    &__container {
      flex-direction: column;
      &--content-description-default {
        display: none;
      }
      &--content-description-mobile {
        display: block;
      }
      &--content-title-default {
        display: none;
      }
      &--content-title-mobile {
        display: block;
      }
      &--content-meta {
        flex-direction: column;
      }
    }
  }
}

@media screen and (max-width: 360px) {
  .details-header {
    &__container {
      &--image {
        img {
          width: 288px;
          height: 288px;
          margin-left: 1rem;
        }
      }
    }
  }
}

@media screen and (max-width: 320px) {
  .details-header {
    &__container {
      &--image {
        img {
          margin-left: 0;
        }
      }
    }
  }
}
</style>
