<template>
  <div
    id="svg_container"
    class="border border-gray-500 flex flex-row justify-center relative"
    style="min-height: 200px"
  >
    <div id="svg-container" ref="svgContainer"></div>
    <div class="bg-transparent absolute bottom-5 right-5 p-3 w-2/12">
      control {{ testgroup }}
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
    return { radius: 4, organized_data: {}, testgroup: "", citationsRange: [] };
  },
  methods: {
    test2: function () {
      const data = this.organized_data;
      const height = 800;
      const width = 1300;

      const links = data.links.map((d) => Object.create(d));
      const nodes = data.nodes.map((d) => Object.create(d));

      var svg = d3
        .select("#svg-container")
        .append("svg")
        .attr("width", width)
        .attr("height", height)
        .attr("viewBox", [-width / 2, -height / 2, width, height]);

      const simulation = d3
        .forceSimulation(nodes)
        .force(
          "link",
          d3.forceLink(links).id((d) => d.id)
        )
        .force("charge", d3.forceManyBody().strength(-11))
        .force("x", d3.forceX())
        .force("y", d3.forceY());

      const link = svg
        .append("g")
        .attr("stroke", "#C0C0C0")
        .attr("stroke-opacity", 0.6)
        .selectAll("line")
        .data(links)
        .join("line");

      // function test(idx) {
      //   this.testgroup = idx.author_list;
      // }

      let that = this;
      function dragstarted(d) {
        if (!d3.event.active) simulation.alphaTarget(1).restart();
        d.fx = d.x;
        d.fy = d.y;
        let x = data.nodes[d.index];
        console.log(x);
        console.log(x.author_list);
        that.testgroup = x.author_list;
      }

      function dragged(d) {
        d.fx = d3.event.x;
        d.fy = d3.event.y;
      }

      function dragended(d) {
        if (!d3.event.active) simulation.alphaTarget(0);
        d.fx = null;
        d.fy = null;
      }

      const node = svg
        .append("g")
        .attr("stroke", "#C0C0C0")
        .attr("stroke-width", 1)
        .selectAll("circle")
        .data(nodes)
        .join("circle")
        .attr("fill", (d) => {
          return d.color;
        })
        .attr("r", (d) => {
          if ("citations" in d) {
            let minAllowed = 4;
            let maxAllowed = 15;
            let unscaledNum = d.computedCitations;
            let max = Math.max.apply(Math, this.citationsRange);
            let min = Math.min.apply(Math, this.citationsRange);
            // console.log(unscaledNum);
            return Math.ceil(
              ((maxAllowed - minAllowed) * (unscaledNum - min)) / (max - min) +
                minAllowed
            );
            // return d.citations;
          } else {
            return this.radius;
          }
        })
        .call(
          d3
            .drag()
            .on("start", dragstarted)
            .on("drag", dragged)
            .on("end", dragended)
        );

      node.append("title").text((d) => {
        return d.doi;
      });

      simulation.on("tick", () => {
        link
          .attr("x1", (d) => d.source.x)
          .attr("y1", (d) => d.source.y)
          .attr("x2", (d) => d.target.x)
          .attr("y2", (d) => d.target.y);

        node.attr("cx", (d) => d.x).attr("cy", (d) => d.y);
      });
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
        if ("protocols" in papers[item]) {
          console.log(item);
        }
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

      return data;
    },
    createViz: async function () {
      let database_response = [];
      database_response = await axios.get(
        "https://sparclink-f151d-default-rtdb.firebaseio.com/.json"
      );
      database_response = database_response.data;

      this.organized_data = await this.organizeData(database_response);

      this.test2();
    },
  },
  mounted() {
    this.createViz();
  },
};
</script>

<style></style>
