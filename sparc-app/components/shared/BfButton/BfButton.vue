<template>
  <button
    class="bf-button"
    :disabled="disabled || processing"
    :autofocus="autofocus"
    :type="type"
    :class="[type ? 'bf-button--' + type : '']"
    @click="handleClick"
  >
    <span v-if="hasPrefixSlot" class="prefix">
      <slot name="prefix" />
    </span>

    <template v-if="processing">
      <el-spinner class="button-spinner" :radius="40" />
      <template v-if="processingText">
        {{ processingText }}
      </template>

      <template v-else>
        <slot />
      </template>
    </template>

    <template v-if="!processing">
      <slot />
    </template>

    <span v-if="hasSuffixSlot" class="suffix">
      <slot name="suffix" />
    </span>
  </button>
</template>

<script>
export default {
  name: 'BfButton',

  props: {
    type: {
      type: String,
      default: 'button'
    },
    autofocus: Boolean,
    disabled: Boolean,
    processing: {
      type: Boolean,
      default: false
    },
    processingText: {
      type: String,
      default: ''
    }
  },

  computed: {
    hasPrefixSlot: function() {
      return !!this.$slots['prefix']
    },
    hasSuffixSlot: function() {
      return !!this.$slots['suffix']
    }
  },

  methods: {
    /**
     * On click
     * @param {Object} evt
     */
    handleClick(evt) {
      this.$emit('click', evt)
    }
  }
}
</script>

<style lang="scss" scoped>
@import '@/assets/_variables.scss';

.bf-button {
  align-items: center;
  background: $median;
  border: 1px solid transparent;
  border-radius: 4px;
  color: #fff;
  cursor: pointer;
  display: inline-flex;
  flex-direction: row;
  font-family: $font-family;
  font-size: 14px;
  justify-content: center;
  line-height: 1;
  margin: 0;
  min-width: 112px;
  outline: none;
  padding: 12px 16px;
  text-transform: none;
  &[disabled] {
    opacity: 0.6;
    cursor: default;
  }
  &:not([disabled]) {
    &:hover,
    &:focus {
      background: $median;
    }
    &:hover {
      box-shadow: 2px 2px 4px rgba(0, 0, 0, 0.25);
    }
    &:active {
      box-shadow: none;
    }
  }
  &.small {
    font-size: 10px;
    color: #ffffff;
    text-align: left;
    line-height: 12px;
    padding: 8px 16px;
    margin-bottom: -10px;
    margin-top: -4px;
  }
  &.compact {
    padding: 8px 16px;
  }
  &.icon {
    padding: 11px 11px;
    min-width: 0;
  }
  &.ghost {
    background: #f9f2fc;
    border-color: $median;
    color: $median;
    font-weight: 500;
    &:not([disabled]) {
      &:hover {
        background: white;
      }
      &:active,
      &:focus {
        background: $median;
        color: white;
      }
    }
  }
  &.white {
    background: #fff;
    color: #000;
    &:hover,
    &:focus {
      background: #fff;
    }
  }
  &.secondary {
    background-color: $light-purple;
    border: solid 1px $median;
    color: $median;
    border-radius: 4px;
    width: 140px;
    &:hover {
      background: $light-purple;
    }
  }
  &.button-spacing {
    margin-left: 16px;
  }

  & iron-icon {
    margin-right: 5px;
  }
}
.button-spinner {
  height: 20px;
  margin: -3px 8px -3px 0;
  width: 20px;
}
.prefix,
.suffix {
  display: inline-flex;
}
.prefix {
  margin-right: 16px;
  .compact & {
    margin-right: 8px;
  }
}
.suffix {
  margin-left: 16px;
  .compact & {
    margin-left: 8px;
  }
}
</style>
