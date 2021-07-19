<template>
  <div class="sparc-pill">
    <slot />
  </div>
</template>

<script>
export default {
  name: 'SparcPill'
}
</script>

<style lang="scss" scoped>
@import '../../assets/_variables.scss';
.sparc-pill {
  background: $median;
  border-radius: 15px;
  color: #fff;
  font-size: 0.875rem;
  max-width: 100%;
  overflow: hidden;
  padding: 0 0.65rem;
  text-overflow: ellipsis;
}
</style>
