<template>
  <!-- legend -->
  <div
    class="border border-gray-500 flex flex-row justify-center relative"
    style="min-height: 200px"
  >
    <div class="flex flex-col items-center">
      <canvas width="1300" height="800"></canvas>
      <p v-if="filter_words != ''" class="my-5 font-sans text-lg">
        Filtering by <span class="font-sans text-base text-gray-600"> {{ filter_words }} </span>
      </p>
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

    <!-- Left controls panel -->
    <div
      class="
        bg-transparent
        absolute
        bottom-5
        left-5
        p-3
        w-80
        flex flex-col
        divide-y divide-gray-300
      "
    >
      <div id="svgContainer" class="pb-5"></div>
      <div class="py-3">
        <h2 class="font-sans text-lg text-gray-700 mb-0">Filter the graph</h2>
        <div class="flex flex-row items-center">
          <input
            placeholder=" Filter keywords"
            ref="filterInput"
            v-model="filterInput"
            @input="filterByInput"
            class="border border-gray-700 p-1"
          />
        </div>
      </div>
      <div class="py-3">
        <div class="flex flex-row items-center">
          <label class="font-sans text-lg text-gray-700 mr-4">
            Remove unconnected nodes
          </label>
          <input
            type="checkbox"
            id="checkbox"
            v-model="filterLonely"
            @change="filterByLonely"
          />
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
            @change="filterByNodes"
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
            @change="filterByNodes"
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
            @change="filterByNodes"
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
            @change="filterByNodes"
          />
          <label class="font-sans text-base text-gray-700 ml-2">
            Citing Publications
          </label>
        </div>
      </div>
    </div>

    <!-- node details window -->
    <div class="bg-transparent absolute top-5 right-2 p-3 w-3/12 flex flex-col">
      <h2 class="font-sans text-lg text-gray-700" v-if="title != ''">
        {{ resource_type }} Title
      </h2>
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

      <h2 class="font-sans text-lg text-gray-700" v-if="computedCitations != 0">
        Number of cited components:
        <span class="font-sans text-base text-gray-500 leading-none mb-2">
          {{ computedCitations }}
        </span>
      </h2>

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
      <h2 class="font-sans text-lg text-gray-700" v-if="doi != ''">DOI</h2>

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

    <!-- top ranked window -->
    <div
      class="bg-transparent absolute bottom-5 right-2 p-3 w-3/12 flex flex-col"
    >
      <h2
        class="font-sans text-lg text-gray-700"
        v-if="topRankedMaterial.length > 0 || loadingSpinner"
      >
        Top 10 ranked items for filter terms
      </h2>

      <div class="flex items-center" v-if="loadingSpinner">
        <div
          class="
            animate-spin
            rounded-full
            h-24
            w-24
            my-10
            border-t-2 border-b-2 border-purple-500
          "
        ></div>
      </div>

      <div
        v-if="!loadingSpinner"
        class="mb-2 flex flex-col divide-y divide-gray-200 h-60 overflow-auto"
      >
        <div v-for="item in topRankedMaterial" :key="item.id" class="py-2 mr-6">
          <h3 class="text-base font-sans">Title</h3>
          <span class="text-sm font-sans">
            {{ item.title }}
          </span>
          <h3 class="text-sm">
            DOI:
            <a
              :href="getDoiURL(item.doi)"
              target="_blank"
              class="p-0 leading-none"
            >
              <span
                class="
                  underline
                  text-blue-500
                  hover:text-blue-700
                  text-sm
                  font-sans
                  leading-none
                  p-0
                "
              >
                {{ item.doi }}
              </span>
            </a>
          </h3>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
