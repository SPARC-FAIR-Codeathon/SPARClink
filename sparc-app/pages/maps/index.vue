<template>
  <div class="maps">
    <breadcrumb :breadcrumb="breadcrumb" :title="title" />
    <page-hero>
      <h1>Maps</h1>
      <p>
        SPARC is creating a detailed PNS map based on SPARC data and information
        available from the literature. The map you see represents the current
        state of the SPARC connectivity database and is not comprehensive. New
        connectivity will be added as the SPARC program progresses.
      </p>
    </page-hero>
    <div ref="mappage" class="page-wrap portalmapcontainer">
      <client-only placeholder="Loading...">
        <div class="mapClass">
          <MapContent
            ref="map"
            :state="state"
            :api="api"
            :flatmap-a-p-i="flatmapAPI"
            :share-link="shareLink"
            @updateShareLinkRequested="updateUUID"
          />
        </div>
      </client-only>
    </div>
  </div>
</template>

<script>
import Breadcrumb from '@/components/Breadcrumb/Breadcrumb.vue'
import PageHero from '@/components/PageHero/PageHero.vue'
export default {
  name: 'MapsPage',
  components: {
    Breadcrumb,
    PageHero,
    MapContent: process.client
      ? () => import('@abi-software/mapintegratedvuer').then(m => m.MapContent)
      : null
  },
  async fetch() {
    if (this.uuid != this.$route.query.id) {
      this.uuid = this.$route.query.id
      if (this.uuid) {
        let url = this.api + `map/getstate`
        await fetch(url, {
          method: 'POST',
          headers: {
            'Content-type': 'application/json'
          },
          body: JSON.stringify({ uuid: this.uuid })
        })
          .then(response => response.json())
          .then(data => {
            this.state = data.state
          })
      }
    }
  },
  data() {
    return {
      resources: [],
      title: 'Maps',
      breadcrumb: [
        {
          to: {
            name: 'index'
          },
          label: 'Home'
        }
      ],
      uuid: undefined,
      state: undefined,
      api: process.env.portal_api,
      flatmapAPI: process.env.flatmap_api,
      shareLink: `${process.env.ROOT_URL}${this.$route.fullPath}`
    }
  },
  watch: {
    '$route.query': '$fetch'
  },
  fetchOnServer: false,
  created: function() {
    this.api = process.env.portal_api
    let lastChar = this.api.substr(-1)
    if (lastChar != '/') {
      this.api = this.api + '/'
    }
  },
  methods: {
    updateUUID: function() {
      let url = this.api + `map/getshareid`
      let state = this.$refs.map.getState()
      fetch(url, {
        method: 'POST',
        headers: {
          'Content-type': 'application/json'
        },
        body: JSON.stringify({ state: state })
      })
        .then(response => response.json())
        .then(data => {
          this.uuid = data.uuid
          this.$router.replace(
            { query: { ...this.$route.query, id: data.uuid } },
            () => {
              this.shareLink = `${process.env.ROOT_URL}${this.$route.fullPath}`
            }
          )
        })
    }
  }
}
</script>

<style lang="scss" scoped>
@import '@/assets/_variables.scss';
.maps {
  .page-hero__copy p {
    @media (min-width: 48em) {
      font-size: 0.9375rem;
      line-height: 1.5rem;
    }
  }

  .portalmapcontainer {
    margin-top: 1.5rem;
    height: 90vh;
    max-width: calc(100% - 48px);
    padding-left: 24px;
  }

  .page-wrap {
    &__results {
      font-size: 0.875em;
      font-weight: normal;
      line-height: 1em;

      @media screen and (max-width: 768px) {
        margin-left: 0.9375rem;
      }

      p {
        margin-top: 1.5rem;
      }
    }
    @media (min-width: 48em) {
      padding-top: 0;
    }
  }
}
</style>
<style lang="scss">
.mapClass {
  position: relative;
  width: 100%;
  height: 100%;
  border: solid 1px #dcdfe6;
  box-shadow: 0 1px 8px 0 rgba(0, 0, 0, 0.06);
  @import '~@abi-software/mapintegratedvuer/dist/mapintegratedvuer';
}
</style>
<style
  src="@abi-software/mapintegratedvuer/assets/mapicon-species-style.css"
></style>
