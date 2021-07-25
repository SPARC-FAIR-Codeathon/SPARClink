<template>
  <div class="flex justify-end bg-indigo-900 py-1">
    <a href="https://sparc.science" target="_blank" class="p-2 flex flex-row">
      <svg
        version="1.1"
        viewBox="0 0 24 24"
        class="svg-icon svg-fill"
        style="width: 18px; height: 18px"
        data-v-38f78515=""
      >
        <path
          fill="#fff"
          pid="0"
          d="M12 5a7 7 0 11-7 7 7.008 7.008 0 017-7m0-2a9 9 0 109 9 9 9 0 00-9-9z"
        ></path>
        <path
          fill="#fff"
          pid="1"
          d="M12 7.148a.9.9 0 10.9.9.9.9 0 00-.9-.9zM12 17.148a1 1 0 01-1-1v-5.4a1 1 0 112 0v5.4a1 1 0 01-1 1z"
        ></path>
      </svg>
      <span class="text-white text-sm px-1">
        This is a developer demo of the SPARC Portal. Click here to go to
        official SPARC Portal
      </span>
    </a>
    <a href="#" class="p-2 flex flex-row">
      <svg
        version="1.1"
        viewBox="0 0 24 24"
        class="svg-icon svg-fill"
        style="width: 18px; height: 18px"
        data-v-38f78515=""
      >
        <path
          fill="#fff"
          pid="0"
          d="M12 5a7 7 0 11-7 7 7.008 7.008 0 017-7m0-2a9 9 0 109 9 9 9 0 00-9-9z"
        ></path>
        <path
          fill="#fff"
          pid="1"
          d="M12 7.148a.9.9 0 10.9.9.9.9 0 00-.9-.9zM12 17.148a1 1 0 01-1-1v-5.4a1 1 0 112 0v5.4a1 1 0 01-1 1z"
        ></path>
      </svg>
      <span class="text-white text-sm px-1"> About SPARC </span>
    </a>
    <a href="#" class="p-2 flex flex-row">
      <svg
        version="1.1"
        viewBox="0 0 24 24"
        class="svg-icon svg-fill"
        style="width: 18px; height: 18px"
        data-v-38f78515=""
      >
        <path
          fill="#fff"
          pid="0"
          d="M19 5.6v7.219h-4.181V16.1l-3.889-3.282H5V5.6h14m2-2H3v11.218h7.2l3.331 2.81 3.288 2.772v-5.582H21V3.6z"
        ></path>
      </svg>
      <span class="text-white text-sm px-1"> Contact Us </span>
    </a>
    <a href="#" class="p-2 flex flex-row">
      <svg
        version="1.1"
        viewBox="0 0 24 24"
        class="svg-icon svg-fill"
        style="width: 18px; height: 18px"
        data-v-38f78515=""
      >
        <circle pid="0" cx="12" cy="15.824" r=".753" fill="#fff"></circle>
        <path
          fill="#fff"
          pid="1"
          d="M12 14.256a.75.75 0 01-.75-.75v-1c0-.529.419-.818.862-1.124.623-.43 1.138-.83 1.138-1.376A1.209 1.209 0 0012 8.756a1.252 1.252 0 00-1.25 1.25.75.75 0 01-1.5 0A2.753 2.753 0 0112 7.256a2.721 2.721 0 012.75 2.75 3.3 3.3 0 01-1.786 2.61c-.079.055-.152.1-.214.147v.743a.75.75 0 01-.75.75z"
        ></path>
        <path
          fill="#fff"
          pid="2"
          d="M12 5a7 7 0 11-7 7 7.008 7.008 0 017-7m0-2a9 9 0 109 9 9 9 0 00-9-9z"
        ></path>
      </svg>
      <span class="text-white text-sm px-1"> Need Help? </span>
    </a>
  </div>
  <div class="w-full bg-white flex flex-row py-6 px-1 justify-between">
    <div class="flex flex-row pl-4">
      <img
        src="https://sparc.science/_nuxt/img/logo-sparc-wave-primary.8ed83a5.svg"
        class="w-36"
      />
      <div class="flex flex-row items-center pl-8">
        <a
          v-for="item in navLinksList"
          :key="item.name"
          :href="item.href"
          class="
            mx-1
            px-1
            text-base text-indigo-800
            hover:text-purple-600
            border-b-2 border-transparent
            hover:border-purple-600
          "
        >
          {{ item.name }}
        </a>
      </div>
    </div>
    <div class="flex flex-row items-center px-5 hidden">
      <div class="flex flex-row items-center px-5">
        <div class="border rounded border-gray-900 flex flex-row w-80">
          <div
            class="
              bg-gray-200
              rounded-sm
              p-2
              text-base
              pr-10
              text-gray-700
              flex flex-row
              justify-between
            "
          >
            <span> Datasets </span>
          </div>
          <div class="p-2 text-base text-gray-600">Search</div>
        </div>
      </div>
      <button
        class="
          bg-purple-600
          w-10
          h-10
          rounded-lg
          flex
          items-center
          justify-center
          hidden
        "
      >
        <svg
          version="1.1"
          viewBox="0 0 24 24"
          class="svg-icon svg-fill svg-left"
          style="width: 25px; height: 25px; transform: scale(-1, 1)"
        >
          <path
            fill="white"
            stroke="none"
            pid="0"
            d="M13 4c-3.3 0-6 2.7-6 6 0 1.3.4 2.5 1.1 3.5l-4.8 4.8c-.4.4-.4 1 0 1.4.2.2.4.3.7.3s.5-.1.7-.3l4.8-4.8c1 .7 2.2 1.1 3.5 1.1 3.3 0 6-2.7 6-6s-2.7-6-6-6zm0 10c-2.2 0-4-1.8-4-4s1.8-4 4-4 4 1.8 4 4-1.8 4-4 4z"
          ></path>
        </svg>
      </button>
    </div>
  </div>
</template>

<script>
export default {
  name: "TheHeader",
  data() {
    return {
      navLinksList: [
        { name: "Home", href: "/home" },
        { name: "Find Data", href: "/home" },
        { name: "Tools & Resources", href: "/home" },
        { name: "Maps", href: "/home" },
        { name: "SPARClink", href: "/sparclink" },
      ],
    };
  },
};
</script>

<style></style>
