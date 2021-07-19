import axios from 'axios'

const apiClient = axios.create({
  baseURL: process.env.portal_api,
  withCredentials: false,
  timeout: 10000
})

const getImageMapData = id => {
  return apiClient.get('imagemap/search_dataset/discover/' + id)
}

const getThumbnail = async id => {
  return apiClient.get('thumbnail/' + id)
}

const getImageInfo = async id => {
  return apiClient.get('image/' + id)
}

const getCollectionInfo = async id => {
  return apiClient.get('collections/' + id)
}

export default {
  getThumbnail,
  getImageMapData,
  getImageInfo,
  getCollectionInfo
}
