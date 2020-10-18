const height = 150
const width = 400
const margin = ({top: 20, right: 30, bottom: 30, left: 40})

var Plot = function(){
  var data = [];
  return{
    data:data,
  }
}();

y_min = Math.max(d3.min(Plot.data, d => d.score)-100, 0)
if (isNaN (y_min)) {
  y_min = 0
}
y_max = Math.min(d3.max(Plot.data, d => d.score)+100, 1000)
if (isNaN(y_max)){
  y_max = 1000
}

y = d3.scaleLinear()
  .domain([y_min,y_max]).nice()
  .range([height - margin.bottom, margin.top])

x = d3.scaleBand()
  .domain(Array.from({length: n_iterations+1}, (x, i) => i+1))
  .range([margin.left, width - margin.right])
  .padding(0.1)

xAxis = g => g
  .attr("transform", `translate(0,${height - margin.bottom})`)
  .call(d3.axisBottom(x)
    .tickSizeOuter(10)
    .tickValues(x.domain().filter(function(d,i){ return !((i+1)%5)})))
  .call(g => g.append("text")
    .attr("x", width - 4)
    .attr("y", -4)
    .attr("font-weight", "bold")
    .attr("text-anchor", "end")
    .attr("fill", "black")
    .text("Round #")
    )

yAxis = g => g
  .attr("transform", `translate(${margin.left},0)`)
  .call(d3.axisLeft(y).ticks(5))

const svg = d3.select("#plot")
    .append("svg")
    .attr("viewBox", [0, 0, width, height]);

svg.append("g")
  .attr('class', 'xaxis')
  .call(xAxis);

svg.append("g")
  .attr('class', 'yaxis')
  .call(yAxis);

svg.append("text")
  .attr("class", "yaxis_label")  // this makes it easy to centre the text as the transform is applied to the anchor
  .attr("font-weight", "bold")
  .attr('font-size', "10px")
  .attr("fill", "black")
  .attr("transform", "translate("+ (45) +","+(25)+")")  // text is drawn off the screen top left, move down and out and rotate
  .text("Score");

function update_plot() {

  y_min = Math.max(d3.min(Plot.data, d => d.score)-100, 0)
  if (isNaN (y_min)) {
    y_min = 0
  }
  y_max = Math.min(d3.max(Plot.data, d => d.score)+100, 1000)
  if (isNaN(y_max)){
    y_max = 1000
  }

  y = d3.scaleLinear()
  .domain([y_min,y_max])
  .range([height - margin.bottom, margin.top]) 

  svg.select('.yaxis')
    .transition().duration(500)
    .call(yAxis)

  bars = svg.selectAll("rect")
    .data(Plot.data);

  bars.enter()
    .append('g')
    .append("rect")
    .attr("fill", "steelblue")
    .attr("x", d => x(d.index))
    .attr("y", d => y(d.score))
    .attr("height", d => y(y_min) - y(d.score))
    .attr("width", x.bandwidth());

  bars.transition()
      .duration(500)
      .attr("x", d => x(d.index))
      .attr("y", d => y(d.score))
      .attr("height", d => y(y_min) - y(d.score));
  // bars.append("text")
  //   .text((d) => `${d.score}`)
  //   .attr("x", (d) => x(d.index)  )
  //   .attr("y", (d) => y(d.score))
  //   .attr('font-size', 6)
}

update_plot()

