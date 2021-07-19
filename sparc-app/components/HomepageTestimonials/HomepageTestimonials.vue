<template>
  <div class="homepage-testimonials">
    <div class="container home-container">
      <h2>Connecting the Research Community</h2>
      <div class="homepage-testimonials__testimonial-wrap">
        <div
          v-for="(testimonial, idx) in testimonials"
          :key="testimonial.author"
          class="homepage-testimonials__testimonial"
          :class="{
            'homepage-testimonials__testimonial--active':
              activeTestimonial === idx
          }"
        >
          <p>{{ testimonial.fields.testimonial }}</p>
          <span class="homepage-testimonial__author">
            &mdash;
            {{ getByLine(testimonial.fields) }}
          </span>
        </div>
      </div>

      <div class="homepage-testimonials__anchor-wrap">
        <button
          v-for="(testimonial, idx) in testimonials"
          :key="testimonial.author"
          class="homepage-testimonials__testimonial-anchor"
          :class="{
            'homepage-testimonials__testimonial-anchor--active':
              activeTestimonial === idx
          }"
          @click="activeTestimonial = idx"
        >
          <div class="homepage-testimonials__testimonial-anchor__indicator">
            <span class="visuallyhidden">
              Go to tab for {{ testimonial.author }}
            </span>
          </div>
        </button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'HomepageTestimonials',

  props: {
    testimonials: {
      type: Array,
      default: () => []
    }
  },

  data: function() {
    return {
      activeTestimonial: 0
    }
  },

  methods: {
    /**
     * Compute byline for the testimonial
     * @param {Object}
     * @returns {String}
     */
    getByLine: function(fields) {
      const author = fields.author
      return fields.organization ? `${author}, ${fields.organization}` : author
    }
  }
}
</script>

<style lang="scss" scoped>
@import '../../assets/_variables.scss';

.home-container {
  box-sizing: border-box;
  padding-left: 1rem;
  padding-right: 1rem;
  @media (min-width: 768px) {
    padding-left: 6rem;
    padding-right: 6rem;
  }
}
.homepage-testimonials {
  padding: 1.75em 0;
  @media (min-width: 768px) {
    padding: 2em 0 4em;
  }
}
p {
  line-height: 1.875rem;
  margin: 0 0 1.25rem;
  @media (min-width: 768px) {
    font-size: 1.25em;
    line-height: 2rem;
  }
  &::before {
    content: '“';
    position: absolute;
    transform: translateX(-10px);
  }
  &::after {
    content: '”';
  }
}
.homepage-testimonials__testimonial-wrap {
  display: flex;
  padding: 0 1rem;
  @media (min-width: 768px) {
    padding: 0;
  }
}
.homepage-testimonials__testimonial {
  display: none;
  flex: 1 0 0em; // Unit required for IE11
  @media (min-width: 768px) {
    display: block;
    margin: 0 2rem;
  }
  &:first-child {
    margin-left: 0;
  }
  &:last-child {
    margin-right: 0;
  }
  &--active {
    display: block;
  }
}
.homepage-testimonials__anchor-wrap {
  margin-top: 11px;
  text-align: center;
  @media (min-width: 768px) {
    display: none;
  }
}
.homepage-testimonials__testimonial-anchor {
  background: none;
  border: none;
  cursor: pointer;
  display: inline-block;
  margin: 0 0.3em;
  outline: none;
  padding: 1em;
  &__indicator {
    background: #999;
    display: block;
    height: 0.25rem;
    width: 2rem;
  }
  &:hover,
  &:focus,
  &--active {
    .homepage-testimonials__testimonial-anchor__indicator {
      background: #fff;
    }
  }
}
.homepage-testimonial__author {
  color: $median;
  font-size: 0.875em;
}
</style>
