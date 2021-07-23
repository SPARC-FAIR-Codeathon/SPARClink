<template>
  <div class="w-full flex flex-row mx-auto justify-between px-16">
    <div class="w-7/12 flex flex-col items-start justify-start py-10 px-8">
      <img
        src="https://sparc.science/_nuxt/img/logo-sparc-wave-primary.8ed83a5.svg"
        alt=""
        class="w-40 py-4"
      />
      <h4 class="text-gray-500 font-sans text-lg leading-relaxed">
        The NIH Common Fund’s Stimulating Peripheral Activity to Relieve
        Conditions (SPARC) program aims to transform our understanding of
        nerve-organ interactions with the intent of advancing bioelectronic
        medicine towards treatments that change lives.
      </h4>
      <div class="flex flex-row py-5">
        <svg
          version="1.1"
          viewBox="0 0 24 19.5"
          class="svg-icon svg-fill mr-5"
          style="width: 32px; height: 32px"
          data-v-47fc1802=""
        >
          <path
            fill="#606266"
            stroke="none"
            pid="0"
            d="M7.5 19.5c9.1 0 14-7.5 14-14v-.6c1-.7 1.8-1.6 2.5-2.5-.9.4-1.9.7-2.8.8 1-.6 1.8-1.6 2.2-2.7-1 .6-2 1-3.1 1.2-1.9-2-5-2.1-7-.2-1.3 1.2-1.8 3-1.4 4.7C7.9 5.8 4.2 4 1.7.9.4 3.1 1 6 3.2 7.5c-.8-.1-1.6-.3-2.2-.6V7c0 2.3 1.7 4.4 4 4.8-.7.2-1.5.2-2.2.1.6 2 2.5 3.4 4.6 3.4-1.7 1.4-3.9 2.1-6.1 2.1-.4 0-.8 0-1.2-.1 2.2 1.4 4.8 2.2 7.4 2.2"
          ></path>
        </svg>
        <svg
          version="1.1"
          viewBox="0 0 24 16.9"
          class="svg-icon svg-fill"
          style="width: 32px; height: 32px"
          data-v-47fc1802=""
        >
          <path
            fill="#606266"
            stroke="none"
            pid="0"
            d="M23.5 2.6c-.3-1-1.1-1.9-2.1-2.1C19.5 0 12 0 12 0S4.5 0 2.6.5C1.6.8.8 1.6.5 2.6 0 4.5 0 8.5 0 8.5s0 3.9.5 5.8c.3 1 1.1 1.9 2.1 2.1 1.9.5 9.4.5 9.4.5s7.5 0 9.4-.5c1-.3 1.8-1.1 2.1-2.1.5-1.9.5-5.8.5-5.8s0-4-.5-5.9zM9.5 12V4.9l6.3 3.6L9.5 12z"
          ></path>
        </svg>
      </div>
    </div>
    <div class="w-4/12 grid grid-cols-2 gap-2 py-10">
      <h5 class="footer-title">Learn More</h5>
      <h5 class="footer-title">Policies</h5>
      <p class="footer-subtitle">About SPARC</p>
      <p class="footer-subtitle">Privacy Policy</p>
      <p class="footer-subtitle">Funding Opportunities</p>
      <p class="footer-subtitle">Terms of Service</p>
      <p class="footer-subtitle">NIH SPARC Program</p>
      <p class="footer-subtitle">Other SPARC Policies</p>
      <p class="footer-subtitle">SPARC Systems Status</p>
      <p class="footer-subtitle"></p>
      <p class="footer-subtitle">SPARC Publications</p>
      <p class="footer-subtitle"></p>
      <p class="footer-subtitle">SPARC Glossary</p>
      <p class="footer-subtitle"></p>
      <h5 class="footer-title">Help Us Improve</h5>
      <h5 class="footer-title">Stay Up-to-Date</h5>
      <p class="footer-subtitle">Site Feedback</p>
      <p class="footer-subtitle">Join our E-mail list</p>
    </div>
  </div>
</template>

<script>
export default {
  name: "TheFooter",
  data() {
    return {};
  },
};
</script>

<style lang="postcss" scoped>
.footer-title {
  @apply font-sans text-gray-600 font-bold text-lg py-2;
}
.footer-subtitle {
  @apply font-sans text-gray-700 font-medium text-lg pb-2;
}
</style>
