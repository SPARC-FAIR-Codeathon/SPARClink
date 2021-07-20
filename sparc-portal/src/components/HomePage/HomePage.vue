<template>
  <div class="bg-gray-50">
    <div class="bg-indigo-900">
      <div class="max-w-screen-xl flex flex-row items-center mx-auto">
        <div>
          <h3 class="text-4xl text-white font-sans pb-2">
            Welcome to the SPARC Portal — Advancing bioelectronic medicine
            through open science!
          </h3>
          <h2 class="text-2xl text-white font-sans pb-2">
            curated datasets • maps of nerve-organ interactions • experimental
            protocols • computational studies • SPARC news and events •
            leading-edge technologies
          </h2>
          <button
            class="
              bg-gray-50
              font-sans
              py-2
              px-4
              rounded
              font-semibold
              text-base text-purple-700
            "
          >
            FIND DATA
          </button>
        </div>
        <img
          src="https://images.ctfassets.net/6bya4tyw8399/8pNex1c7zdRBr0QO3jtwf/9695da0c49b4c1e4abd1a2e9a90a4874/SPARK_Hero_Static_10.png"
          style="width: 35%"
        />
      </div>
    </div>
    <div class="max-w-screen-xl flex flex-col items-center mx-auto py-10">
      <h3
        class="
          w-full
          text-center
          justify-center
          items-center
          font-medium
          text-3xl
          font-sans
          py-6
        "
      >
        Find Data by Category
      </h3>
      <div class="flex flex-row pb-8">
        <div
          v-for="item in datasetcategories"
          :key="item.name"
          class="flex flex-col p-8"
        >
          <img :src="item.img" class="rounded-full border-2 my-4 bg-white" />
          <h4 class="font-sans text-xl w-full text-center font-semibold">
            {{ item.name }}
          </h4>
        </div>
      </div>
      <button
        class="
          bg-white
          border border-gray-300
          text-purple-600
          rounded-md
          px-4
          py-2
          font-md font-sans
          text-base
        "
      >
        View more
      </button>
    </div>
    <div class="max-w-screen-lg flex flex-col items-center mx-auto py-10">
      <h3
        class="
          w-full
          text-center
          justify-center
          items-center
          font-medium
          text-3xl
          font-sans
          py-6
        "
      >
        News & Upcoming Events
      </h3>
      <div class="w-full flex flex-row">
        <div class="w-1/2">
          <img
            src="https://images.ctfassets.net/6bya4tyw8399/2CweYgwfV1TDFT37WYGsRR/2d99a843b137ea5a482f4dde5a2b6182/sfn-min.png"
            alt=""
          />
        </div>
        <div
          class="
            w-1/2
            flex flex-col
            py-6
            px-10
            justify-center
            items-start
            bg-indigo-900
          "
        >
          <h3
            class="
              w-full
              text-left
              justify-center
              items-center
              font-medium
              text-3xl text-white
              font-sans
              py-4
            "
          >
            Society for Neuroscience 50th Annual Meeting: Abstracts due July 6
            to 15.
          </h3>
          <div class="flex flex-row justify-between">
            <div class="flex flex-row justify-around">
              <svg
                version="1.1"
                viewBox="0 0 16 17"
                class="m-1"
                style="width: 24px; height: 24px"
              >
                <g>
                  <path
                    pid="0"
                    fill="#fff"
                    d="M6.168 1.482h3.684v1.744H6.168z"
                  ></path>
                  <path
                    pid="1"
                    fill="#fff"
                    d="M13.032 3.226h1.242v2.79H1.705v-2.79h1.242V1.482H.021V17H15.98V1.482h-2.947v1.744zM1.705 15.256V7.76h12.59v7.497H1.705z"
                  ></path>
                  <path
                    pid="2"
                    fill="#fff"
                    d="M3.726 0H5.41v4.348H3.726zM10.589 0h1.684v4.348h-1.684z"
                  ></path>
                </g>
              </svg>
              <h4 class="font-medium text-2xl font-sans px-2 text-white">
                November 12, 2021 - November 16, 2021
              </h4>
            </div>
            <div class="flex flex-row">
              <svg
                version="1.1"
                viewBox="0 0 13 17"
                class="m-1"
                style="width: 24px; height: 24px"
              >
                <path
                  pid="0"
                  fill="#fff"
                  d="M6.478 0C10.072 0 13 2.95 13 6.527c0 4.203-2.485 7.422-5.546 10.104a1.418 1.418 0 01-1.908 0C2.485 13.95 0 10.73 0 6.527 0 2.951 2.928 0 6.478 0zM6.5 4A2.51 2.51 0 019 6.5C9 7.893 7.893 9 6.5 9A2.51 2.51 0 014 6.5C4 5.148 5.148 4 6.5 4z"
                  _fill="#000"
                  fill-rule="evenodd"
                ></path>
              </svg>
              <h4 class="font-medium text-2xl font-sans px-2 text-white">
                Chicago, Illinois
              </h4>
            </div>
          </div>
          <h4
            class="
              w-full
              text-left
              justify-center
              items-center
              font-medium
              text-2xl text-white
              font-sans
              py-4
            "
          >
            SPARC Symposia
          </h4>
          <button
            class="
              py-2
              px-4
              bg-white
              text-purple-700
              rounded-md
              text-base
              font-semibold
            "
          >
            Learn More
          </button>
        </div>
      </div>
    </div>
    <div class="max-w-screen-lg flex flex-col items-center mx-auto py-10">
      <div class="w-full flex flex-row-reverse">
        <div class="w-1/2">
          <img
            src="https://images.ctfassets.net/6bya4tyw8399/X9wXYhWmWAqypfnC0zjkl/85e30060e1bd04355f4ff8b1064b81e4/2A469289-B09E-47DB-995A-DCBF5B0C9058.jpeg"
            alt=""
          />
        </div>
        <div
          class="
            w-1/2
            flex flex-col
            py-6
            px-10
            justify-center
            items-start
            bg-indigo-900
          "
        >
          <h3
            class="
              w-full
              text-left
              justify-center
              items-center
              font-medium
              text-3xl text-white
              font-sans
              py-2
            "
          >
            Watch SPARC’s first Fireside Chat!
          </h3>
          <svg
            version="1.1"
            viewBox="0 0 16 17"
            class="m-1"
            style="width: 16px; height: 16px"
            data-v-4c497379=""
            data-v-4fe8fe1a=""
          >
            <path
              pid="0"
              fill="#fff"
              d="M6.168 1.482h3.684v1.744H6.168z"
            ></path>
            <path
              fill="#fff"
              pid="1"
              d="M13.032 3.226h1.242v2.79H1.705v-2.79h1.242V1.482H.021V17H15.98V1.482h-2.947v1.744zM1.705 15.256V7.76h12.59v7.497H1.705z"
            ></path>
            <path
              pid="2"
              fill="#fff"
              d="M3.726 0H5.41v4.348H3.726zM10.589 0h1.684v4.348h-1.684z"
            ></path>
          </svg>

          <h4
            class="
              w-full
              text-left
              justify-center
              items-center
              font-light
              text-xl text-white
              font-sans
              pb-4
            "
          >
            New NIH SPARC Plug vlog featuring SPARC-funded researchers and their
            peers discussing their latest scientific discoveries, from the bench
            to the bedside, and how SPARC Portal resources may help target new
            therapies for the gut!
          </h4>
          <button
            class="
              py-2
              px-4
              bg-white
              text-purple-700
              rounded-md
              text-base
              font-semibold
            "
          >
            Learn More
          </button>
        </div>
      </div>
    </div>
    <div class="max-w-screen-lg flex flex-col items-center mx-auto py-10">
      <h3
        class="
          w-full
          text-center
          justify-center
          items-center
          font-medium
          text-3xl
          font-sans
          py-6
        "
      >
        Connecting the Research community
      </h3>
      <div class="flex flex-row justify-evenly w-full">
        <div
          class="flex flex-col mx-6 w-1/3"
          v-for="item in reviews"
          :key="item.name"
        >
          <h4 class="font-sans text-xl leading-relaxed pb-4">"{{ item.review }}"</h4>
          <h5 class="text-purple-700 text-sm font-medium">-  {{ item.name }}</h5>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "HomePage",
  data() {
    return {
      datasetcategories: [
        {
          name: "Stomach",
          img: "https://images.ctfassets.net/6bya4tyw8399/5XkFsSnbCcRxopkuMjRUA1/cfef2b74ecfbd64d4310cde9ad379588/Stomach.png",
        },
        {
          name: "Colon",
          img: "https://images.ctfassets.net/6bya4tyw8399/20OtFTjdhi0KPsCLQFUcer/69366665d56b56f0a7f97b9346e9bdfc/Colon.png",
        },
        {
          name: "Heart",
          img: "https://images.ctfassets.net/6bya4tyw8399/49CWaFWgmAdjqeUlZHB0zt/0a20f3c8e6f8eaff5d51c58e1271c681/Heart.png",
        },
        {
          name: "Bladder",
          img: "https://images.ctfassets.net/6bya4tyw8399/7er5DQYVdZVr6AvqajVw5Q/f8a1c600f4ce197c8472dcc3784745f1/Bladder.png",
        },
        {
          name: "Lung",
          img: "https://images.ctfassets.net/6bya4tyw8399/4EgrOJkV79H7T12u9XPrZr/19d6456ee13cddf18c91c83fc8c5d05b/Lung.png",
        },
        {
          name: "Pancreas",
          img: "https://images.ctfassets.net/6bya4tyw8399/3Xk7mh0QPUy7zSmczHNBoP/fbed5d5c3798cfaa666b101fd1b948a8/sparc-icons-pancreas.png",
        },
      ],
      reviews: [
        {
          name: "Heather Clark, Northeastern University",
          review:
            "The (SPARC) experience has been bigger than what one lab can accomplish on its own, and I love seeing all of the different aspects come together to solve a large-scale problem.",
        },
        {
          name: "Janet Keast, University of Melbourne",
          review:
            "We all genuinely want to try and help the clinical outcomes...SPARC has provided me with a much clearer route for being able to use my work in a clinical setting.",
        },
        {
          name: "Pradeep Rajendran, University of California, Los Angeles",
          review:
            "The exact signals that go to the heart and the lungs may be slightly different, the paths are conserved between those organs, and so there's an immense amount that can be learned by interacting with other teams that are also working on different organs",
        },
      ],
    };
  },
};
</script>

<style></style>
