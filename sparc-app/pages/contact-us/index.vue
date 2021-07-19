<template>
  <div class="contact-us-page">
    <breadcrumb :breadcrumb="breadcrumb" :title="pageTitle" />
    <page-hero v-if="heroCopy">
      <h1>{{ pageTitle }}</h1>
      <!-- eslint-disable vue/no-v-html -->
      <!-- marked will sanitize the HTML injected -->
      <div v-html="parseMarkdown(heroCopy)" />
    </page-hero>
    <div class="page-wrap container">
      <div class="subpage">
        <template v-if="!isBugSubmitted && !isGeneralSubmitted">
          <h2>Let us know why you’re contacting us:</h2>
          <el-select
            v-model="formType"
            class="input-reason"
            placeholder="Select a reason"
            aria-placeholder="Select a reason"
            :popper-append-to-body="false"
          >
            <el-option
              v-for="option in formTypeOptions"
              :key="option.key"
              :label="option.label"
              :value="option.value"
            />
          </el-select>

          <hr v-if="formType" class="mt-32 mb-32" />

          <general-form
            v-if="formType === 'general'"
            @submit="onGeneralFormSubmit($event)"
          />
          <bug-form v-if="formType === 'bug'" @submit="isBugSubmitted = true" />
        </template>

        <div v-if="isGeneralSubmitted" class="msg-success">
          <template v-if="firstName">
            <p>{{ firstName }},</p>
          </template>
          <p>
            Thank you for your inquiry. A member of the SPARC team will contact
            you within two business days.
          </p>
          <a href="#" @click="resetForms">Submit another inquiry</a>
        </div>

        <div v-if="isBugSubmitted" class="msg-success">
          <p>
            Thank you for letting us know about this error or technical issue.
            If you requested a response, a member of the SPARC team will contact
            you within two business days.
          </p>
          <a href="#" @click="resetForms">Submit another inquiry</a>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import Breadcrumb from '@/components/Breadcrumb/Breadcrumb.vue'
import PageHero from '@/components/PageHero/PageHero.vue'
import GeneralForm from '@/components/ContactUsForms/GeneralForm/GeneralForm.vue'
import BugForm from '@/components/ContactUsForms/BugForm/BugForm.vue'

import MarkedMixin from '@/mixins/marked'
import createClient from '@/plugins/contentful.js'

const client = createClient()

export default {
  name: 'ContactUsPage',

  components: {
    Breadcrumb,
    PageHero,
    GeneralForm,
    BugForm
  },

  mixins: [MarkedMixin],

  asyncData() {
    return Promise.all([
      // Get page content
      client.getEntry(process.env.ctf_contact_us_page_id)
    ])
      .then(([page]) => {
        return { ...page.fields }
      })
      .catch(console.error)
  },

  data: () => {
    return {
      heroCopy: '',
      breadcrumb: [
        {
          to: {
            name: 'index'
          },
          label: 'Home'
        }
      ],
      formType: '',
      formTypeOptions: [
        {
          label: 'I couldn’t find the information in Help',
          value: 'general'
        },
        {
          label: 'I want to report an error or a technical issue',
          value: 'bug'
        }
      ],
      isBugSubmitted: false,
      isGeneralSubmitted: false,
      firstName: ''
    }
  },

  watch: {
    /**
     * Set formType data based on query param
     * @param {Object} to
     */
    $route: {
      handler(to) {
        this.formType = to.query.type
      },
      immediate: true
    },

    /**
     * Set query param based on formType data
     * @param {String} val
     */
    formType(val) {
      this.$router.push({ query: { type: val } })
    }
  },

  methods: {
    /**
     * Reset all form data
     */
    resetForms: function() {
      this.isBugSubmitted = false
      this.isGeneralSubmitted = false
      this.formType = ''
      this.firstName = ''
    },

    /**
     * On general form meetings
     * @param {String} firstName
     */
    onGeneralFormSubmit: function(firstName) {
      this.firstName = firstName
      this.isGeneralSubmitted = true
    }
  }
}
</script>

<style scoped lang="scss">
@import '@/assets/_variables.scss';
.page {
  display: flex;
  margin-top: 7rem;

  p {
    color: #606266;
  }
}
h2 {
  font-size: 1.5rem;
  line-height: 2rem;
}
.msg-success {
  font-size: 1.5rem;
  line-height: 2rem;
}
</style>

<style lang="scss">
@import '@/assets/_variables.scss';
.contact-us-page {
  .el-form-item:not(.mb-0) {
    margin-bottom: 3.25rem;
  }
  .el-form-item__label {
    color: #000;
    font-size: 1.625rem;
    line-height: 1.2;
    margin-bottom: 1rem;
    padding-bottom: 0;
  }
  .el-select {
    max-width: 20rem;
    width: 100%;
  }
  .el-input,
  .el-textarea,
  .el-select-dropdown__item {
    font-size: 1rem;
    ::placeholder {
      color: $medium-gray;
    }
  }
  .el-input__inner,
  .el-textarea__inner {
    border-color: $medium-gray;
    border-radius: 4px;
    padding: 0.5rem 1rem;
  }
  .el-textarea__inner {
    font-family: inherit;
  }
  .input-reason {
    max-width: 36rem;
    width: 100%;
    ::placeholder {
      color: $dark-sky;
    }
  }
}
</style>
