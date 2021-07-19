<template>
  <div class="header">
    <div class="header__nav">
      <div class="header__nav--parent">
        <svg-icon icon="icon-about" width="18" height="18" />
        <nuxt-link :to="{ name: 'about' }">
          About SPARC
        </nuxt-link>
        <svg-icon icon="icon-contact" width="18" height="18" />
        <nuxt-link to="/contact-us">
          Contact Us
        </nuxt-link>
        <svg-icon icon="icon-help" width="18" height="18" />
        <nuxt-link :to="{ name: 'help' }">
          Need Help?
        </nuxt-link>
      </div>
      <div class="header__nav--main">
        <div class="nav-main-container">
          <button
            class="nav-main-container__mobile-menu"
            @click="openMobileNav"
          >
            <svg-icon icon="icon-hamburger" height="25" width="25" />
          </button>
          <div class="logo">
            <nuxt-link :to="{ name: 'index' }">
              <sparc-logo />
            </nuxt-link>
          </div>
          <button
            v-if="shouldShowSearch"
            class="nav-main-container__mobile-search"
            @click="openMobileSearch"
            @enter="executeSearch"
          >
            <svg-icon
              icon="icon-magnifying-glass"
              height="25"
              width="25"
              dir="left"
            />
          </button>
          <div :class="[searchOpen ? 'search-overlay' : '']">
            <div v-if="searchOpen" class="search-mobile">
              <input type="text" placeholder="Search Datasets" />
              <button class="search-mobile__close" @click="closeMobileSearch">
                <svg-icon
                  icon="icon-remove"
                  class="search-mobile__close--icon"
                />
              </button>
            </div>
          </div>

          <div :class="[menuOpen ? 'overlay' : '']">
            <div class="mobile-navigation" :class="[menuOpen ? 'open' : '']">
              <ul>
                <li
                  v-for="link in links"
                  :key="link.href"
                  style="z-index: 100;"
                >
                  <nuxt-link
                    :to="link.href"
                    :class="{ active: activeLink(link.href) }"
                    exact-active-class="active"
                  >
                    {{ link.displayTitle }}
                  </nuxt-link>
                </li>
                <hr class="divider" />
              </ul>
              <ul class="mobile-navigation__links">
                <li>
                  <svg-icon icon="icon-about" width="18" height="18" />
                  <nuxt-link :to="{ name: 'about' }">
                    About SPARC
                  </nuxt-link>
                </li>
                <li>
                  <svg-icon icon="icon-contact" width="18" height="18" />
                  <nuxt-link to="/contact-us">
                    Contact Us
                  </nuxt-link>
                </li>
                <li>
                  <svg-icon icon="icon-help" width="18" height="18" />
                  <nuxt-link :to="{ name: 'help' }">
                    Need Help?
                  </nuxt-link>
                </li>
              </ul>
              <div class="mobile-navigation__links--social">
                <a href="https://twitter.com/sparc_science" target="_blank">
                  <svg-icon
                    icon="icon-twitter"
                    width="30"
                    height="26"
                    color="#606266"
                  />
                </a>
                <a
                  href="https://www.youtube.com/results?search_query=sparc+nih"
                  target="_blank"
                >
                  <svg-icon
                    icon="icon-youtube"
                    width="30"
                    height="26"
                    color="#606266"
                  />
                </a>
              </div>
            </div>
          </div>
          <div v-if="shouldShowSearch" class="nav-main-container__search">
            <el-input
              v-model="searchQuery"
              type="text"
              class="nav-main-container__search-input"
              placeholder="Search"
              @keyup.native.enter="executeSearch"
            >
              <el-select slot="prepend" v-model="searchSelect">
                <el-option
                  v-for="option in searchSelectOptions"
                  :key="option.key"
                  :label="option.label"
                  :value="option.value"
                />
              </el-select>
            </el-input>
            <button
              class="nav-main-container__search-button"
              @click="executeSearch"
            >
              <svg-icon
                color="white"
                icon="icon-magnifying-glass"
                height="25"
                width="25"
                dir="left"
              />
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import SparcLogo from '../logo/SparcLogo.vue'
import { mapActions } from 'vuex'

