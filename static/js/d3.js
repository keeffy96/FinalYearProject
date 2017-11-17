// Data: Average age of employees in an organization
var employees = [
    {dept: 'A', count : 22},
    {dept: 'B', count : 66},
    {dept: 'C', count : 25},
    {dept: 'D', count : 50},
    {dept: 'E', count : 27}
];
var maxWidth = 200;
var maxHeight = 200;
var outerRadius = 100;
var ringWidth = 20;

function drawAnimatedRingChart(config) {
    var pie = d3.layout.pie().value(function (d) {
        return d.count;
    });

    var color = d3.scale.category10();
    var arc = d3.svg.arc();

    // This function helps transition between
    // a starting point and an ending point
    // Also see: http://jsfiddle.net/Nw62g/3/
    function tweenPie(finish) {
        var start = {
                startAngle: 0,
                endAngle: 0
            };
        var i = d3.interpolate(start, finish);
        return function(d) { return arc(i(d)); };
    }
    arc.outerRadius(config.outerRadius || outerRadius)
        .innerRadius(config.innerRadius || innerRadius);

    // Remove the previous ring
    d3.select(config.el).selectAll('g').remove();

    var svg = d3.select(config.el)
        .attr({
            width : maxWidth,
            height: maxHeight
        });

    // Add the groups that will hold the arcs
    var groups = svg.selectAll('g.arc')
    .data(pie(config.data))
    .enter()
    .append('g')
    .attr({
        'class': 'arc',
        'transform': 'translate(' + outerRadius + ', ' + outerRadius + ')'
    });

    // Create the actual slices of the pie
    groups.append('path')
    .attr({
        'fill': function (d, i) {
            return color(i);
        }
    })
    .transition()
    .duration(config.duration || 1000)
    .attrTween('d', tweenPie);
}

// Render the initial ring
drawAnimatedRingChart({
    el: '.animated-ring svg',
    outerRadius: outerRadius,
    innerRadius: outerRadius - ringWidth,
    data: employees
});

// Listen to changes on the select element
document.querySelector('#numberOfDepartments')
  .addEventListener('change', function (e) {
      drawAnimatedRingChart({
        el: '.animated-ring svg',
        outerRadius: outerRadius,
        innerRadius: outerRadius - ringWidth,
        data: employees.slice(0, parseInt(this.value))
    });
  });