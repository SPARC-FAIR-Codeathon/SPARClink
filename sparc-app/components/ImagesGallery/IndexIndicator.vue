<template>
  <div class="indicator-container">
    <div
      v-for="(number, index) in count"
      :key="'indicator_' + number"
      :class="['indicator', { active: current === index }]"
    />
  </div>
</template>

<script>
export default {
  name: 'IndexIndicator',
  props: {
    count: {
      type: Number,
      default: 0,
    },
    current: {
      type: Number,
      default: 0,
    },
  },
}
</script>

<style>
.indicator-container {
  display: flex;
  justify-content: center;
}
.indicator {
  width: 1em;
  height: 1em;
  border-radius: 50%;
  margin-left: 0.2em;
  margin-right: 0.2em;
  background-color: #8300bf;
  opacity: 0.5;
}
.indicator.active {
  transform: scale(1.2);
  opacity: 1;
}
</style>