const links = [
  {
    title: 'index',
    displayTitle: 'Home',
    href: '/'
  },
  {
    title: 'data',
    displayTitle: 'Find Data',
    href: '/data?type=dataset'
  },
  {
    title: 'resources',
    displayTitle: 'Tools & Resources',
    href: `/resources?type=${process.env.ctf_resource_id}`
  },
  {
    title: 'maps',
    displayTitle: 'Maps',
    href: '/maps'
  },
  {
    title: 'news-and-events',
    displayTitle: 'News & Events',
    href: '/news-and-events'
  },
  {
    title: 'sparclink',
    displayTitle: 'SPARClink',
    href: '/sparclink'
  }
]

export default {
  name: 'SparcHeader',
  components: {
    SparcLogo
  },
  data: () => ({
    links,
    menuOpen: false,
    searchOpen: false,
    searchQuery: '',
    searchSelect: 'data',
    searchSelectOptions: [
      {
        key: 'data',
        value: 'data',
        label: 'Datasets'
      },
      {
        key: 'resources',
        value: 'resources',
        label: 'Resources'
      },
      {
        key: 'news-and-events',
        value: 'news-and-events',
        label: 'News and Events'
      },
      {
        key: 'help',
        value: 'help',
        label: 'Support Center'
      }
    ]
  }),

  computed: {
    /**
     * Compute if search should be visible
     * @returns {Boolean}
     */
    shouldShowSearch: function() {
      return this.$route.name !== 'data'
    }
  },

  watch: {
    /**
     * Watches for the route path to hide
     * mobile nav on menu click
     **/
    '$nuxt.$route.path': {
      handler: function(val) {
        if (val) {
          this.menuOpen = false
        }
      },
      immediate: true
    },

    /**
     * Watches menuOpen to check if it's false
     * to enable scrolling
     */
    menuOpen: {
      handler: function(val) {
        if (!val) {
          this.$store.dispatch('updateDisabledScrolling', false)
        }
      },
      immediate: true
    }
  },

  methods: {
    ...mapActions({
      scrolling: 'updateDisabledScrolling'
    }),
    /**
     * Sets a link to active based on current page
     * @param {String} query
     */
    activeLink: function(query) {
      if (this.$nuxt.$route.path === query) {
        return true
      } else {
        return false
      }
    },
    /**
     * Opens the mobile version of the navigation
     */
    openMobileNav: function() {
      if (!this.menuOpen) {
        this.searchOpen = false // just in case the search menu is open also
        this.$store.dispatch('updateDisabledScrolling', true)
        this.menuOpen = true
      } else {
        this.menuOpen = false
        this.$store.dispatch('updateDisabledScrolling', false)
      }
    },

    /**
     * Opens the mobile version of the search bar
     */
    openMobileSearch: function() {
      this.searchOpen = true
      this.menuOpen = false
      this.$store.dispatch('updateDisabledScrolling', true)
    },

    /**
     * Closes the mobile version of the search bar
     */
    closeMobileSearch: function() {
      this.searchOpen = false
      this.$store.dispatch('updateDisabledScrolling', false)
    },

    /**
     * Executes a search query based on selected
     * option and query
     */
    executeSearch: function() {
      const option = this.searchSelectOptions.find(
        o => o.value === this.searchSelect
      )
      const searchKey = option.value === 'data' ? 'q' : 'search'
      const type =
        option.value === 'data'
          ? 'dataset'
          : option.value === 'resources'
          ? 'sparcPartners'
          : undefined

      this.$router.push({
        name: option.value,
        query: {
          type,
          [searchKey]: this.searchQuery
        }
      })

      this.searchQuery = ''
      this.searchSelect = 'data'
    }
  }
}
</script>

<style scoped lang="scss">
@import '@/assets/_variables.scss';

.nav {
  height: 4em;
  padding: 0;
  padding-top: 1rem;
}

