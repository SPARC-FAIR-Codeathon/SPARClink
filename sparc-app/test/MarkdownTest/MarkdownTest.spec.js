import { mount } from '@vue/test-utils'
import MarkdownTest from './MarkdownTest'

describe('MarkdownTest', () => {
  const wrapper = mount(MarkdownTest)

  it('Renders the correct markup', () => {
    expect(wrapper.find('#externalWrap a').exists()).toBe(true)
    expect(wrapper.find('#externalWrap h1').exists()).toBe(true)
  })

  it('Adds target="blank" to links', () => {
    expect(wrapper.find('#externalWrap a').element.getAttribute('target')).toBe(
      '_blank'
    )
  })

  it('Renders an anchor tag properly', () => {
    expect(wrapper.find('#anchorWrap a').element.getAttribute('target')).toBe(
      null
    )
  })
})
