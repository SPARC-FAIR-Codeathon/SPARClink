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
          Citing Publication
        </span>
      </div>
    </div>

    <div
      class="
        bg-transparent
        absolute
        bottom-5
        left-5
        p-3
        w-80
        flex flex-col
        divide-y-2
      "
    >
      <div class="py-3">
        <h2 class="font-sans text-lg text-gray-700 mb-0">Filter the graph</h2>
        <div class="flex flex-row items-center">
          <input
            placeholder=" Filter keywords"
            ref="filterInput"
            v-model="filterInput"
            class="border border-gray-700 p-1"
          />
        </div>
      </div>
      <div class="py-3">
        <div class="flex flex-row items-center">
          <label class="font-sans text-lg text-gray-700 mr-4">
            Remove unconnected nodes
          </label>
          <input type="checkbox" id="checkbox" v-model="filterLonely" />
        </div>
      </div>
      <div class="py-3">
        <h2 class="font-sans text-lg text-gray-700 mb-0">Filter nodes</h2>
        <div class="flex flex-row items-center pr-3">
          <input
            type="checkbox"
            id="filterNodes"
            value="sparc dataset"
            v-model="filterNodes"
          />
          <label class="font-sans text-base text-gray-700 ml-2">
            SPARC Datasets
          </label>
        </div>
        <div class="flex flex-row items-center pr-3">
          <input
            type="checkbox"
            id="filterNodes"
            value="sparc publication"
            v-model="filterNodes"
          />
          <label class="font-sans text-base text-gray-700 ml-2">
            SPARC Publications
          </label>
        </div>
        <div class="flex flex-row items-center pr-3">
          <input
            type="checkbox"
            id="filterNodes"
            value="sparc protocol"
            v-model="filterNodes"
          />
          <label class="font-sans text-base text-gray-700 ml-2">
            SPARC Protocols
          </label>
        </div>
        <div class="flex flex-row items-center pr-3">
          <input
            type="checkbox"
            id="filterNodes"
            value="non sparc publication"
            v-model="filterNodes"
          />
          <label class="font-sans text-base text-gray-700 ml-2">
            Citing Publications
          </label>
        </div>
      </div>
    </div>

    <!-- node details window -->
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
// import Tagify from "@yaireo/tagify";
import { v4 as uuidv4 } from "uuid";
// import "@yaireo/tagify/dist/tagify.css";

