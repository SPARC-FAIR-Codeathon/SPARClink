<template>
  <div class="page-hero">
    <div class="container">
      <div class="row">
        <div class="col page-hero__copy">
          <slot />
        </div>
        <div v-if="$slots['image']" class="page-hero__image">
          <slot name="image" />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'PageHero',
  props: {
    justify: {
      type: String,
      default: 'center'
    }
  }
}
</script>

<style lang="scss">
@import '../../assets/_variables.scss';

.page-hero {
  background: $navy;
  color: #f0f2f5;
  font-size: 1em;
  line-height: 1.5rem;
  padding: 2rem 1rem;
  @media (min-width: 48em) {
    font-size: 1.25em;
    line-height: 2rem;
    padding: 2.5rem 0;
  }
  &__copy {
    position: relative;
    z-index: 1;
    @media (min-width: 64em) {
      max-width: 53rem;
    }
    a {
      color: #fff;
      text-decoration: underline;
    }
  }
  &__image {
    display: none;

    @media (min-width: 48em) {
      display: flex;
      height: calc(100% + 5rem);
      justify-content: flex-end;
      right: 0;
      position: absolute;
      top: -2.5rem;
      width: auto;
    }
    img,
    video {
      display: block;
      height: 100%;
      width: inherit;
    }
  }
  .container {
    position: relative;
  }
  h1 {
    font-size: 1.75em;
    margin-bottom: 0.5rem;
    line-height: 1.2;
  }
  h1,
  p {
    background-color: rgba(36, 36, 91, 0.75);
  }

  .row {
    display: flex;
  }
}
</style>
