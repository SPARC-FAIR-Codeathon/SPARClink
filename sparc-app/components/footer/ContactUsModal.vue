<template>
  <el-dialog :show-close="true" :visible.sync="visible" @close="onClose">
    <div class="dialog-body">
      <div class="header">
        <h2>Send Us a Message</h2>
      </div>
      <el-form
        ref="contactForm"
        :label-position="labelPosition"
        label-width="100px"
        :model="contactUsForm"
        :rules="contactUsFormRules"
      >
        <el-form-item prop="name" label="Your Name">
          <el-input
            v-model="contactUsForm.name"
            aria-placeholder="Enter your name"
          />
        </el-form-item>
        <el-form-item prop="email" label="Your Email">
          <el-input
            v-model="contactUsForm.email"
            aria-placeholder="Enter your email"
            type="email"
          />
        </el-form-item>
        <el-form-item prop="message" label="Your Message">
          <el-input
            v-model="contactUsForm.message"
            aria-placeholder="Your message"
            type="textarea"
          />
        </el-form-item>
        <el-form-item>
          <el-button class="send-button" @click="submitContactForm">
            Send
          </el-button>
        </el-form-item>
      </el-form>
    </div>
  </el-dialog>
</template>

<script>
export default {
  name: 'ContactUsModal',
  props: {
    visible: {
      type: Boolean,
      default: false
    }
  },
  data() {
    return {
      labelPosition: 'top',
      contactUsForm: {
        name: '',
        email: '',
        message: ''
      },
      contactUsFormRules: {
        name: [
          {
            required: true,
            message: 'Please enter your name',
            trigger: 'change'
          }
        ],

        email: [
          {
            required: true,
            message: 'Please enter your email',
            trigger: 'change'
          }
        ],

        message: [
          {
            required: true,
            message: 'Please enter a message',
            trigger: 'change'
          }
        ]
      }
    }
  },

  methods: {
    submitContactForm: function() {
      this.$refs.contactForm.validate(valid => {
        if (!valid) {
          return
        }
        this.sendRequest()
      })
    },

    sendRequest: function() {
      // send request logic goes here
      this.$http.post('/api/contact', {
        name: this.contactUsForm.name,
        email: this.contactUsForm.email,
        message: this.contactUsForm.message
      })
      this.onClose()
    },

    onClose: function() {
      this.$emit('update:visible', false)
      this.$refs.contactForm.resetFields()
    }
  }
}
</script>

<style lang="scss" scoped>
.send-button {
  background-color: #24245b;
  color: white;
  display: block;
  border-radius: 4px;
  margin: 0 auto;
  padding: 12px 46px;
}

.header {
  margin-left: 1px;
  @media (max-width: 767px) {
    text-align: center;
    width: 90vw;
  }
}

h2 {
  color: #24245b;
  font-weight: normal;
  font-size: 46px;
  line-height: 1;
  margin-bottom: 32px;
  text-transform: none;
  @media (max-width: 767px) {
    & {
      font-size: 24px;
    }
  }
}

.el-dialog {
  background: none;
  display: flex;
  height: 100vh;
  margin: 0 !important;
  width: 100vw;

  .el-dialog__body {
    align-items: center;
    background-color: rgba(237, 241, 252, 0.9);
    display: flex;
    flex: 1;
    justify-content: center;
    padding: 0;
  }

  .el-dialog__header {
    padding: 0;
  }

  .el-dialog__headerbtn .el-dialog__close {
    font-size: 34px;
    color: #24245b;
    font-weight: bold;
  }
}

.el-form {
  margin: 0 auto;
  max-width: 317px;
}

.el-form-item__label {
  line-height: 1.2;
}

.el-input {
  .el-input__inner {
    border-radius: 4px;
    border: 1px solid #909399;
  }
}

.el-form-item {
  margin-bottom: 26px;
  &:last-child {
    margin: 0;
  }
}

.el-textarea {
  .el-textarea__inner {
    border-radius: 4px;
    border: 1px solid #909399;
  }
}

.el-form {
  .el-form-item {
    .el-form-item__label {
      text-transform: none;
    }
  }
}
</style>
