<template>
  <div class="subpage">
    <div v-for="(item, index) in stories" :key="index">
      <community-spotlight-item :story="item" />
      <div v-if="index !== stories.length - 1 || inNews" class="seperator-path" />
    </div>
    <nuxt-link
      v-if="inNews"
      class="community-link mt-16"
      :to="{
        name: 'news-and-events-community-spotlight'
      }"
    >
      View All Community Spotlights &gt;
    </nuxt-link>
  </div>
</template>

<script>
import CommunitySpotlightItem from './CommunitySpotlightItem.vue'

export default {
  name: 'CommunitySpotlightListings',
  components: {
    CommunitySpotlightItem
  },
  props: {
    stories: {
      type: Array,
      default: () => []
    },
    inNews: {
      type: Boolean,
      default: false
    }
  }
}
</script>

<style lang="scss" scoped>
@import '@/assets/_variables.scss';

.seperator-path {
  width: 100%;
  height: 2px;
  background: rgb(216, 216, 216);
  border-radius: 0px;
  margin-bottom: 32px;
  margin-top: 32px;
}

.subpage {
  margin-bottom: 20px;
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
