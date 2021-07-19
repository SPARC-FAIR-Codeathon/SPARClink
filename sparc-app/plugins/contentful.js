// ./plugins/contentful.js

const contentful = require('contentful')
// use default environment config for convenience
// these will be set via `env` property in nuxt.config.js
const ctf_config = {
  space: process.env.CTF_SPACE_ID,
  accessToken: process.env.CTF_CDA_ACCESS_TOKEN,
  host: process.env.CTF_API_HOST
}

// export `createClient` to use it in page components
export default function createClient() {
  const client = contentful.createClient(ctf_config)
  return client
}
