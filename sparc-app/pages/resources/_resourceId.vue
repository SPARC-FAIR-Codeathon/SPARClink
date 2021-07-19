<template>
  <div class="resources">
    <news-events-page
      :page="resource"
      :content="resource.fields.longDescription"
      :breadcrumb="breadcrumb"
      :hero-title="resource.fields.name"
      :hero-summary="resource.fields.description"
      type="news"
    >
      <template v-if="resourceLogoUrl">
        <img :src="resourceLogoUrl" :alt="resourceLogoAlt" />
        <hr />
      </template>

      <div class="mb-8">
        <h3>Tool / Resource Name</h3>
        <p class="mb-0">
          {{ resource.fields.name }}
        </p>
        <span v-if="resource.fields.developedBySparc" class="resource-category">
          SPARC
        </span>
      </div>
      <h3>URL</h3>
      <p>
        <a :href="resource.fields.url" target="_blank">
          {{ resource.fields.url }}
        </a>
      </p>
    </news-events-page>

    <!-- <page-hero>
      <h2>{{ resource.fields.name }}</h2>
    </page-hero>
    <div class="page-wrap container">
      <div class="subpage">
        <el-row type="flex" justify="center">
          <el-col :row="24">
            <div class="resource">
              <img :src="resourceLogoUrl" :alt="resourceLogoAlt" />
              <div class="resource__content">
                <p>
                  {{ resource.fields.description }}
                </p>
                <a :href="resource.fields.url" target="_blank">
                  <bf-button>
                    Visit Website
                  </bf-button>
                </a>
              </div>
            </div>
          </el-col>
        </el-row>
      </div>
    </div> -->
  </div>
</template>

<script>
import { pathOr } from 'ramda'

import NewsEventsPage from '@/components/NewsEventsPage/NewsEventsPage'

import createClient from '@/plugins/contentful.js'

const client = createClient()

export default {
  name: 'Resources',

  components: {
    NewsEventsPage
  },

  asyncData(ctx) {
    return Promise.all([client.getEntry(ctx.route.params.resourceId)])
      .then(([resource]) => {
        return {
          resource
        }
      })
      .catch(console.error)
  },

  data() {
    return {
      resource: {},
      breadcrumb: [
        {
          label: 'Home',
          to: {
            name: 'index'
          }
        },
        {
          label: 'Tools & Resources',
          to: {
            name: 'resources'
          }
        }
      ]
    }
  },

  computed: {
    /**
     * Compute the URL for the resource's logo
     * @returns {String}
     */
    resourceLogoUrl: function() {
      return pathOr(
        '',
        ['fields', 'logo', 'fields', 'file', 'url'],
        this.resource
      )
    },
    /**
     * Compute the alt tag for the resource's logo
     * @returns {String}
     */
    resourceLogoAlt: function() {
      return pathOr('', ['fields', 'logo', 'fields', 'title'], this.resource)
    }
  }
}
</script>

<style lang="scss" scoped>
@import '../../assets/_variables.scss';

.resource-category {
  background: $median;
  border-radius: 15px;
  color: #fff;
  display: block;
  font-size: 0.875rem;
  top: 10px;
  padding: 0 0.65rem;
  right: 14px;
  width: fit-content;
  margin-bottom: 10px;
}
</style>