.header {
  width: 100%;
  display: flex;
  flex-direction: row;
  @media (min-width: 320px) and (max-width: 1023px) {
    align-items: center;
  }
}
@media (min-width: 320px) and (max-width: 1023px) {
  .overlay {
    position: absolute;
    top: 56px;
    left: 0;
    width: 100%;
    height: 100%;
    z-index: 10;
    background-color: rgba(0, 0, 0, 0.5);
  }
}

@media (min-width: 320px) and (max-width: 1023px) {
  .search-overlay {
    position: absolute;
    top: 56px;
    left: 0;
    width: 100%;
    height: 100%;
    z-index: 10;
    background-color: rgba(0, 0, 0, 0.5);
  }
}

.divider {
  display: none;
  @media screen and (max-width: 1023px) {
    border: 0;
    clear: both;
    display: block;
    width: 89%;
    background-color: $pudendal;
    height: 1px;
    margin-left: 0;
    margin-top: 11px;
  }
}

.header__nav {
  background-color: $navy;
  width: 100%;
}

.header__nav--parent {
  display: flex;
  flex-direction: row;
  justify-content: flex-end;
  margin-top: 8px;
  margin-bottom: 8px;
  .svg-icon {
    color: $cochlear;
    padding-right: 0.4rem;
    padding-top: 0.2rem;
  }
  img {
    margin-right: 5px;
  }
  a {
    font-size: 13px;
    font-weight: 400;
    line-height: 24px;
    color: $cochlear;
    padding-right: 18px;
    text-decoration: none;
  }
  @media (min-width: 320px) and (max-width: 1023px) {
    & {
      display: none;
    }
  }
}

.header__nav--main {
  height: 82px;
  background-color: $cochlear;
  padding-top: 30px;
  padding-left: 33px;
  display: flex;
  flex-direction: row;
  @media (min-width: 320px) and (max-width: 1023px) {
    height: 41px;
    padding-left: 0;
    padding-top: 13px;
    .nav-main-container__mobile-menu {
      padding-left: 2px;
    }
  }

  .mobile-navigation__links {
    display: none;
    &--social {
      display: none;
    }
    @media (min-width: 320px) and (max-width: 1023px) {
      display: flex;
      flex-direction: column;
      a {
        font-size: 14px;
        font-weight: 300;
        line-height: 32px;
        margin-left: 0.5rem;
      }

      &--social {
        display: flex;
        flex-direction: row;
        margin-top: 15rem;
        .svg-icon {
          margin-right: 1rem;
        }
      }
    }
  }

  a {
    color: $app-secondary-color;
    font-size: 16px;
    line-height: 32px;
    font-weight: 500;
    padding-top: 5px;
    text-decoration: none;
  }
}

.nav-main-container__mobile-search {
  background: none;
  border: none;
  color: #000;
  display: flex;
  outline: none;
  padding-bottom: 1rem;
  &:hover:not(:active),
  &:focus:not(:active) {
    color: $app-primary-color;
  }
  @media (min-width: 64em) {
    display: none;
  }
}

.nav-main-container {
  display: flex;
  flex-direction: row;
  width: 100%;
  @media (min-width: 320px) and (max-width: 1023px) {
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    margin: 0;
    width: 100%;
  }
}

.logo {
  height: 62px;
  width: 127px;
  white-space: nowrap;
  margin-right: 48px;
  @media (min-width: 320px) and (max-width: 1023px) {
    height: 2rem;
    width: 100%;
    margin-right: 0;
    padding-top: 0.1rem;
  }
}

.nav-main-container__search {
  display: flex;
  flex-direction: row;
  justify-content: flex-end;
  width: 54%;
  margin-right: 1rem;
  @media (min-width: 320px) and (max-width: 1023px) {
    width: 0;
  }
}

.nav-main-container__search-input {
  width: 30vw;
  height: 34px;
  border-radius: 4px;
  border: solid 1px $dark-gray;
  @media screen and (max-width: 1023px) {
    display: none;
  }
  .el-select {
    width: 150px;
  }
  ::v-deep .el-input__inner {
    color: $medium-gray;
  }
}

