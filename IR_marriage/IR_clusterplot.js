// D3 VER 3
var width = 960*2,
    height = 600,
    padding = 6, // separation between nodes
    maxRadius = 12;

var n = 1000, // total number of nodes
    m = 4; // number of distinct clusters

function weightedRand(spec) {
  var i, j, table=[];
  for (i in spec) {
    // The constant 10 below should be computed based on the
    // weights in the spec for a correct and optimal table size.
    // E.g. the spec {0:0.999, 1:0.001} will break this impl.
    for (j=0; j<spec[i]*1000; j++) {
      table.push(i);
    }
  }
  return function() {
    return table[Math.floor(Math.random() * table.length)];
  }
}
//Male Rates ( for plotting the men)
// var rates=[0.61365865, 0.06441721, 0.11653099, 0.0407308 , 0.08905088, 0.02750786, 0.04011841, 0.0079852]

//Femal Rates (for plottig the women)
var rates=[0.664098,
 0.068902,
 0.12682000000000002,
 0.04318,
 0.114282,
 0.011718000000000001,
 0.03322800000000001,
 0.018772]
var rand012 = weightedRand({1:rates[0],
                           5:rates[1],
                           2:rates[2],
                           6:rates[3],
                           3:rates[4],
                           7:rates[5],
                           4:rates[6],
                           8:rates[7]});

// This is the mariage rates
// var rates=[0.095,0.259,0.236,0.166]

var color = d3.scale.category10()
    .domain(d3.range(m));

var x = d3.scale.ordinal()
    .domain(d3.range(m))
    .rangePoints([0, width], 1);


var colors=["#d3d3d3",
            "#d3d3d3",
            "#d3d3d3",
            "#d3d3d3",
            "#00ccbc",
           "#00ccbc",
           "#00ccbc",
           "#00ccbc"]
// var colors=["#d3d3d3",
//             "#d3d3d3",
//             "#d3d3d3",
//             "#d3d3d3",
//             "#ff8888",
//            "#ff8888",
//            "#ff8888",
//            "#ff8888"]
var nodes = d3.range(n).map(function() {
  var i = rand012(),
      v = (i + 1) / m * -Math.log(Math.random());
  return {
    radius: 10,
    color: colors[i-1],
    cx: x((i-1)%4)+100,
    cy: height / 2
  };
});

var force = d3.layout.force()
    .nodes(nodes)
    .size([width, height])
    .gravity(0)
    .charge(0)
    .on("tick", tick)
    .start();

var svg = d3.select("body").append("svg")
    .attr("width", width)
    .attr("height", height);

var circle = svg.selectAll("circle")
    .data(nodes)
  .enter().append("circle")
    .attr("r", function(d) { return d.radius; })
    .style("fill", function(d) { return d.color; })
    .call(force.drag);

function tick(e) {
  circle
      .each(gravity(.2 * e.alpha))
      .each(collide(.5))
      .attr("cx", function(d) { return d.x; })
      .attr("cy", function(d) { return d.y; });
}

// Move nodes toward cluster focus.
function gravity(alpha) {
  return function(d) {
    d.y += (d.cy - d.y) * alpha;
    d.x += (d.cx - d.x) * alpha;
  };
}

// Resolve collisions between nodes.
function collide(alpha) {
  var quadtree = d3.geom.quadtree(nodes);
  return function(d) {
    var r = d.radius + maxRadius + padding,
        nx1 = d.x - r,
        nx2 = d.x + r,
        ny1 = d.y - r,
        ny2 = d.y + r;
    quadtree.visit(function(quad, x1, y1, x2, y2) {
      if (quad.point && (quad.point !== d)) {
        var x = d.x - quad.point.x,
            y = d.y - quad.point.y,
            l = Math.sqrt(x * x + y * y),
            r = d.radius + quad.point.radius + (d.color !== quad.point.color) * 0;
        if (l < r) {
          l = (l - r) / l * alpha;
          d.x -= x *= l;
          d.y -= y *= l;
          quad.point.x += x;
          quad.point.y += y;
        }
      }
      return x1 > nx2 || x2 < nx1 || y1 > ny2 || y2 < ny1;
    });
  };
}