const d3 = require("d3");
const axios = require("axios");
import { v4 as uuidv4 } from "uuid";
import cloud from "d3-cloud";

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
      computedCitations: 0,
      datasetTags: [],
      cite_max: 0,
      cite_min: 0,
      filterInput: "",
      strength: -12,
      resource_type: "",
      citationsRange: [],
      topRankedMaterial: [],
      simulation: "",
      filterLonely: false,
      filterNodes: [],
      loadingSpinner: false,
      filter_words: "",
    };
  },
  methods: {
    generateWorldCloudData: function (data) {
      let sentences = [];
      data.nodes.forEach((node) => {
        if ("title" in node) {
          sentences.push(node.title);
        }

        if ("description" in node) {
          sentences.push(node.description);
        }

        if ("tags" in node) {
          node.tags.forEach((item) => {
            sentences.push(item);
          });
        }
      });

      let config = {
        method: "post",
        url: "https://megasanjay.pythonanywhere.com/wordcloud",
        headers: {
          "Content-Type": "application/json",
        },
        data: JSON.stringify({ sentences: sentences }),
      };

      let that = this;

      axios(config, that)
        .then(function (response) {
          let res = response.data.counters;

          let keywords = [];
          let values = [];

          res.forEach((item, idx) => {
            if (idx > 30 || item[0] == "") {
              return;
            }
            keywords.push(item[0]);
            values.push(item[1]);
          });

          function normalize(min, max) {
            var delta = max - min;
            return function (val) {
              return (val - min) / delta;
            };
          }

          const MAX = Math.max(...values);
          const MIN = Math.min(...values);

          values = values.map(normalize(MIN, MAX));

          that.generateWordCloud(keywords, values);
        })
        .catch(function (error) {
          console.log(error);
        });
    },
    generateWordCloud: function (keywords, values) {
      const CLOUD_SIZE = [300, 250];
      const that = this;

      const fontFamily = "Asap, Verdana, Arial, Helvetica, sans-serif";

      var layout = cloud()
        .size(CLOUD_SIZE)
        .words(
          keywords.map(function (d, i) {
            return { text: d, size: 10 + values[i] * 90 };
          })
        )
        .padding(5)
        .rotate(0)
        .font(fontFamily)
        .fontSize(function (d) {
          return d.size;
        })
        .on("end", draw);

      layout.start();

      function handleMouseOver(d) {
        d3.select(this)
          .classed("word-hovered", true)
          .transition(`mouseover-${d.text}`)
          .duration(300)
          .style("font-size", d.size + 10 + "px");
      }

      function handleMouseOut(d) {
        d3.select(this)
          .classed("word-hovered", false)
          .interrupt(`mouseover-${d.text}`)
          .style("font-size", d.size);
      }

      function draw(words) {
        let container = d3.select("#svgContainer");
        container.selectAll("*").remove();
        container
          .append("svg")
          .attr("width", layout.size()[0])
          .attr("height", layout.size()[1])
          .append("g")
          .attr(
            "transform",
            "translate(" +
              layout.size()[0] / 2 +
              "," +
              layout.size()[1] / 2 +
              ")"
          )
          .selectAll("text")
          .data(words)
          .enter()
          .append("text")
          .classed("word-default", true)
          .style("font-size", function (d) {
            return d.size + "px";
          })
          .style("font-family", fontFamily)
          .attr("text-anchor", "middle")
          .attr("transform", function (d) {
            return "translate(" + [d.x, d.y] + ")rotate(" + d.rotate + ")";
          })
          .text(function (d) {
            return d.text;
          })
          .on("mouseover", handleMouseOver)
          .on("mouseout", handleMouseOut)
          .on("click", function (d) {
            that.addItemToFilter(d.text);
          });
      }
    },
    addItemToFilter(keywordPhrase) {
      this.filterInput += ` ${keywordPhrase}`;
      this.filterByInput();
    },
    filterByNodes: function () {
      this.filterInput = "";
      this.filterLonely = false;
      this.loadingSpinner = false;
      this.topRankedMaterial = [];
      this.simulation.stop();

      const val = this.filterNodes;

      if (val.length == 0) {
        this.drawCanvas();
      } else {
        let data = JSON.parse(JSON.stringify(this.organized_data));

        let keepList = [];

        data.nodes.forEach((node) => {
          let keepFlag = false;
          if (val.includes(node.group)) {
            keepFlag = true;
          }
          if (keepFlag) {
            if (!keepList.includes(node.id)) {
              keepList.push(node.id);
            }
          }
        });

        this.filtered_data = { nodes: [], links: [] };
        data.nodes.forEach((node) => {
          if (keepList.includes(node.id)) {
            node.computedCitations = 0;
            this.filtered_data.nodes.push(node);
          }
        });
        data.links.forEach((link) => {
          if (
            keepList.includes(link.source) &&
            keepList.includes(link.target)
          ) {
            this.filtered_data.links.push(link);
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
    filterByLonely: function () {
      this.filterInput = "";
      this.filterNodes = [];
      this.loadingSpinner = false;
      this.topRankedMaterial = [];
      this.simulation.stop();

      const val = this.filterLonely;

      if (!val) {
        this.drawCanvas();
      } else {
        let data = JSON.parse(JSON.stringify(this.organized_data));

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
    filterByInput: function () {
      this.filterLonely = false;
      this.filterNodes = [];
      this.simulation.stop();

      const val = this.filterInput.trim();

      if (val == "") {
        this.loadingSpinner = false;
        this.topRankedMaterial = [];
        this.filter_words = ""
        this.drawCanvas();
      } else {
        let filter_words = val.split(" ");
        filter_words = filter_words.filter((word) => word != "");

        let data = JSON.parse(JSON.stringify(this.organized_data));

        let removeList = [];

        let requestData = JSON.stringify({
          inputString: val,
          fullModel: false,
          recommendation: true,
        });

        let config = {
          method: "post",
          url: "https://megasanjay.pythonanywhere.com/sparcsearch",
          headers: {
            "Content-Type": "application/json",
          },
          data: requestData,
        };

        let that = this;

        this.loadingSpinner = true;
        this.topRankedMaterial = [];
        axios(config)
          .then(function (response) {
            const topRanked = response.data.topRanked;
            const correctTerms = response.data.cs; //spelling corrected
            const topRankedIds = topRanked.slice(0, 10);

            that.topRankedMaterial = [];
            console.log(correctTerms);
            filter_words = correctTerms;
            that.filter_words = correctTerms.join(", ");

            topRankedIds.forEach((item) => {
              data.nodes.forEach((node) => {
                if (node.id == item) {
                  let obj = node;
                  that.topRankedMaterial.push(obj);
                }
              });
            });

            that.loadingSpinner = false;

            data.nodes.forEach((item) => {
              let removeFlag = true;
              if ("tags" in item) {
                item.tags.forEach((tag) => {
                  filter_words.forEach((word) => {
                    if (tag.search(word) != -1) {
                      // console.log("Found in tag", item.id);
                      removeFlag = false;
                    }
                  });
                });
              }
              if ("title" in item) {
                filter_words.forEach((word) => {
                  if (item.title.search(word) != -1) {
                    // console.log("Found in title", item.id);
                    removeFlag = false;
                  }
                });
              }
              if ("description" in item) {
                filter_words.forEach((word) => {
                  if (item.description.search(word) != -1) {
                    // console.log("Found in description", item.id);
                    removeFlag = false;
                  }
                });
              }
              if ("author_list" in item) {
                filter_words.forEach((word) => {
                  if (item["author_list"].search(word) != -1) {
                    // console.log("Found in author_list", item.id);
                    removeFlag = false;
                  }
                });
              }
              if ("url" in item) {
                filter_words.forEach((word) => {
                  if (item.url.search(word) != -1) {
                    // console.log("Found in url", item.id);
                    removeFlag = false;
                  }
                });
              }
              if ("journal" in item) {
                filter_words.forEach((word) => {
                  if (item.journal.search(word) != -1) {
                    // console.log("Found in journal", item.id);
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

            that.filtered_data = { nodes: [], links: [] };
            data.nodes.forEach((item) => {
              if (!removeList.includes(item.id)) {
                item.computedCitations = 0;
                that.filtered_data.nodes.push(item);
              }
            });
            data.links.forEach((item) => {
              if (
                !(
                  removeList.includes(item.source) ||
                  removeList.includes(item.target)
                )
              ) {
                that.filtered_data.links.push(item);
              }
            });

            // get citations count
            that.filtered_data.links.forEach((link) => {
              let source = link.source;
              that.filtered_data.nodes.forEach((node) => {
                if (node.id == source) {
                  node.computedCitations = node.computedCitations + 1;
                }
              });
            });

            let citationsRange = [];
            that.filtered_data.nodes.forEach((node) => {
              citationsRange.push(node.computedCitations);
            });

            that.cite_max = Math.max.apply(Math, citationsRange);
            that.cite_min = Math.min.apply(Math, citationsRange);

            if (
              that.filtered_data.nodes.length <
              that.organized_data.nodes.length * 0.6
            ) {
              that.strength = -30;
            } else {
              that.strength = -12;
            }

            that.drawCanvas(true);
          })
          .catch(function (error) {
            console.log(error);
            that.loadingSpinner = false;
          });
      }
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
      this.generateWorldCloudData(data);

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
            that.resource_type = "";
        }

        if ("computedCitations" in node) {
          that.computedCitations = node.computedCitations;
        } else {
          that.computedCitations = 0;
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
      // Extract nodes from the protocols
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

.word-hovered {
  @apply cursor-pointer;
}

/* width */
::-webkit-scrollbar {
  width: 4px;
}
/* button */
::-webkit-scrollbar-button {
  background: rgba(220, 222, 224, 0.849);
}
/* Handle */
::-webkit-scrollbar-thumb {
  background: rgb(155, 152, 152);
}
/* Handle on hover */
::-webkit-scrollbar-thumb:hover {
  background: rgb(115, 117, 117);
}
/* Track */
::-webkit-scrollbar-track {
  background: rgba(220, 222, 224, 0.849);
}
/* The track NOT covered by the handle. */
::-webkit-scrollbar-track-piece {
  background: rgba(220, 222, 224, 0.849);
}
/* Corner */
::-webkit-scrollbar-corner {
  background: rgba(220, 222, 224, 0.849);
}
/* Resizer */
::-webkit-resizer {
  background: rgba(220, 222, 224, 0.849);
}
</style>
