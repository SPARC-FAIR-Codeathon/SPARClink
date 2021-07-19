<template>
  <img class="logo" alt="SPARC logo" :src="logo" />
</template>

<script>
import logo from '@/static/images/logo-sparc-wave-primary.svg'

export default {
  name: 'SparcLogo',
  data: () => ({
    logo
  })
}
</script>

<style scoped lang="scss">
.logo {
  height: 100%;
}
</style>
