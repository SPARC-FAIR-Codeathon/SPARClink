d3 = require("d3@5");

data = d3.json("https://gist.githubusercontent.com/lodilas/613d35c4fbf91bb6892ecf0a4ff151a7/raw/4ca473162fccd8db1a8e0fbe22bf8542eaab3f94/JAS_2009-2018_neu.json")

height = 680

drag = (simulation) => {
  function dragstarted(d) {
    if (!d3.event.active) simulation.alphaTarget(0.3).restart();
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

  return d3
    .drag()
    .on("start", dragstarted)
    .on("drag", dragged)
    .on("end", dragended);
};

color = {
  const scale = d3.scaleOrdinal(d3.schemeCategory10);
  return d => scale(d.group);
}

//https://observablehq.com/@lodilas/disjoint-force-directed-graph