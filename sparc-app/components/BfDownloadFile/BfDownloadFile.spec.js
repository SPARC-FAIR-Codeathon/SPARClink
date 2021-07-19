import { shallowMount, mount } from '@vue/test-utils'
import BfDownloadFile from './BfDownloadFile.vue'

import Config from '@/nuxt.config'

const smallFile = {
  name: '1G.random',
  path: 'files/1G.random',
  size: 100000,
  icon: 'Generic',
  uri: 's3://pennsieve-prod-discover-publish-use1/676/17/files/1G.random',
  fileType: 'GenericData',
  packageType: 'Unknown',
  sourcePackageId: 'N:package:503af663-118e-4c9f-9046-4359871d2e95',
  createdAt: null,
  type: 'File'
}

const selectedMock = [
  smallFile,
  {
    name: '1G.random (1)',
    path: 'files/1G.random (1)',
    size: 1073741824,
    icon: 'Generic',
    uri: 's3://pennsieve-prod-discover-publish-use1/676/17/files/1G.random (1)',
    fileType: 'GenericData',
    packageType: 'Unknown',
    sourcePackageId: 'N:package:84a65d32-ed67-4685-852f-e2ee33893b02',
    createdAt: null,
    type: 'File'
  },
  {
    name: '20G.random',
    path: 'files/20G.random',
    size: 21474836480,
    icon: 'Generic',
    uri: 's3://pennsieve-prod-discover-publish-use1/676/17/files/20G.random',
    fileType: 'GenericData',
    packageType: 'Unknown',
    sourcePackageId: 'N:package:2cbbec8e-0bd8-43aa-b8e4-afe0f0eec7ad',
    createdAt: null,
    type: 'File'
  }
]
const dataset = {
  id: 676,
  sourceDatasetId: 1338,
  name: '1 terabyte data',
  description: 'Test for publishing large datasets',
  ownerId: 11,
  ownerFirstName: 'Bo',
  ownerLastName: 'Marchman',
  ownerOrcid: '0000-0003-4794-225X',
  organizationName: 'Blackfynn Test',
  organizationId: 19,
  license: 'Community Data License Agreement – Sharing',
  tags: ['data'],
  version: 17,
  revision: null,
  size: 572307256170,
  modelCount: [],
  fileCount: 1141,
  recordCount: 0,
  uri: 's3://pennsieve-prod-discover-publish-use1/676/17/',
  arn: 'arn:aws:s3:::pennsieve-prod-discover-publish-use1/676/17/',
  status: 'PUBLISH_SUCCEEDED',
  doi: '10.21397/gonm-7vsy',
  banner:
    'https://assets.discover.pennsieve.io/dataset-assets/676/17/banner.jpg',
  readme:
    'https://assets.discover.pennsieve.io/dataset-assets/676/17/readme.md',
  contributors: [
    {
      firstName: 'Bo',
      middleInitial: null,
      lastName: 'Marchman',
      degree: null,
      orcid: '0000-0003-4794-225X'
    }
  ],
  collections: [],
  externalPublications: [],
  sponsorship: null,
  pennsieveSchemaVersion: '4.0',
  createdAt: '2020-09-17T17:09:33.04728Z',
  updatedAt: '2020-10-27T20:12:17.446566Z',
  firstPublishedAt: '2020-09-15T11:26:25.589161Z',
  versionPublishedAt: '2020-09-17T17:09:33.04728Z',
  revisedAt: null,
  embargo: false,
  embargoReleaseDate: null,
  ownerEmail: ''
}

beforeAll(() => {
  process.env = Config.env
})

describe('BfDownloadFile.vue', () => {
  test('Does not allow downloads over the app threshold', () => {
    const wrapper = shallowMount(BfDownloadFile, {
      propsData: {
        dataset,
        selected: selectedMock
      },
      stubs: {
        SvgIcon: true,
        ElButton: true,
        ElDialog: true,
        ElInput: true
      }
    })

    expect(wrapper.vm.downloadDisabled).toBe(true)
  })

  test('Allows downloads under the app threshold', () => {
    const wrapper = shallowMount(BfDownloadFile, {
      propsData: {
        dataset,
        selected: [smallFile]
      },
      stubs: {
        SvgIcon: true,
        ElButton: true,
        ElDialog: true,
        ElInput: true
      }
    })

    expect(wrapper.vm.downloadDisabled).toBe(false)
  })
})
