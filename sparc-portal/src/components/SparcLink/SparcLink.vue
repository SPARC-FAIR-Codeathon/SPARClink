<template>
  SPARClink
  <div id="svg_container" class="border-1 border-gray-100"></div>
  container2
  <div id="svg_container2" class="border-1 border-gray-100"></div>
</template>

<script>
const d3 = require("d3");
const axios = require("axios");

import { v4 as uuidv4 } from "uuid";

export default {
  name: "SparcLink",
  methods: {
    test2: function (data) {
      const height = 680;
      const width = 1800;

      const links = data.links.map((d) => Object.create(d));
      const nodes = data.nodes.map((d) => Object.create(d));

      // const svg = d3.create("svg")
      //     .attr("viewBox", [-width / 2, -height / 2, width, height]);
      const radius = 5;
      var svg = d3
        .select("#svg_container2")
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

      function dragstarted(d) {
        console.log("test", d3);
        if (!d3.event.active) simulation.alphaTarget(1).restart();
        d.fx = d.x;
        d.fy = d.y;
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

      // function color() {
      //   const scale = d3.scaleOrdinal(d3.schemeCategory10);
      //   return (d) => scale(d.group);
      // }

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
        .attr("r", radius)
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
        console.log(obj.originatingArticle)
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
      //   console.log(database_response);

      const organized_data = await this.organizeData(database_response);

      this.test2(organized_data);
    },
  },
  mounted() {
    this.createViz();

    // test();
  },
};
</script>

<style></style>
