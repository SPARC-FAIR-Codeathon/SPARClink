import DialogBody from './DialogBody.vue'
import { shallow } from '@vue/test-utils'

describe('DialogBody.vue', () => {
  let cmp
  let cmpEmpty

  beforeEach(() => {
    cmp = shallow(DialogBody, {
      slots: {
        icon: '<div class="icon" />',
        heading: '<div class="heading" />',
        default: '<div class="default" />'
      }
    })
    cmpEmpty = shallow(DialogBody)
  })

  it('Has slots', () => {
    expect(cmp.vm.$slots.icon.length).toBe(1)
    expect(cmp.vm.$slots.heading.length).toBe(1)
  })

  it('Does not have slots', () => {
    expect(cmpEmpty.vm.$slots.icon).toBe(undefined)
    expect(cmpEmpty.vm.$slots.heading).toBe(undefined)
  })
})
