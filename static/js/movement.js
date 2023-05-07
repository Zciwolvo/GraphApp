var canvas = document.getElementById("canvas");
var ctx = canvas.getContext("2d");
var x = 0;
var y = 0;

var circles = [];
var layers = [];
var colors = [];

function generateCircles(numCircles, connectionChance, startPoint) {
  console.log("Generating circles...");
  var xhr = new XMLHttpRequest();
  xhr.open("POST", "/generate_circles");
  xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
  xhr.send(
    JSON.stringify({
      numCircles: numCircles,
      connectionChance: connectionChance,
      startPoint: startPoint,
    })
  );
  xhr.onreadystatechange = function () {
    if (xhr.readyState === 4 && xhr.status === 200) {
      var circleData = JSON.parse(xhr.responseText);
      console.log(circleData);
      circles = addCircles(circleData);
      layers = circleData[Object.keys(circleData).length - 1];
      colors = generateColors(layers);
    }
  };
}

function addCircles(circleData) {
  var circles = [];
  var keys = Object.keys(circleData);
  for (var i = 0; i < keys.length - 1; i++) {
    var key = keys[i];
    var circle = {
      x: circleData[key].x,
      y: circleData[key].y,
      radius: circleData[key].radius,
      connections: circleData[key].connections,
    };
    circles.push(circle);
  }
  return circles;
}

function addCircle(circle, index, layer) {
  ctx.beginPath();
  ctx.strokeStyle = colors[layer];
  ctx.arc(circle.x, circle.y, circle.radius, 0, 2 * Math.PI);
  ctx.fillStyle = colors[layer];
  ctx.fill();
  ctx.stroke();
  ctx.fillStyle = "white";
  ctx.font = "30px Arial";
  var textWidth = ctx.measureText(index).width;
  var textHeight = 30;
  ctx.fillText(index, circle.x - textWidth / 2, circle.y + textHeight / 2);
  ctx.fillStyle = "black";
  for (var i = 0; i < circle.connections.length; i++) {
    var connection = circle.connections[i];
    var connectionCircle = circles[connection];
    ctx.strokeStyle = "black";
    ctx.beginPath();
    ctx.moveTo(circle.x, circle.y);
    ctx.lineTo(connectionCircle.x, connectionCircle.y);
    ctx.stroke();
  }
}

function getRandomColor() {
  colors = [
    "(230, 25, 75)",
    "(60, 180, 75)",
    "(255, 225, 25)",
    "(0, 130, 200)",
    "(245, 130, 48)",
    "(145, 30, 180)",
    "(70, 240, 240)",
    "(240, 50, 230)",
    "(210, 245, 60)",
    "(250, 190, 212)",
    "(0, 128, 128)",
    "(220, 190, 255)",
    "(170, 110, 40)",
    "(255, 250, 200)",
    "(128, 0, 0)",
    "(170, 255, 195)",
    "(128, 128, 0)",
    "(255, 215, 180)",
    "(0, 0, 128)",
    "(128, 128, 128)",
  ];
  return "rgb" + colors[Math.floor(Math.random() * colors.length)];
}

function generateColors(layers) {
  var colors = [];
  for (var i = 0; i < layers.length; i++) {
    var color = getRandomColor();
    if (i > 0 && colors.length < 20) {
      while (color in colors) {
        color = getRandomColor();
      }
    }
    colors.push(color);
  }
  return colors;
}

var generateCirclesButton = document.getElementById("generate-circles");
generateCirclesButton.addEventListener("click", function () {
  var numCirclesInput = document.getElementById("num-circles");
  var connectionChanceInput = document.getElementById("connection-chance");
  var startPointInput = document.getElementById("start-point");
  var numCircles = parseInt(numCirclesInput.value);
  var connectionChance = parseInt(connectionChanceInput.value);
  var startPoint = parseInt(startPointInput.value);
  generateCircles(numCircles, connectionChance, startPoint);
});

var isDragging = false;
var selectedCircle = null;

canvas.addEventListener("mousedown", function (event) {
  var rect = canvas.getBoundingClientRect();
  var mouseX = event.clientX - rect.left;
  var mouseY = event.clientY - rect.top;
  for (var i = 0; i < circles.length; i++) {
    var circle = circles[i];
    var distance = Math.sqrt(
      (mouseX - circle.x) ** 2 + (mouseY - circle.y) ** 2
    );
    if (distance <= circle.radius) {
      isDragging = true;
      selectedCircle = circle;
      break;
    }
  }
});

canvas.addEventListener("mousemove", function (event) {
  if (isDragging && selectedCircle) {
    var rect = canvas.getBoundingClientRect();
    selectedCircle.x = event.clientX - rect.left;
    selectedCircle.y = event.clientY - rect.top;
  }
});

canvas.addEventListener("mouseup", function (event) {
  isDragging = false;
  selectedCircle = null;
});

setInterval(function () {
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  for (var i = 0; i < circles.length; i++) {
    var layer = -1;
    for (var j = 0; j < layers.length; j++) {
      if (layers[j].indexOf(i) !== -1) {
        layer = j;
        break;
      }
    }
    addCircle(circles[i], i, layer);
  }
  socket.emit("move", { x: x, y: y });
}, 10);
