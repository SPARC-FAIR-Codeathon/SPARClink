<template>
  <el-form
    ref="contactForm"
    label-position="top"
    :model="form"
    :rules="formRules"
    :hide-required-asterisk="true"
  >
    <el-form-item
      prop="sparcInvestigator"
      label="Are you a SPARC investigator?*"
    >
      <el-select
        v-model="form.sparcInvestigator"
        aria-placeholder="Select one"
        :popper-append-to-body="false"
      >
        <el-option
          v-for="sparcInvestigatorOption in questionOptions.sparcInvestigator"
          :key="sparcInvestigatorOption"
          :label="sparcInvestigatorOption"
          :value="sparcInvestigatorOption"
        />
      </el-select>
    </el-form-item>

    <el-form-item
      prop="pageOrResource"
      label="Is this about a specific page or resource?"
    >
      <el-select
        v-model="form.pageOrResource"
        aria-placeholder="Select one"
        :popper-append-to-body="false"
      >
        <el-option
          v-for="pageOrResource in questionOptions.pageOrResource"
          :key="pageOrResource"
          :label="pageOrResource"
          :value="pageOrResource"
        />
      </el-select>
    </el-form-item>

    <el-form-item
      prop="title"
      label="Provide a short description of what you were doing.*"
    >
      <el-input
        v-model="form.title"
        placeholder="(Example: When I click <this button>, <this happens>.)"
      />
    </el-form-item>

    <el-form-item prop="description" label="Provide a detailed description*">
      <el-input
        v-model="form.description"
        type="textarea"
        :rows="3"
        placeholder="Please provide specific steps so our team can reproduce your experience in order to resolve the issue."
      />
    </el-form-item>

    <el-form-item
      prop="howToImprove"
      label="How would you like this experience to improve?*"
      class="mb-0"
    >
      <el-input
        v-model="form.howToImprove"
        type="textarea"
        :rows="3"
        placeholder="Description here"
      />
    </el-form-item>

    <el-form-item prop="shouldFollowUp" class="mb-0">
      <el-checkbox v-model="form.shouldFollowUp">
        Let me know when you resolve this issue
      </el-checkbox>
    </el-form-item>

    <template v-if="form.shouldFollowUp">
      <el-form-item prop="firstName" label="First Name" class="mt-32">
        <el-input v-model="form.firstName" placeholder="First name here" />
      </el-form-item>

      <el-form-item prop="lastName" label="Last Name">
        <el-input v-model="form.lastName" placeholder="Last name here" />
      </el-form-item>

      <el-form-item prop="email" label="Email" class="mb-0">
        <el-input v-model="form.email" placeholder="Email here" type="email" />
      </el-form-item>

      <el-form-item prop="shouldSubscribe">
        <el-checkbox v-model="form.shouldSubscribe">
          Subscribe to the SPARC Newsletter
        </el-checkbox>
      </el-form-item>
    </template>

    <el-form-item>
      <el-button class="primary" :disabled="isSubmitting" @click="onSubmit">
        Submit
      </el-button>
      <p v-if="hasError" class="error">
        An error has occurred, please try again.
      </p>
    </el-form-item>
  </el-form>
</template>

<script>
import { sparcInvestigator, pageOrResource } from '../questions'
import NewsletterMixin from '../NewsletterMixin'

export default {
  name: 'BugForm',

  mixins: [NewsletterMixin],

  data() {
    return {
      form: {
        sparcInvestigator: '',
        pageOrResource: '',
        title: '',
        description: '',
        howToImprove: '',
        shouldFollowUp: false,
        firstName: '',
        lastName: '',
        email: '',
        shouldSubscribe: false
      },
      questionOptions: {
        sparcInvestigator,
        pageOrResource
      },
      isSubmitting: false,
      formRules: {
        sparcInvestigator: [
          {
            required: true,
            message: 'Please select one',
            trigger: 'change'
          }
        ],

        email: [
          {
            required: true,
            message: 'Please enter your email',
            type: 'email',
            trigger: 'blur'
          }
        ],

        firstName: [
          {
            required: true,
            message: 'Please enter your first name',
            trigger: 'blur',
            validator: this.validateForNewsletter
          }
        ],

        lastName: [
          {
            required: true,
            message: 'Please enter your last name',
            trigger: 'blur',
            validator: this.validateForNewsletter
          }
        ],

        title: [
          {
            required: true,
            message: 'Please enter a description',
            trigger: 'change'
          }
        ],

        description: [
          {
            required: true,
            message: 'Please enter a description',
            trigger: 'change'
          }
        ],

        howToImprove: [
          {
            required: true,
            message: 'Please enter a description',
            trigger: 'change'
          }
        ]
      }
    }
  },

  mounted() {
    // Reset form fields when showing the form
    this.$refs.contactForm.resetFields()
    this.hasError = false
  },

  methods: {
    /**
     * Submit the form and validate
     */
    onSubmit() {
      this.hasError = false
      this.$refs.contactForm.validate(valid => {
        if (!valid) {
          return
        }
        this.sendForm()
      })
    },

    /**
     * Send form to endpoint
     */
    sendForm() {
      this.isSubmitting = true

      this.$axios
        .post(`${process.env.portal_api}/tasks`, {
          title: this.form.title,
          description: `
            Are you a SPARC investigator?<br>${this.form.sparcInvestigator}
            <br><br>Is this about a specific page or resource?
            <br>${this.form.pageOrResource}
            <br><br>Description
            <br>${this.form.description}
            <br><br>How would you like this experience to improve?
            <br>${this.form.howToImprove}
            <br><br>Let me know when you resolve this issue
            <br>${this.form.shouldFollowUp ? 'Yes' : 'No'}
            <br><br>Email
            <br>${this.form.email}
          `
        })
        .then(() => {
          if (this.form.shouldSubscribe) {
            this.subscribeToNewsletter()
          } else {
            this.$emit('submit')
          }
        })
        .catch(() => {
          this.hasError = true
        })
        .finally(() => {
          this.isSubmitting = false
        })
    }
  }
}
</script>

<style lang="scss" scoped>
@import '../../../assets/_variables.scss';

.error {
  color: $facial;
}
</style>
