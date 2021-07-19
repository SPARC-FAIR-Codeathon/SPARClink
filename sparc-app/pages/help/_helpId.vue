<template>
  <div class="events-page">
    <breadcrumb :breadcrumb="breadcrumb" :title="helpItem.fields.title" />
    <help-hero :title="helpHeroData.title" :summary="helpHeroData.summary" />
    <div class="page-wrap container">
      <div class="subpage">
        <div class="header">
          <h2>{{ helpItem.fields.title }}</h2>
          <div class="summary">
            {{ helpItem.fields.summary }}
          </div>
          <div class="updated">
            <i>Updated at: {{ updateDate }} </i>
          </div>
        </div>
        <!-- eslint-disable vue/no-v-html -->
        <!-- marked will sanitize the HTML injected -->
        <div class="content" v-html="parseMarkdown(htmlContent)" />
      </div>
    </div>
  </div>
</template>

<script>
import { format, parseISO } from 'date-fns'
import { pathOr } from 'ramda'

import HelpHero from '@/components/HelpHero/HelpHero'
import MarkedMixin from '@/mixins/marked'
import Breadcrumb from '../../components/Breadcrumb/Breadcrumb'

import createClient from '@/plugins/contentful.js'

const client = createClient()

const getHelpItem = async id => {
  try {
    const isSlug = id.split('-').length > 1

    const item = isSlug
      ? await client.getEntries({
          content_type: process.env.ctf_help_id,
          'fields.slug': id
        })
      : await client.getEntry(id)
    return isSlug ? item.items[0] : item
  } catch (error) {
    return {}
  }
}

export default {
  name: 'EventPage',

  components: {
    HelpHero,
    Breadcrumb
  },

  mixins: [MarkedMixin],

  async asyncData({ params, redirect }) {
    const helpItem = await getHelpItem(params.helpId)

    // Redirect to the friendly URL page, if this page has a slug
    const slug = helpItem.fields.slug
    if (slug && params.helpId !== slug) {
      redirect({
        name: 'help-helpId',
        params: { helpId: slug }
      })
    }

    const allHelpData = await client.getEntry(process.env.ctf_support_page_id, {
      include: 2
    })

    return {
      helpHeroData: allHelpData.fields,
      helpItem: helpItem,
      breadcrumb: [
        {
          label: 'Home',
          to: {
            name: 'index'
          }
        },
        {
          label: allHelpData.fields.title,
          to: {
            name: 'help'
          }
        }
      ]
    }
  },

  computed: {
    /**
     * Compute HTML Content for the page
     * @returns {String}
     */
    htmlContent() {
      return pathOr('', ['fields', 'helpContent'], this.helpItem)
    },

    /**
     * Compute and convert the date the article was created
     * @returns {String}
     */
    updateDate: function() {
      return format(parseISO(this.helpItem.sys.updatedAt), 'MM/dd/yyyy')
    }
  }
}
</script>

<style lang="scss" scoped>
@import '@/assets/_variables.scss';

.content {
  & ::v-deep {
    color: $vestibular;
  }
  & ::v-deep p {
    margin-bottom: 1em;
  }
  & ::v-deep img {
    height: auto;
    margin: 0.5em 0;
    max-width: 100%;
  }
}

.header {
  margin-bottom: 3em;
  .updated {
    color: #aaa;
  }
}
</style>