export default {
  name: "SparcLink",
  components: {},
  data() {
    return {
      radius: 4,
      organized_data: {},
      filtered_data: {},
      title: "",
      doi: "",
      award: "",
      datasetDescription: "",
      datasetTags: [],
      cite_max: 0,
      cite_min: 0,
      filterInput: "",
      strength: -12,
      resource_type: "",
      citationsRange: [],
      simulation: "",
      filterLonely: false,
      filterNodes: [],
    };
  },
  watch: {
    filterInput: function (val) {
      this.filterLonely = false;
      val = val.trim();
      this.simulation.stop();
      if (val == "") {
        this.drawCanvas();
      } else {
        const filter_words = val.split(" ");
        let data = this.organized_data;

        let removeList = [];

        data.nodes.forEach((item) => {
          let removeFlag = true;
          if ("tags" in item) {
            item.tags.forEach((tag) => {
              filter_words.forEach((word) => {
                if (tag.search(word) != -1) {
                  removeFlag = false;
                }
              });
            });
          }
          if ("title" in item) {
            filter_words.forEach((word) => {
              if (item.title.search(word) != -1) {
                removeFlag = false;
              }
            });
          }
          if ("description" in item) {
            filter_words.forEach((word) => {
              if (item.description.search(word) != -1) {
                removeFlag = false;
              }
            });
          }
          if ("author_list" in item) {
            filter_words.forEach((word) => {
              if (item["author_list"].search(word) != -1) {
                removeFlag = false;
              }
            });
          }
          if ("url" in item) {
            filter_words.forEach((word) => {
              if (item.url.search(word) != -1) {
                removeFlag = false;
              }
            });
          }
          if ("journal" in item) {
            filter_words.forEach((word) => {
              if (item.journal.search(word) != -1) {
                removeFlag = false;
              }
            });
          }
          if (removeFlag == true) {
            if (!removeList.includes(item.id)) {
              removeList.push(item.id);
            }
          }
        });

        this.filtered_data = { nodes: [], links: [] };
        data.nodes.forEach((item) => {
          if (!removeList.includes(item.id)) {
            item.computedCitations = 0;
            this.filtered_data.nodes.push(item);
          }
        });
        data.links.forEach((item) => {
          if (
            !(
              removeList.includes(item.source) ||
              removeList.includes(item.target)
            )
          ) {
            this.filtered_data.links.push(item);
          }
        });

        // get citations count
        this.filtered_data.links.forEach((link) => {
          let source = link.source;
          this.filtered_data.nodes.forEach((node) => {
            if (node.id == source) {
              node.computedCitations = node.computedCitations + 1;
            }
          });
        });

        let citationsRange = [];
        this.filtered_data.nodes.forEach((node) => {
          citationsRange.push(node.computedCitations);
        });

        this.cite_max = Math.max.apply(Math, citationsRange);
        this.cite_min = Math.min.apply(Math, citationsRange);

        if (
          this.filtered_data.nodes.length <
          this.organized_data.nodes.length * 0.6
        ) {
          this.strength = -30;
        } else {
          this.strength = -12;
        }

        this.drawCanvas(true);
      }
    },
    filterLonely: function (val) {
      this.filterInput = "";
      this.simulation.stop();
      if (!val) {
        this.drawCanvas();
      } else {
        let data = this.organized_data;

        let keepList = [];

        data.links.forEach((item) => {
          if (!keepList.includes(item.source)) {
            keepList.push(item.source);
          }
          if (!keepList.includes(item.target)) {
            keepList.push(item.target);
          }
        });

        this.filtered_data = { nodes: [], links: [] };
        data.nodes.forEach((item) => {
          if (keepList.includes(item.id)) {
            item.computedCitations = 0;
            this.filtered_data.nodes.push(item);
          }
        });
        data.links.forEach((item) => {
          this.filtered_data.links.push(item);
        });

        if (
          this.filtered_data.nodes.length <
          this.organized_data.nodes.length * 0.6
        ) {
          this.strength = -30;
        } else {
          this.strength = -12;
        }

        // get citations count
        this.filtered_data.links.forEach((link) => {
          let source = link.source;
          this.filtered_data.nodes.forEach((node) => {
            if (node.id == source) {
              node.computedCitations = node.computedCitations + 1;
            }
          });
        });

        let citationsRange = [];
        this.filtered_data.nodes.forEach((node) => {
          citationsRange.push(node.computedCitations);
        });

        this.cite_max = Math.max.apply(Math, citationsRange);
        this.cite_min = Math.min.apply(Math, citationsRange);

        this.drawCanvas(true);
      }
    },
    filterNodes: function (val) {
      this.filterInput = "";
      this.filterLonely = false;
      this.simulation.stop();

      if (val.length == 0) {
        this.drawCanvas();
      } else {
        let data = this.organized_data;

        let keepList = [];

        data.nodes.forEach((node) => {
          let keepFlag = false;
          if (val.includes(node.group)) {
            keepFlag = true;
          }
          if (keepFlag == true) {
            if (!keepList.includes(node.id)) {
              keepList.push(node.id);
            }
          }
        });

        this.filtered_data = { nodes: [], links: [] };
        data.nodes.forEach((item) => {
          if (keepList.includes(item.id)) {
            item.computedCitations = 0;
            this.filtered_data.nodes.push(item);
          }
        });
        data.links.forEach((item) => {
          if (
            keepList.includes(item.source) &&
            keepList.includes(item.target)
          ) {
            this.filtered_data.links.push(item);
          }
        });

        // get citations count
        this.filtered_data.links.forEach((link) => {
          let source = link.source;
          this.filtered_data.nodes.forEach((node) => {
            if (node.id == source) {
              node.computedCitations = node.computedCitations + 1;
            }
          });
        });

        let citationsRange = [];
        this.filtered_data.nodes.forEach((node) => {
          citationsRange.push(node.computedCitations);
        });

        this.cite_max = Math.max.apply(Math, citationsRange);
        this.cite_min = Math.min.apply(Math, citationsRange);

        if (
          this.filtered_data.nodes.length <
          this.organized_data.nodes.length * 0.6
        ) {
          this.strength = -30;
        } else {
          this.strength = -12;
        }

        this.drawCanvas(true);
      }
    },
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
    drawCanvas: function (filtered = false) {
      let data;
      if (!filtered) {
        this.cite_max = Math.max.apply(Math, this.citationsRange);
        this.cite_min = Math.min.apply(Math, this.citationsRange);
        data = JSON.parse(JSON.stringify(this.organized_data));
        this.strength = -12;
      } else {
        data = JSON.parse(JSON.stringify(this.filtered_data));
      }

      const MAX = this.cite_max;
      const MIN = this.cite_min;
      const HEIGHT = 800;
      const WIDTH = 1300;

      var canvas = document.querySelector("canvas");
      let context = canvas.getContext("2d");

      const links = data.links.map((d) => Object.create(d));
      const nodes = data.nodes.map((d) => Object.create(d));
     
      this.simulation = d3
        .forceSimulation(nodes)
        .force(
          "link",
          d3.forceLink(links).id((d) => d.id)
        )
        .force("x", d3.forceX())
        .force("y", d3.forceY())
        .force("charge", d3.forceManyBody().strength(this.strength))
        .force("center", d3.forceCenter(WIDTH / 2, HEIGHT / 2));

      this.simulation.nodes(nodes).on("tick", ticked);

      this.simulation.force("link").links(links);

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
        return that.simulation.find(d3.event.x, d3.event.y);
      }

      let that = this;
      function dragstarted() {
        if (!d3.event.active) that.simulation.alphaTarget(0.2).restart();
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
        if (!d3.event.active) that.simulation.alphaTarget(0);
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
          let maxAllowed = 15;
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
    // this.tagify = new Tagify(this.$refs.filterInput, {});
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
