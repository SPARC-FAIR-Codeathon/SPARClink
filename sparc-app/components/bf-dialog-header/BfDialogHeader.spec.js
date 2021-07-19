import Vue from 'vue'
import BfDialogHeader from './BfDialogHeader.vue'
import { mount } from '@vue/test-utils'

describe('BfDialogHeader.vue', () => {
  let cmp
  let Test

  beforeEach(() => {
    Test = Vue.component('Test', {
      components: {
        BfDialogHeader
      },
      template: '<bf-dialog-header></bf-dialog-header>'
    })
    cmp = mount(Test, {
      methods: {
        handleClose: () => {}
      }
    })
  })

  it('Parent handles close event', () => {
    const spy = jest.spyOn(cmp.vm, 'handleClose')
    cmp.vm.$children[0].onClose()
    expect(spy).toBeCalled()
  })
})
