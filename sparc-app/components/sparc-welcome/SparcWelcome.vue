<template>
  <div class="sparc-welcome">
    {{ message }}
  </div>
</template>

<script>
export default {
  name: 'SparcWelcome',
  components: {},
  props: {
    message: {
      type: String,
      default: 'The SPARC Portal will be coming soon (Summer 2019)!'
    }
  }
}
</script>

<style lang="scss" scoped></style>
