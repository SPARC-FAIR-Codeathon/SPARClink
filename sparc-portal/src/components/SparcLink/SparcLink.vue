<template>
  <div
    id="svg_container"
    class="border border-gray-500 flex flex-row justify-center relative"
    style="min-height: 200px"
  >
    <div id="svg-container" ref="svgContainer">
      <canvas width="1300" height="800"></canvas>
    </div>
    <div class="bg-transparent absolute top-5 left-5 p-3 w-80 flex flex-col">
      <h2 class="font-sans text-lg text-gray-700 mb-0">Legend</h2>
      <div class="flex flex-row items-center">
        <div class="rounded-full w-3 h-3 bg-pink-600"></div>
        <span class="px-2 text-sm font-sans text-gray-700">
          SPARC Dataset
        </span>
      </div>
      <div class="flex flex-row items-center">
        <div class="rounded-full w-3 h-3 bg-yellow-500"></div>
        <span class="px-2 text-sm font-sans text-gray-700">
          SPARC Publication
        </span>
      </div>
      <div class="flex flex-row items-center">
        <div class="rounded-full w-3 h-3 bg-green-400"></div>
        <span class="px-2 text-sm font-sans text-gray-700">
          SPARC Protocol
        </span>
      </div>
      <div class="flex flex-row items-center">
        <div class="rounded-full w-3 h-3 bg-blue-500"></div>
        <span class="px-2 text-sm font-sans text-gray-700">
          Citating Publication
        </span>
      </div>
    </div>

    <div class="bg-transparent absolute top-5 left-5 p-3 w-80 flex flex-col">
      <h2 class="font-sans text-lg text-gray-700 mb-0">Legend</h2>
      <div class="flex flex-row items-center">
        <div class="rounded-full w-3 h-3 bg-pink-600"></div>
        <span class="px-2 text-sm font-sans text-gray-700"> Filter </span>
      </div>
    </div>

    <div class="bg-transparent absolute top-5 right-3 p-3 w-3/12 flex flex-col">
      <h2 class="font-sans text-lg text-gray-700">{{ resource_type }} Title</h2>
      <span class="font-sans text-base text-gray-500 leading-none mb-2">
        {{ title }}
      </span>

      <h2 class="font-sans text-lg text-gray-700" v-if="award != ''">
        Award Number
      </h2>
      <span
        class="font-sans text-base text-gray-500 leading-none mb-2"
        v-if="award != ''"
      >
        {{ award }}
      </span>

      <h2
        class="font-sans text-lg text-gray-700"
        v-if="datasetDescription != ''"
      >
        Dataset Description
      </h2>
      <span
        class="font-sans text-base text-gray-500 leading-none mb-2"
        v-if="datasetDescription != ''"
      >
        {{ datasetDescription }}
      </span>

      <h2 class="font-sans text-lg text-gray-700" v-if="datasetTags.length > 0">
        Dataset Tags
      </h2>

      <div v-if="datasetTags.length > 0" class="mb-2">
        <span
          class="font-sans text-base text-gray-500 leading-none pr-2"
          v-for="(item, idx) in datasetTags"
          :key="idx"
        >
          {{ item }}
        </span>
      </div>
      <h2 class="font-sans text-lg text-gray-700">DOI</h2>

      <a :href="doi" target="_blank" class="p-0 leading-none">
        <span
          class="
            underline
            text-blue-500
            hover:text-blue-700
            text-base
            font-sans
            leading-none
            p-0
          "
          >{{ doi }}</span
        >
      </a>
    </div>
  </div>
</template>

<script>
const d3 = require("d3");
const axios = require("axios");
import { v4 as uuidv4 } from "uuid";

