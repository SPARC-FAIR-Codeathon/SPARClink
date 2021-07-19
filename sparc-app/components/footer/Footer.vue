<template>
  <div class="footer container">
    <el-row :gutter="32">
      <el-col :sm="{ span: 22, offset: 1 }" :md="{ span: 12, offset: 0 }">
        <div class="footer__info">
          <div class="footer__info--logo">
            <nuxt-link :to="{ name: 'index' }">
              <sparc-logo />
            </nuxt-link>
          </div>
          <div class="footer__info--blurb">
            <p>
              {{ footerData.copy }}
            </p>
          </div>
          <div class="footer__info--social">
            <a href="https://twitter.com/sparc_science" target="_blank">
              <svg-icon
                icon="icon-twitter"
                color="#606266"
                height="32px"
                width="32px"
              />
            </a>
            <a
              href="https://www.youtube.com/channel/UCCmUx4tOSlTAwlUrjSGz2mw"
              target="_blank"
            >
              <svg-icon
                icon="icon-youtube"
                color="#606266"
                height="32px"
                width="32px"
              />
            </a>
          </div>
        </div>
      </el-col>
      <el-col :sm="{ span: 22, offset: 1 }" :md="{ span: 8, offset: 4 }">
        <div class="footer__links">
          <el-row :gutter="32">
            <el-col :span="12">
              <h3>Learn More</h3>
              <ul>
                <li
                  v-for="learnMoreLink in footerData.learnMoreLinks"
                  :key="learnMoreLink.fields.url"
                >
                  <footer-link :link="learnMoreLink" />
                </li>
              </ul>
            </el-col>
            <el-col :span="12">
              <h3>Policies</h3>
              <ul>
                <li
                  v-for="policiesLink in footerData.policiesLinks"
                  :key="policiesLink.fields.url"
                >
                  <footer-link :link="policiesLink" />
                </li>
              </ul>
            </el-col>
          </el-row>
          <el-row :gutter="32">
            <el-col :span="12">
              <h3>Help Us Improve</h3>
              <ul>
                <li
                  v-for="helpUsImproveLink in footerData.helpUsImproveLinks"
                  :key="helpUsImproveLink.fields.url"
                >
                  <footer-link :link="helpUsImproveLink" />
                </li>
              </ul>
            </el-col>
            <el-col :span="12">
              <h3>Stay Up-to-Date</h3>
              <ul>
                <li
                  v-for="stayUpdatedLink in footerData.stayUpdatedLinks"
                  :key="stayUpdatedLink.fields.url"
                >
                  <footer-link :link="stayUpdatedLink" />
                </li>
              </ul>
            </el-col>
          </el-row>
        </div>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import { mapState } from 'vuex'

import FooterLink from './FooterLink.vue'
import SparcLogo from '@/components/logo/SparcLogo.vue'

export default {
  name: 'SparcFooter',
  components: {
    FooterLink,
    SparcLogo
  },

  computed: {
    ...mapState(['footerData'])
  }
}
</script>

<style scoped lang="scss">
@import '@/assets/_variables.scss';

.footer {
  display: flex;
  flex-direction: row;
  padding: 3rem 1rem;

  &__info {
    &--logo {
      height: 4rem;
      margin-bottom: 1.5rem;
    }

    &--blurb {
      margin-bottom: 3rem;
      p {
        font-size: 1rem;
        font-weight: normal;
        line-height: 2rem;
        color: $dark-gray;
      }
    }

    &--social {
      margin-bottom: 3rem;
      .svg-icon {
        width: 2.2rem;
        margin-right: 1rem;
      }
    }
  }

  &__links {
    h3 {
      font-size: 1rem;
      font-weight: bold;
      line-height: 2rem;
      color: $dark-gray;
    }
    ul {
      list-style: none;
      padding-left: 0;

      li {
        padding-bottom: 1rem;
      }

      a {
        color: $dark-gray;
        text-decoration: none;
        &:hover {
          text-decoration: underline;
        }
      }
    }
  }
}

@media screen and (max-width: 1023px) {
  .footer {
    &__info {
      &--logo {
        height: 2rem;
      }

      &--blurb {
        font-size: 0.75rem;
        font-weight: normal;
        line-height: 1.25rem;

        p {
          margin-bottom: 1rem;
        }
      }
    }
  }
}
</style>
