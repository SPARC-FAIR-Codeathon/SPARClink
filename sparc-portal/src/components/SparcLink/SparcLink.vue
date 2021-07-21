<template>
  SPARClink
  <div id="svg_container" class="border-1 border-gray-100"></div>
  container2
  <div id="svg_container2" class="border-1 border-gray-100"></div>
</template>

<script>
const d3 = require("d3");
import { event as currentEvent } from "d3-selection";

function test() {
  const people = [
    {
      value: "Food lovers",
      color: "#2d3e50",
    },
    {
      value: "Pasta lovers",
      color: "#b97ebb",
    },
    {
      value: "Pizza lovers",
      color: "#3bbc9b",
    },
  ];

  const height = 500;
  const width = 1000;

  const data = d3.range(80).map((d, idx) => ({
    id: idx,
    type: people[~~d3.randomUniform(3)()],
    radius: ~~d3.randomUniform(5, 15)(),
  }));

  var svg = d3
    .select("#svg_container")
    .append("svg")
    .attr("width", width)
    .attr("height", height);

  svg
    .append("circle")
    .attr("id", "category_1")
    .attr("r", height / 3)
    .attr("cx", width / 2.8)
    .attr("cy", height / 2)
    .attr("fill", "#3bbc9b")
    .attr("fill-opacity", 0.1)
    .attr("stroke", "#3bbc9b")
    .attr("stroke-opacity", 0.5)
    .attr("opacity", 0);

  svg
    .append("circle")
    .attr("id", "category_2")
    .attr("r", height / 3)
    .attr("cx", width / 1.8)
    .attr("cy", height / 2)
    .attr("fill", "#b97ebb")
    .attr("fill-opacity", 0.1)
    .attr("stroke", "#b97ebb")
    .attr("stroke-opacity", 0.5)
    .attr("opacity", 0);

  const nodeGroup = svg.append("g").attr("id", "nodes");

  let simulation = d3.forceSimulation();

  simulation = simulation
    .force("collide", d3.forceCollide((d) => d.radius + 3).iterations(12))
    .force("charge", d3.forceManyBody())
    .velocityDecay(0.5)
    .force("center", d3.forceCenter(width / 2, height / 2))
    .force("y", d3.forceY(0))
    .force("x", d3.forceX(0));

  const ticked = () => {
    nodeGroup
      .selectAll("circle")
      .attr("cx", (d) => d.x)
      .attr("cy", (d) => d.y);
  };

  simulation.nodes(data).on("tick", ticked);

  function draw() {
    const node = nodeGroup
      .selectAll("circle")
      .data(simulation.nodes(), (d) => d.id)
      .enter()
      .append("circle")
      .attr("r", (d) => d.radius)
      .attr("fill", (d) => d.type.color)
      .call(
        d3
          .drag()
          .on("start", dragstarted)
          .on("drag", dragged)
          .on("end", dragended)
      );

    node
      .attr("r", (d) => d.radius)
      .attr("fill", (d) => d.type.color)
      .call(
        d3
          .drag()
          .on("start", dragstarted)
          .on("drag", dragged)
          .on("end", dragended)
      );
  }

  draw();

  function split() {
    simulation
      .force(
        "left",
        isolate(
          d3.forceX(width / 3).strength(0.3),
          (d) => d.type.value === "Pizza lovers"
        )
      )
      .force(
        "center",
        isolate(
          d3.forceX(width / 2.2).strength(0.3),
          (d) => d.type.value === "Food lovers"
        )
      )
      .force(
        "right",
        isolate(
          d3.forceX(width / 1.7).strength(0.3),
          (d) => d.type.value === "Pasta lovers"
        )
      )
      .force("x", null)
      .force("y", d3.forceY(height / 2).strength(0.3));

    svg
      .select("#category_1")
      .transition()
      .delay(1000)
      .duration(1000)
      .attr("opacity", 1);

    svg
      .select("#category_2")
      .transition()
      .delay(1000)
      .duration(1000)
      .attr("opacity", 1);
  }

  function isolate(force, filter) {
    let initialize = force.initialize;
    force.initialize = function () {
      initialize.call(force, data.filter(filter));
    };
    return force;
  }

  function dragstarted(d) {
    console.log(d3);
    console.log(currentEvent);
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

  console.log(split);
}

async function test2() {
  const data = await d3.json(
    "https://gist.githubusercontent.com/lodilas/613d35c4fbf91bb6892ecf0a4ff151a7/raw/4ca473162fccd8db1a8e0fbe22bf8542eaab3f94/JAS_2009-2018_neu.json"
  );
  console.log(data);

  const height = 680;
  const width = 1000;

  const links = data.links.map((d) => Object.create(d));
  const nodes = data.nodes.map((d) => Object.create(d));

  // const svg = d3.create("svg")
  //     .attr("viewBox", [-width / 2, -height / 2, width, height]);

  var svg = d3.select("#svg_container2")
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
    .force("charge", d3.forceManyBody())
    .force("x", d3.forceX())
    .force("y", d3.forceY());

  const link = svg
    .append("g")
    .attr("stroke", "#999")
    .attr("stroke-opacity", 0.6)
    .selectAll("line")
    .data(links)
    .join("line");

  function dragstarted(d) {
    console.log(d3);
    console.log(currentEvent);
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

  const node = svg
    .append("g")
    .attr("stroke", "#fff")
    .attr("stroke-width", 1.5)
    .selectAll("circle")
    .data(nodes)
    .join("circle")
    .attr("r", 5)
    .call(
      d3
        .drag()
        .on("start", dragstarted)
        .on("drag", dragged)
        .on("end", dragended)
    );

  node.append("title").text((d) => d.id);

  simulation.on("tick", () => {
    link
      .attr("x1", (d) => d.source.x)
      .attr("y1", (d) => d.source.y)
      .attr("x2", (d) => d.target.x)
      .attr("y2", (d) => d.target.y);

    node.attr("cx", (d) => d.x).attr("cy", (d) => d.y);
  });

  console.log(svg, link, node);
}

export default {
  name: "SparcLink",
  mounted() {
    test();
    test2();
  },
};
</script>

<style></style>
