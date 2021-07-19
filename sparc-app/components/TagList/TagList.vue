<template>
  <ul class="tag-list unstyled">
    <li v-for="tag in tags" :key="tag">
      <span class="tag-list-tag">
        {{ tag }}
      </span>
    </li>
  </ul>
</template>

<script>
export default {
  name: 'TagList',

  props: {
    tags: {
      type: Array,
      default: () => []
    }
  }
}
</script>

<style lang="scss">
@import '@/assets/_variables.scss';
.tag-list {
  margin: 0;
  padding: 0;
  li {
    display: inline-block;
    margin: 0 8px 8px 0;
  }
}
.tag-list-tag {
  border-radius: 3px;
  border: solid 1px $cloudy;
  color: $dark-sky;
  display: block;
  font-size: 12px;
  font-weight: normal;
  line-height: 16px;
  padding: 8px;
  text-align: center;
  text-decoration: none;
  margin-top: 13px;
}
</style>
