import marked from 'marked'

/**
 * Modify the link renderer to add `target="blank"`
 * https://github.com/markedjs/marked/pull/1371#issuecomment-434320596
 */
const renderer = new marked.Renderer()
const linkRenderer = renderer.link
const tableRenderer = renderer.table

export const isAnchor = str => {
  return /(?:^|\s)(#[^ ]+)/i.test(str)
}

/**
 * Compute if the link is an external link
 * @param {String} str
 * @returns {Boolean}
 */
export const isInternalLink = str => {
  return isAnchor(str)
    ? true
    : str.includes(process.env.ROOT_URL) || str.startsWith('/')
}

renderer.link = function(href, title, text) {
  const html = linkRenderer.call(renderer, href, title, text)
  const isInternal = isInternalLink(href)

  return isInternal
    ? html
    : html.replace(/^<a /, '<a target="_blank" rel="nofollow" ')
}

renderer.table = function(header, body) {
  const html = tableRenderer.call(renderer, header, body)

  return `<div class="markdown-table-wrap">${html}</div>`
}

renderer.oldImage = renderer.image

renderer.image = function(href, title, text) {
  const videos = ['webm', 'mp4', 'mov']
  const filetype = href.split('.').pop()
  if (videos.indexOf(filetype) > -1) {
    return `<video alt="${text}" controls><source src="${href}" type="video/${filetype}"></video>`
  } else {
    return renderer.oldImage(href, title, text)
  }
}

marked.setOptions({
  sanitize: true,
  renderer
})

export default {
  methods: {
    /**
     * Parse markdown
     * @param {String} markdown
     * @returns {HTML}
     */
    parseMarkdown: function(markdown = '') {
      return marked(markdown)
    }
  }
}
