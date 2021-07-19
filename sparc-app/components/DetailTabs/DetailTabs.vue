<template>
  <div name="details-tabs">
    <div class="details-tabs__container">
      <el-row type="flex">
        <el-col :span="24">
          <ul class="details-tabs__container--types">
            <li v-for="tab in tabs" :key="tab.label">
              <nuxt-link
                class="details-tabs__container--button"
                :class="{ active: tab.type === activeTab }"
                :to="{ query: queryParams(tab.type) }"
              >
                {{ tab.label }}
              </nuxt-link>
            </li>
          </ul>
        </el-col>
      </el-row>
      <div class="details-tabs__container--data">
        <slot />
      </div>
    </div>
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
      default: ''
    },
    defaultTab: {
      type: String,
      default: ''
    }
  },
  methods: {
    queryParams(tabType) {
      const query = { ...this.$route.query }
      if (tabType === this.defaultTab && 'tab' in query) {
        delete query.tab
      } else if (tabType !== this.defaultTab) {
        query['tab'] = tabType
      }

      return query
    }
  }
}
</script>

<style lang="scss" scoped>
@import '../../assets/_variables.scss';
.details-tabs {
  margin: 1.25rem;
  &__container {
    background: white;
    border: solid 1px $cloudy;
    padding: 2em;

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
      font-size: 1.375em;
      font-weight: normal;
      outline: none;
      padding: 0.5rem;
      text-decoration: none;
      border-bottom: 2px solid transparent;
      &:hover,
      &.active {
        color: $median;
        border-bottom: 2px solid $median;
      }
    }

    &--data {
      h3 {
        font-size: 14px;
        font-weight: 500;
        line-height: 16px;
      }
      p {
        font-size: 14px;
        font-weight: normal;
        line-height: 24px;
        margin-top: 0;
      }
      ul {
        list-style: none;
        padding-left: 0;
        margin-top: 0;
        li {
          font-size: 14px;
          font-weight: normal;
          line-height: 24px;
        }
      }
    }
  }
}
@media screen and (max-width: 768px) {
  .details-tabs {
    &__container {
      margin-top: 1.5rem;
      padding-right: 1rem;
      padding-left: 1rem;
      &--types {
        display: -webkit-box;
        width: max-content;
      }
      &--button {
        font-size: 1em;
        padding-right: 0;
        padding-left: 0;
      }
      li {
        margin-right: 0;
      }
    }
  }

  ::v-deep .el-row--flex {
    overflow-y: scroll;
  }
}

@media screen and (max-width: 1024px) {
  .details-tabs {
    &__container {
      &--types {
        width: 100%;
      }
    }
  }
}
</style>
