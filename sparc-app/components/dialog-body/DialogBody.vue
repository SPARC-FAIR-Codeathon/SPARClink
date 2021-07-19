<template>
  <div :class="classNames">
    <div v-if="$slots['icon']" class="dialog-body-icon">
      <slot name="icon" />
    </div>

    <div v-if="$slots['heading']" class="dialog-body-heading">
      <slot name="heading" />
    </div>

    <div class="dialog-body-content">
      <slot />
    </div>
  </div>
</template>

<style lang="scss" scoped>
@import '../../assets/_variables.scss';

.dialog-body {
  align-items: center;
  display: flex;
  font-size: 14px;
  flex-direction: column;
  justify-content: center;
  .simple & {
    padding: 64px 48px;
    text-align: center;
    &.icon {
      padding: 48px;
    }
  }
}

.dialog-spacing {
  align-items: center;
  display: flex;
  font-size: 14px;
  flex-direction: column;
  justify-content: center;
  .simple & {
    padding: 0 0px;
    text-align: center;
    &.icon {
      padding: 48px;
    }
  }
}

.dialog-body-icon {
  margin-bottom: 8px;
}

.dialog-body-heading {
  color: #000;
  font-weight: bold;
  line-height: 16px;
  margin-bottom: 8px;

  h2,
  h3 {
    font-size: 14px;
    line-height: 14px;
    margin: 0;
  }
}

.btn-third-option {
  display: inline-block;
  margin-top: 16px;
}

.dialog-body-content {
  color: $glial;
  line-height: 18px;
  width: 100%;
}

.dialog-simple-buttons {
  display: flex;
  margin-top: 16px;
  justify-content: center;
  .bf-button:nth-child(2) {
    margin-left: 8px;
  }
}

.spacing {
  padding: 64px 7px;
}
</style>

<script>
export default {
  name: 'DialogBody',

  props: {
    fixedHeight: {
      type: Boolean,
      default: false
    }
  },

  computed: {
    classNames: function() {
      const hasIcon = this.$slots['icon'] ? 'icon' : ''
      const fixedHeight = this.fixedHeight ? 'fixed-height' : ''

      return `dialog-body ${hasIcon} ${fixedHeight}`
    }
  }
}
</script>
