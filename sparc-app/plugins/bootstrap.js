import Vue from 'vue'
import Element from 'element-ui'
import locale from 'element-ui/lib/locale/lang/en'

Vue.use(Element, { locale })
Vue.config.devtools = true

import { Message } from 'element-ui'
import '@/assets/element-variables.scss'
import * as svgicon from 'vue-svgicon'
import '@/static/icons-js'
import VueClipboard from 'vue-clipboard2'
// // import '@/assets/icons'
// // import SocialSharing from 'vue-social-sharing'

import striptags from 'striptags'
Vue.prototype.$sanitize = (html, allowedTags = ['br']) =>
  striptags(html, allowedTags)

// // configure language
// locale.use(lang)
Vue.config.productionTip = false

Vue.use(VueClipboard)
// Vue.use(Dialog)
// Vue.use(Spinner)
// Vue.use(Loading)
// Vue.use(Tooltip)
// // Vue.use(SocialSharing)
Vue.use(svgicon, {
  tagName: 'svg-icon'
})

Vue.prototype.$message = Message
