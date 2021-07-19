<template>
  <div class="about-page">
    <breadcrumb :breadcrumb="breadcrumb" :title="pageTitle" />
    <page-hero v-if="heroCopy">
      <h1>{{ pageTitle }}</h1>
      <!-- eslint-disable vue/no-v-html -->
      <!-- marked will sanitize the HTML injected -->
      <div v-html="parseMarkdown(heroCopy)" />
    </page-hero>
    <div class="page-wrap container">
      <div class="subpage">
        <div class="row">
          <div class="col">
            <div class="about-page-text" v-html="parseMarkdown(overview)" />
          </div>
          <div class="col">
            <!-- <img src="https://via.placeholder.com/222" /> -->
          </div>
        </div>
      </div>

      <div class="subpage">
        <div class="row">
          <div class="col">
            <!-- <img class="about-page-portal-img" src="https://via.placeholder.com/222" /> -->
          </div>
          <div class="subpage-col">
            <div class="about-page-text" v-html="parseMarkdown(sparcPortal)" />
            <!-- <img class="about-page-portal-img-mobile" src="https://via.placeholder.com/222" /> -->
            <button class="about-teams-and-projects-button">
              <nuxt-link
                :to="{
                  name: 'data',
                  query: {
                    type: projectId
                  }
                }"
              >
                View Teams & Projects
              </nuxt-link>
            </button>
          </div>
        </div>
      </div>

      <div v-if="futurePlans" class="subpage">
        <div class="row">
          <div class="subpage-col">
            <div class="about-page-text" v-html="parseMarkdown(futurePlans)" />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import Breadcrumb from '@/components/Breadcrumb/Breadcrumb.vue'
import PageHero from '@/components/PageHero/PageHero.vue'

import MarkedMixin from '@/mixins/marked'
import createClient from '@/plugins/contentful.js'

const client = createClient()

export default {
  name: 'AboutPage',

  components: {
    Breadcrumb,
    PageHero
  },

  mixins: [MarkedMixin],

  asyncData() {
    return Promise.all([
      // Get page content
      client.getEntry(process.env.ctf_about_page_id)
    ])
      .then(([page]) => {
        return { ...page.fields }
      })
      .catch(console.error)
  },

  data: () => {
    return {
      heroCopy: '',
      copy: '',
      breadcrumb: [
        {
          to: {
            name: 'index'
          },
          label: 'Home'
        }
      ],
      projectId: process.env.ctf_project_id,
      heroImage: {},
      futurePlans: ''
    }
  }
}
</script>

<style scoped lang="scss">
@import '@/assets/_variables.scss';
.page {
  display: flex;
  margin-top: 7rem;

  p {
    color: #606266;
  }
}

.subpage {
  .subpage-col {
    @media screen and (max-width: 767px) {
      margin-top: 0;
    }
    .about-page-text {
      @media screen and (max-width: 767px) {
        margin-left: 0;
      }
    }

    .about-page-portal-img-mobile {
      display: none;
      @media screen and (max-width: 767px) {
        display: block;
        margin-bottom: 1.25rem;
      }
    }
  }

  @media screen and (max-width: 767px) {
    .about-page-portal-img {
      display: none;
    }
  }

  .row {
    display: flex;
    @media screen and (max-width: 767px) {
      flex-direction: column;
    }
  }
}

.about-page-link {
  color: white;
  text-decoration: underline;
  &:hover {
    color: #909399;
  }
}

.about-page-button {
  width: 12.3rem;
  height: 2.5rem;
  border-radius: 0.25em;
  margin-top: 1rem;
  background: #fff;
  a {
    font-size: 1.25em;
    font-weight: 500;
    letter-spacing: 0;
    text-transform: uppercase;
    color: $median;
    text-decoration: none;
  }
}

.about-teams-and-projects-button {
  background: $median;
  text-transform: uppercase;
  height: 2.5rem;
  width: 12.4rem;
  border-radius: 4px;
  font-size: 0.875em;
  font-weight: 500;
  a {
    text-decoration: none;
    color: #fff;
  }
  @media screen and (max-width: 767px) {
    margin-left: 0;
  }
}

.about {
  text-align: center;
  min-height: 50vh;
  margin-top: 9rem;
}
</style>
