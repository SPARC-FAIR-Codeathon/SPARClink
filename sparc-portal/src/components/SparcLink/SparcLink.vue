<template>
  <div
    id="svg_container"
    class="border border-gray-500 flex flex-row justify-center relative"
    style="min-height: 200px"
  >
    <div id="svg-container" ref="svgContainer"></div>
    <div class="bg-gray-50 absolute bottom-5 right-5 p-3 w-1/12">
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
    return { radius: 5, organized_data: {}, testgroup: "" };
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
        .attr("r", this.radius)
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

      let database_response = database["czPp6z6JCxXIrlMCmTiGyIX7y913"];
      // FIX ME uncomment awards and protocols
      //   let awards = database.Awards;
      let datasets = database_response.Datasets;
      let papers = database_response.Papers;
      // let protocols = database.Protocols;

      let datasetmap = [];
      // Extract nodes from the datasets
      for (const item in datasets) {
        let obj = datasets[item];
        obj.ogKey = obj.doi;
        obj.id = item;
        obj.group = "sparc dataset";
        obj.color = "#FF0063";
        data.nodes.push(obj);
        datasetmap.push(item);
      }

      let papersmap = [];
      // Extract nodes from the papers
      for (const item in papers) {
        let obj = papers[item];
        obj.ogKey = obj.doi;
        obj.id = item;
        if ("awards" in obj) {
          obj.group = "sparc publication";
          obj.color = "#FF9000";
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
              link_obj.source = item;
              link_obj.target = paper;
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
      }

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