.nav-main-container__search-button {
  background-color: $median;
  width: 40px;
  height: 40px;
  border-radius: 4px;
  margin-left: 9px;
  margin-top: 1px;
  border: none;
  @media screen and (max-width: 1023px) {
    display: none;
  }
}

::placeholder {
  /* Chrome, Firefox, Opera, Safari 10.1+ */
  color: #909399;
  opacity: 1; /* Firefox */
  font-size: 14px;
  font-weight: 300;
  line-height: 32px;
  padding-left: 7px;
}

:-ms-input-placeholder {
  /* Internet Explorer 10-11 */
  color: lightgray;
  font-size: 14px;
  font-weight: 300;
  line-height: 32px;
  padding-left: 7px;
}

.nav-main-container__mobile-menu {
  background: none;
  border: none;
  color: #000;
  display: none;
  font-size: 24px;
  margin: 0;
  outline: none;
  padding: 10px;
  transform: translate(12px, -8px);
  -webkit-appearance: none;

  &:hover:not(:active),
  &:focus:not(:active) {
    color: $app-primary-color;
  }

  @media screen and (max-width: 1023px) {
    & {
      display: block;
    }
  }
}

.mobile-navigation {
  padding: 0px;
  height: 100%;
  margin-left: 1rem;
  width: 120%;
  ul {
    padding-left: 0;
    margin-top: 0.5rem;
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    li {
      display: inline;
      padding-right: 5rem;
      @media screen and (min-width: 1023px) {
        padding-right: 0.5rem;
      }

      a {
        text-decoration: none;
        color: $navy;
        padding-bottom: 0.2rem;
        font-weight: 500;

        &.active,
        &:hover,
        &:focus {
          border-bottom: 2px solid $median;
          color: $median;
        }
      }
    }
  }

  @media (min-width: 320px) and (max-width: 1023px) {
    & {
      background: $seafoam;
      bottom: 0;
      display: none;
      flex-direction: column;
      left: 0;
      padding: 1em;
      position: fixed;
      right: 6rem;
      top: 3.4rem;
      z-index: 9999;
      &.open {
        display: flex;
        margin-left: 0;
        margin-right: 1rem;
        width: 70%;
        overflow: scroll;
      }
    }
    ul {
      display: flex;
      flex-direction: column;
      margin: 0;
      padding: 0;
      li {
        margin: 0.25rem 0;
      }
    }
  }
}

.search-mobile {
  display: none;
}

@media (min-width: 320px) and (max-width: 1023px) {
  .search-mobile {
    background-color: $cochlear;
    flex-direction: column;
    left: 0;
    padding: 1em;
    padding-top: 12px;
    padding-bottom: 14px;
    position: fixed;
    right: 6rem;
    top: 3.4rem;
    z-index: 9999;
    display: flex;
    width: 100%;
    height: 1.4rem;
    border-top: solid 1px lightgray;

    &__close {
      width: 27px;
      height: 30px;
      position: inherit;
      right: 0.8rem;
    }

    &--icon {
      color: $neutral-gray;
      width: 20px;
      height: 20px;
    }
  }

  input {
    height: 2rem;
    font-size: 16px;
    width: 90%;
  }

  ::placeholder {
    /* Chrome, Firefox, Opera, Safari 10.1+ */
    color: lightgrey;
    opacity: 1; /* Firefox */
    font-size: 16px;
    font-weight: 300;
    line-height: 32px;
    padding-left: 7px;
  }

  :-ms-input-placeholder {
    /* Internet Explorer 10-11 */
    color: lightgrey;
    font-size: 16px;
    font-weight: 300;
    line-height: 32px;
    padding-left: 7px;
  }
}

.data-portal-title {
  font-size: 14px;
  color: #303133;
  line-height: 14px;
  position: relative;
  bottom: 5px;
  margin-left: 5px;
  user-select: none;
}
</style>