export default {
  name: "SparcLink",
  components: {},
  data() {
    return {
      radius: 4,
      organized_data: {},
      title: "",
      doi: "",
      award: "",
      datasetDescription: "",
      citationsRange: [],
      datasetTags: [],
      cite_max: 0,
      cite_min: 0,
      resource_type: "",
    };
  },
  methods: {
    getDoiURL: function (doi) {
      if (doi != "") {
        const http_pos = doi.search("http");
        if (http_pos != -1) {
          return doi;
        }
        const org_pos = doi.search("org");
        if (org_pos != -1) {
          const val = doi.substring(org_pos + 4);
          return `https://dx.doi.org/${val}`;
        }
        return `https://dx.doi.org/${doi}`;
      } else return "#";
    },
    drawCanvas: function () {
      const MAX = this.cite_max;
      const MIN = this.cite_min;
      const data = this.organized_data;
      const HEIGHT = 800;
      const WIDTH = 1300;

      var canvas = document.querySelector("canvas");
      let context = canvas.getContext("2d");

      const links = data.links.map((d) => Object.create(d));
      const nodes = data.nodes.map((d) => Object.create(d));

      const simulation = d3
        .forceSimulation(nodes)
        .force(
          "link",
          d3.forceLink(links).id((d) => d.id)
        )
        .force("x", d3.forceX())
        .force("y", d3.forceY())
        .force("charge", d3.forceManyBody().strength(-12))
        .force("center", d3.forceCenter(WIDTH / 2, HEIGHT / 2));

      simulation.nodes(nodes).on("tick", ticked);

      simulation.force("link").links(links);

      d3.select(canvas).call(
        d3
          .drag()
          .container(canvas)
          .subject(dragsubject)
          .on("start", dragstarted)
          .on("drag", dragged)
          .on("end", dragended)
      );

      function ticked() {
        context.clearRect(0, 0, WIDTH, HEIGHT);

        context.beginPath();
        links.forEach(drawLink);
        context.strokeStyle = "#aaa";
        context.stroke();

        context.beginPath();
        for (const node of nodes) {
          context.beginPath();
          drawNode(node);
          context.strokeStyle = "#C0C0C0";
          context.lineWidth = 1;
          context.fillStyle = node.color;
          context.fill();
          context.stroke();
        }
      }

      function dragsubject() {
        return simulation.find(d3.event.x, d3.event.y);
      }

      let that = this;
      function dragstarted() {
        if (!d3.event.active) simulation.alphaTarget(0.2).restart();
        d3.event.subject.fx = d3.event.subject.x;
        d3.event.subject.fy = d3.event.subject.y;

        let node = data.nodes[d3.event.subject.index];
        that.title = node.title;
        that.doi = that.getDoiURL(node.doi);

        if ("award" in node) {
          that.award = node.award;
        } else {
          that.award = "";
        }

        if ("awards" in node) {
          that.award = node.awards[0];
        } else {
          that.award = "";
        }

        if ("description" in node) {
          that.datasetDescription = node.description;
        } else {
          that.datasetDescription = "";
        }

        if ("tags" in node) {
          that.datasetTags = node.tags;
        } else {
          that.datasetTags = [];
        }

        switch (node.group) {
          case "sparc dataset":
            that.resource_type = "Dataset";
            break;
          case "sparc protocol":
            that.resource_type = "Protocol";
            break;
          case "sparc publication":
            that.resource_type = "Publication";
            break;
          case "non sparc publication":
            that.resource_type = "Publication";
            break;
          default:
            that.resource_type = node.group;
        }
      }

      function dragged() {
        d3.event.subject.fx = d3.event.x;
        d3.event.subject.fy = d3.event.y;
      }

      function dragended() {
        if (!d3.event.active) simulation.alphaTarget(0);
        d3.event.subject.fx = null;
        d3.event.subject.fy = null;
      }

      function drawLink(d) {
        context.moveTo(d.source.x, d.source.y);
        context.lineTo(d.target.x, d.target.y);
      }

      // const that = this;
      function drawNode(d) {
        let radius = 4;
        if ("citations" in d) {
          let minAllowed = 4;
          let maxAllowed = 18;
          let unscaledNum = d.computedCitations;
          radius = Math.ceil(
            ((maxAllowed - minAllowed) * (unscaledNum - MIN)) / (MAX - MIN) +
              minAllowed
          );
        }
        context.moveTo(d.x + radius, d.y);
        context.arc(d.x, d.y, radius, 0, 2 * Math.PI);
      }
    },
    organizeData: async function (database) {
      let data = { nodes: [], links: [] };

      let database_response = database["ikP4sIT5PJMWFNCKG5eof5RN2Em1"];
      // FIX ME uncomment awards and protocols
      //   let awards = database.Awards;
      let datasets = database_response.Datasets;
      let papers = database_response.Papers;
      let protocols = database_response.Protocols;

      let datasetmap = [];
      // Extract nodes from the datasets
      for (const item in datasets) {
        let obj = datasets[item];
        obj.ogKey = obj.doi;
        obj.id = item;
        obj.computedCitations = 0;
        obj.group = "sparc dataset";
        obj.color = "#FF0063";
        obj.title = obj.name;
        data.nodes.push(obj);
        datasetmap.push(item);
      }

      let protocolsmap = [];
      // Extract nodes from the datasets
      for (const item in protocols) {
        let obj = protocols[item];
        obj.ogKey = obj.doi;
        obj.id = item;
        obj.computedCitations = 0;
        obj.group = "sparc protocol";
        obj.color = "#00ff00";
        data.nodes.push(obj);
        protocolsmap.push(item);
      }

      let papersmap = [];
      // Extract nodes from the papers
      for (const item in papers) {
        let obj = papers[item];
        obj.ogKey = obj.doi;
        obj.id = item;
        obj.computedCitations = 0;
        if ("direct" in obj) {
          if (obj.direct) {
            obj.group = "sparc publication";
            obj.color = "#FF9000";
          } else {
            obj.group = "non sparc publication";
            obj.color = "#109CFF";
          }
        } else {
          obj.group = "non sparc publication";
          obj.color = "#109CFF";
        }
        papersmap.push(item);
        data.nodes.push(obj);
      }

      // Extract links from the papers
      for (const item in papers) {
        let obj = papers[item];

        if ("papers" in obj) {
          let connected_papers = obj.papers;
          connected_papers.forEach((paper) => {
            let link_obj = {};
            link_obj.id = uuidv4();

            if (papersmap.includes(item) && papersmap.includes(paper)) {
              link_obj.source = paper;
              link_obj.target = item;
              data.links.push(link_obj);
            }
          });
        }

        if ("datasets" in obj) {
          let connected_datasets = obj.datasets;
          connected_datasets.forEach((dataset) => {
            let link_obj = {};
            link_obj.id = uuidv4();

            if (papersmap.includes(item) && datasetmap.includes(dataset)) {
              link_obj.source = item;
              link_obj.target = dataset;
              data.links.push(link_obj);
            }
          });
        }

        if ("protocols" in obj) {
          let connected_protocols = obj.protocols;
          connected_protocols.forEach((protocol) => {
            let link_obj = {};
            link_obj.id = uuidv4();

            if (papersmap.includes(item) && protocolsmap.includes(protocol)) {
              link_obj.source = item;
              link_obj.target = protocol;
              data.links.push(link_obj);
            }
          });
        }
      }

      // Extract links from the datasets
      for (const item in datasets) {
        let obj = datasets[item];

        if ("protocols" in obj) {
          let connected_protocols = obj.protocols;
          connected_protocols.forEach((protocol) => {
            let link_obj = {};
            link_obj.id = uuidv4();

            if (datasetmap.includes(item) && protocolsmap.includes(protocol)) {
              link_obj.source = item;
              link_obj.target = protocol;
              data.links.push(link_obj);
            }
          });
        }
      }

      // get citations count
      data.links.forEach((link) => {
        let source = link.source;
        data.nodes.forEach((node) => {
          if (node.id == source) {
            node.computedCitations = node.computedCitations + 1;
          }
        });
      });

      data.nodes.forEach((node) => {
        this.citationsRange.push(node.computedCitations);
      });

      this.cite_max = Math.max.apply(Math, this.citationsRange);
      this.cite_min = Math.min.apply(Math, this.citationsRange);

      return data;
    },
    createViz: async function () {
      let database_response = [];
      database_response = await axios.get(
        "https://sparclink-f151d-default-rtdb.firebaseio.com/.json"
      );
      database_response = database_response.data;

      this.organized_data = await this.organizeData(database_response);

      this.drawCanvas();
    },
  },
  mounted() {
    this.createViz();
  },
};
</script>

<style lang="postcss" scoped>
.li-item:before {
  content: "";
  background-color: red;
  border-color: white;
  border-radius: 50%;
  border-width: 5px;
  height: 25px;
  width: 25px;
}
</style>
