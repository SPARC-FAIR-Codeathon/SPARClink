import BfStorageMetrics from './'

describe('BfStorageMetrics Mixin', () => {
  const storageMetrics = {
    sums: {
      '123': 100,
      '456': 1100,
      '789': 1000001,
      '999': 1010000000,
      '007': 2100000000000
    }
  }

  let dataId = '123'

  it('Displays storage metrics in bytes', () => {
    const sum = `${storageMetrics.sums[dataId]} B`
    const displayedSum = BfStorageMetrics.methods.formatMetric(
      storageMetrics.sums[dataId]
    )
    expect(displayedSum).toEqual(sum)
  })

  it('Displays storage metrics in kilobytes', () => {
    dataId = '456'
    const sum = '1.1 KB'
    const displayedSum = BfStorageMetrics.methods.formatMetric(
      storageMetrics.sums[dataId]
    )
    expect(displayedSum).toEqual(sum)
  })

  it('Displays storage metrics in megabytes', () => {
    dataId = '789'
    const sum = '1 MB'
    const displayedSum = BfStorageMetrics.methods.formatMetric(
      storageMetrics.sums[dataId]
    )
    expect(displayedSum).toEqual(sum)
  })

  it('Displays storage metrics in gigabytes', () => {
    dataId = '999'
    const sum = '1.01 GB'
    const displayedSum = BfStorageMetrics.methods.formatMetric(
      storageMetrics.sums[dataId]
    )
    expect(displayedSum).toEqual(sum)
  })

  it('Displays storage metrics in terabytes', () => {
    dataId = '007'
    const sum = '2.1 TB'
    const displayedSum = BfStorageMetrics.methods.formatMetric(
      storageMetrics.sums[dataId]
    )
    expect(displayedSum).toEqual(sum)
  })

  it('No storage metrics to compute', () => {
    dataId = '000'
    const sum = String.fromCharCode(8212)
    const displayedSum = BfStorageMetrics.methods.formatMetric(
      storageMetrics.sums[dataId]
    )
    expect(displayedSum).toEqual(sum)
  })
})
