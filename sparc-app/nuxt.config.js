export default {
  /*
   ** Headers of the page
   */
  head: {
    title: 'SPARC Portal' || '',
    meta: [
      { charset: 'utf-8' },
      { name: 'viewport', content: 'width=device-width, initial-scale=1' },
      {
        hid: 'description',
        name: 'description',
        content: process.env.npm_package_description || ''
      }
    ],
    link: [
      {
        rel: 'icon',
        type: 'image/x-icon',
        href: '/favicon/favicon.ico'
      },
      {
        rel: 'stylesheet',
        href:
          'https://fonts.googleapis.com/css?family=Asap:400,400i,500,600,700&display=swap'
      }
    ]
  },
  env: {
    portal_api: process.env.PORTAL_API_HOST || 'http://localhost:8000',
    flatmap_api:
      process.env.FLATMAP_API_HOST || 'https://mapcore-demo.org/flatmaps/',
    crosscite_api_host:
      process.env.CROSSCITE_API_HOST || 'https://citation.crosscite.org',
    discover_api_host:
      process.env.BLACKFYNN_DISCOVER_API_HOST ||
      'https://api.pennsieve.io/discover',
    bf_api_host: process.env.BF_API_HOST || 'https://api.pennsieve.io',
    zipit_api_host:
      process.env.ZIPIT_API_HOST || 'https://api.pennsieve.io/zipit/discover',
    osparc_host: process.env.OSPARC_HOST || 'https://osparc.io',
    ctf_event_id: 'event',
    ctf_news_id: 'news',
    ctf_resource_id: 'sparcPartners',
    ctf_resource_hero_id: '3ImGx7UyDXPwM3oTag06nt',
    ctf_help_id: 'helpDocument',
    ctf_help_list_id: 'helpSection',
    ctf_help_aws_id: 'zQfzadwADutviJjT19hA5',
    ctf_about_page_id: '4VOSvJtgtFv1PS2lklMcnS',
    ctf_contact_us_page_id: '7t2GZ5F74AdNRqBau4mp8S',
    ctf_support_page_id: '59F0dM5goobqjw3TsqINRw',
    ctf_home_page_id: '4qJ9WUWXg09FAUvCnbGxBY',
    ctf_news_and_events_page_id: '4IoMamTLRlN3OpxT1zgnU',
    ctf_dataset_navigation_info_page_id: 'qvEcnv56c76V0JC0KvtSd',
    ctf_dataset_format_info_page_id: '3FXikFXC8shPRd8xZqhjVT',
    ctf_project_id: 'sparcAward',
    ctf_organ_id: 'organ',
    ctf_filter_id: '6bya4tyw8399',
    ctf_filters_dataset_id: '7fL88ABgKSB2tPJmysn2V',
    ctf_filters_project_id: 'YVan5NSd4bgj2Q5WZdOVw',
    ctf_filters_organ_id: '5Hhlb7Lf4yijMQUSBai1fh',
    ctf_filters_image_id: '4R4zfdND13xLLGU9nPpNCD',
    ctf_filters_simulation_id: '6qMQRugMyzeaUrTIPQDdF1',
    ctf_footer_copy_id: 'wpik0A2sDOy9IQEoKpkKG',
    ctf_terms_id: '6XCER8v1TVVCoZdaBWg66t',
    ctf_privacy_policy_id: '2p44GCn1rrWUETwTRF2ElS',
    ctf_success_story_id: 'successStory',
    CTF_SPACE_ID: process.env.CTF_SPACE_ID,
    CTF_CDA_ACCESS_TOKEN: process.env.CTF_CDA_ACCESS_TOKEN,
    CTF_API_HOST: process.env.CTF_API_HOST,
    ALGOLIA_API_KEY: process.env.ALGOLIA_API_KEY,
    ALGOLIA_APP_ID: process.env.ALGOLIA_APP_ID,
    BL_SERVER_URL: 'https://sparc.biolucida.net/api/v1/',
    BL_SHARE_LINK_PREFIX: 'https://sparc.biolucida.net/image?c=',
    ROOT_URL: process.env.ROOT_URL || 'http://localhost:3000',
    max_download_size: parseInt(process.env.MAX_DOWNLOAD_SIZE || '5000000000')
  },

  serverMiddleware: [
    // Will register redirect-ssl npm package
    'redirect-ssl'
  ],

  /*
   ** Customize the progress-bar color
   */
  loading: { color: '#fff' },

  /*
   ** Customize router classes globally
   */
  router: {
    linkActiveClass: 'active-link',
    extendRoutes(routes) {
      // Redirects
      routes.push({
        path: '/submit_data.html',
        redirect: '/help/7k8nEPuw3FjOq2HuS8OVsd'
      })
      routes.push({
        name: 'version',
        path: '/datasets/:datasetId/version/:version',
        component: '@/pages/datasets/_datasetId.vue'
      })
    }
  },
  /*
   ** Global CSS
   */
  css: ['element-ui/lib/theme-chalk/index.css'],
  /*
   ** Plugins to load before mounting the App
   */
  plugins: ['@/plugins/bootstrap', '@/plugins/contentful'],
  /*
   ** Nuxt.js dev-modules
   */
  buildModules: [
    '@nuxt/typescript-build',
    [
      '@nuxtjs/google-analytics',
      {
        id: 'UA-143804703-1'
      }
    ]
  ],
  /*
   ** Nuxt.js modules
   */
  modules: [
    '@nuxtjs/axios',
    '@nuxtjs/robots',
    'cookie-universal-nuxt',
    '@miyaoka/nuxt-twitter-widgets-module',
    'vue-social-sharing/nuxt'
  ],
  /*
   ** robots.txt
   */
  robots: [
    {
      // all environment
      UserAgent: '*',

      // disallow all in all environments except production
      Disallow: () => (process.env.DEPLOY_ENV !== 'production' ? '/' : [])
    }
  ],
  /*
   ** Build configuration
   */
  build: {
    transpile: [/^element-ui/],

    /*
     ** You can extend webpack config here
     */
    extend(config, ctx) {
      if (ctx.isDev) {
        config.devtool = ctx.isClient ? 'source-map' : 'inline-source-map'
      }
    }
  }
}
