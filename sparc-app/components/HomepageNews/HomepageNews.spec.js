import { shallowMount, RouterLinkStub } from '@vue/test-utils'
import HomepageNews from './HomepageNews.vue'
import { events, internalEvent } from './mockNews'

describe('HomepageNews.vue', () => {
  it('filters only future news or news without a date', () => {
    const wrapper = shallowMount(HomepageNews, {
      propsData: {
        news: events
      },
      stubs: {
        NuxtLink: RouterLinkStub,
        SvgIcon: true,
        ElButton: true
      }
    })

    expect(wrapper.vm.news.length).toBe(4)
    expect(wrapper.vm.upcomingNews.length).toBe(2)
  })

  it('Renders a NuxtLink if the entry has a details page', () => {
    const wrapper = shallowMount(HomepageNews, {
      propsData: {
        news: internalEvent
      },
      stubs: {
        NuxtLink: RouterLinkStub,
        SvgIcon: true,
        ElButton: true
      }
    })

    const link = wrapper.findComponent(RouterLinkStub)
    expect(link.exists()).toBe(true)
  })

  it('Renders an a tag if the entry does not have a details page', () => {
    const wrapper = shallowMount(HomepageNews, {
      propsData: {
        news: events
      },
      stubs: {
        NuxtLink: RouterLinkStub,
        SvgIcon: true,
        ElButton: true
      }
    })

    const link = wrapper.find('h3 NuxtLink')
    expect(link.exists()).toBe(false)
  })
})
