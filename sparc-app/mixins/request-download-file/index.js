import { compose, last, defaultTo, split, propOr } from 'ramda'
import FileDownload from 'js-file-download'

export default {
  methods: {
    /**
     * Request download file via axios.
     */
    requestDownloadFile: function(downloadInfo) {
      const fileName = propOr('', 'name', downloadInfo)
      const datasetVersionRegexp = /s3:\/\/pennsieve-prod-discover-publish-use1\/(?<datasetId>\d*)\/(?<version>\d*)\/(?<filePath>.*)/
      const matches = downloadInfo.uri.match(datasetVersionRegexp)

      const payload = {
        data: {
          paths: [matches.groups.filePath],
          datasetId: matches.groups.datasetId,
          version: matches.groups.version
        }
      }
      this.$axios.$post(process.env.zipit_api_host, payload).then(response => {
        FileDownload(response, fileName)
      })
    }
  }
}
