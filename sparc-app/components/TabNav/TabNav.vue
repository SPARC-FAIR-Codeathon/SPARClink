<template>
  <div name="tabs">
    <ul class="tabs__container--types">
      <li v-for="tab in tabs" :key="tab.label">
        <a
          class="tabs__container--button"
          :class="{ active: tab.type === activeTab }"
          href="#"
          @click.prevent="$emit('set-active-tab', tab.type)"
        >
          {{ tab.label }}
        </a>
      </li>
    </ul>
  </div>
</template>

<script>
export default {
  name: 'DetailsTabs',
  props: {
    tabs: {
      type: Array,
      default: () => []
    },
    activeTab: {
      type: String,
      default: 'datasets'
    }
  }
}
</script>

<style lang="scss" scoped>
@import '../../assets/_variables.scss';
.tabs {
  &__container {
    &--types {
      border-bottom: 2px solid #dbdfe6;
      display: flex;
      list-style: none;
      margin: 0 0 1.5rem;
      padding: 0;
      li {
        margin: 0 2em;
        transform: translateY(2px);
        &:first-child {
          margin-left: 0;
        }
      }
    }

    &--button {
      background: none;
      border: none;
      color: $dark-sky;
      cursor: pointer;
      display: block;
      font-weight: normal;
      outline: none;
      padding: 0.5rem;
      text-decoration: none;
      &:hover,
      &:focus,
      &.active {
        color: $median;
        border-bottom: 2px solid $median;
      }
      &.active {
        font-weight: 500;
      }
    }
  }
}
</style>
