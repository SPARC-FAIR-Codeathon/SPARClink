
keywords = [
    "Hello", "world", "normally", "you", "want", "more", "words",
    "than", "this"]

values = []
for (var i = 0; i < keywords.length; i++) {
    values[i] = Math.random()
}
values[0] = 0

d3.select(window).on("load", function(){ generateWordCloud(keywords, values, [500, 500], function(d, i) {
    console.log('Clicked ' + d.text);
}) })

function handleMouseOver(d, i) {
    d3.select(this)
        .classed("word-hovered", true)
        .transition(`mouseover-${d.text}`).duration(300)
            .style("font-size", d.size + 10 + "px");
}

function handleMouseOut(d, i) {
    console.log(d.text)
    d3.select(this)
        .classed("word-hovered", false)
        .interrupt(`mouseover-${d.text}`)
        .style("font-size", d.size);
}

function mouseClicked(d, i) {
    d3.selectAll(".word-default")
        .classed("word-selected", false)
    
    d3.select(this)
        .classed("word-selected", true)
}

function generateWordCloud (keywords, values, cloud_size, callback) {
    
    const fontFamily = "Verdana, Arial, Helvetica, sans-serif";

    var layout = d3.layout.cloud()
        .size(cloud_size)
        .words(keywords.map(function(d, i) {
            return {text: d, size: 10 + values[i] * 90, test: "haha"};
        }))
        .padding(5)
        .rotate(function() { return 0; })
        .font(fontFamily)
        .fontSize(function(d) { return d.size; })
        .on("end", draw);
    //.on("mouseover", handleMouseOver);

    layout.start();

    function draw(words) {
        d3.select("body").append("svg")
            .attr("width", layout.size()[0])
            .attr("height", layout.size()[1])
            .append("g")
            .attr("transform", "translate(" + layout.size()[0] / 2 + "," + layout.size()[1] / 2 + ")")
            .selectAll("text")
            .data(words)
            .enter().append("text")
            .classed("word-default", true)
            .style("font-size", function(d) { return d.size + "px"; })
            .style("font-family", fontFamily)
            .attr("text-anchor", "middle")
            .attr("transform", function(d) {
                return "translate(" + [d.x, d.y] + ")rotate(" + d.rotate + ")";
            })
            .text(function(d) { return d.text; })
            .on("mouseover", handleMouseOver)
            .on("mouseout", handleMouseOut)
            .on("click", function(d, i){
                mouseClicked.call(this, d, i)
                callback.call(this, d, i)
            });
    }
}