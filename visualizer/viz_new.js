/* vim: tabstop=4 shiftwidth=4 noexpandtab
 *
 *  MechMania 17: Thrust Wars
 *  Visualizer
 */
var w = 1;
var h = 1;
var screen_scale = 60000;
var screen_x = 0;
var screen_y = 0;
var last_draw = 0;
var t = 0.0;
var turn = 0;
var auth = prompt("Authcode:");
var ship_scale = 2;

var colors = ["rgb(0,255,0)","rgb(255,128,0)","rgb(255,64,64)","rgb(0,128,255)","rgb(255,128,255)"]
var asteroid_paths = {};

function sortObject(a,b) {
	var a_ = 0, b_ = 0;
	if (a.type == "Ship") {
		a_ = 50;
	} else if (a.type == "Asteroid") {
		a_ = 25;
	}
	if (b.type == "Ship") {
		b_ = 50;
	} else if (b.type == "Asteroid") {
		b_ = 25;
	}
	return a_ - b_;
}

function draw(data) {
	if (data) {
		if (data.turn > -1) {
			if (!data.game_active) {
				turn = 0;
				update();
				return false;
			}
		}
		last_draw = data;
	}
	var canvas = document.getElementById('visualizer');
	if (canvas.getContext) {
		var ctx = canvas.getContext('2d');
		w = $(window).width() - 12;
		h = $(window).height() - 12;
		canvas.width = w;
		canvas.height = h;
		ctx.fillStyle = "rgb(0,0,0)";
		ctx.fillRect(0,0,w,h);
		var players = Array();
		var n_players = 0;
		var nums = Array();
		ctx.lineCap = "round";
		ctx.lineJoin = "round";
		for (i in data.players) {
			players[data.players[i].id + "_"] = data.players[i];
			nums[data.players[i].id + "_"] = i;
			n_players++;
		}
		var d = data.objects.sort(sortObject);
		for (i in d) {
			var o = d[i];
			if (o.type == "Ship") {
				if (o.health == 0)
					continue;
				var p = toView(o.position[0],o.position[1]);
				ctx.fillStyle = colors[nums[o.owner + "_"] % 5];
				ctx.strokeStyle = colors[nums[o.owner + "_"] % 5];
				var vel_angle = (o.velocity[1] < 0 ? 3.14 : 0) + Math.atan(o.velocity[0]/o.velocity[1])
				ship(ctx,p[0],p[1],vel_angle);
				/*
				ctx.font = Math.max(toViewSize(100),8) + "pt monospace";
				var t = players[o.owner + "_"].name;
				var m = ctx.measureText(t);
				ctx.fillText(t,p[0]-m.width/2,p[1]+toViewSize(250));
				ctx.fillStyle = "rgb(0,255,0)";
				ctx.strokeStyle = "rgb(0,255,0)";
				ctx.fillStyle = "rgba(0,255,0,0.7)";
				healthMeter(ctx, p[0], p[1] - toViewSize(200), o.health);
				*/
			} else if (o.type == "Planet") {
				var p = toView(o.position[0],o.position[1]);
				if (o.base && o.base.owner) {
					ctx.strokeStyle = colors[nums[o.base.owner + "_"] % 5];
				} else {
					ctx.strokeStyle = "rgb(255, 255, 255)";
				}
				//ctx.fillStyle = "rgb(0,0,255)";
				circle(ctx,p[0],p[1],toViewSize(o.size));
				/*
				ctx.stroke();
				if (o.base) {
					ctx.strokeStyle = "rgba(0,255,0,1)";
					ctx.fillStyle = "rgba(0,255,0,0.7)";
					healthMeter(ctx, p[0], p[1] - toViewSize(200), o.base.health);
					ctx.fillStyle = colors[nums[o.base.owner + "_"] % 5];
					ctx.font = Math.max(toViewSize(200),8) + "pt monospace";
					var t = players[o.base.owner + "_"].name;
					var m = ctx.measureText(t);
					ctx.fillText(t,p[0]-m.width/2,p[1]+toViewSize(100));
				}
				ctx.strokeStyle = "rgba(0,0,0,0)";
				*/
			} else if (o.type == "Asteroid") {
				var p = toView(o.position[0],o.position[1]);
				var asteroid_path = asteroid_paths[o.id];
				if (!asteroid_path) {
					asteroid_path = createAsteroidPath(o);
					asteroid_paths[o.id] = asteroid_path;
				}

				ctx.lineWidth = Math.max(toViewSize(40), 1);
				if (o.refinery) {
					var style = colors[nums[o.refinery.owner + "_"] % 5];
					ctx.strokeStyle = style;
					//ctx.fillStyle = style;
				} else {
					ctx.strokeStyle = "rgb(255, 255, 255)";
				//	ctx.fillStyle = "rgb(0, 0, 0)";
				}
				drawAsteroid(ctx, asteroid_path);
				/*
				if (o.refinery) {
					ctx.fillStyle = colors[nums[o.refinery.owner + "_"] % 5];
					ctx.font = Math.max(toViewSize(100),8) + "pt monospace";
					var t = players[o.refinery.owner + "_"].name;
					var m = ctx.measureText(t);
					ctx.fillText(t,p[0]-m.width/2,p[1]+toViewSize(o.size + 300));
					ctx.strokeStyle = "rgb(0,255,0)";
					ctx.fillStyle = "rgba(0,255,0,0.7)";
					healthMeter(ctx, p[0], p[1] - toViewSize(o.size + 120), o.refinery.health);
					ctx.strokeStyle = colors[nums[o.refinery.owner + "_"] % 5];
					ctx.lineWidth = toViewSize(100);
				} else {
					ctx.strokeStyle = "rgba(0,0,0,0)";
				}
				ctx.fillStyle = "rgb(255,0,255)";
				circle(ctx,p[0],p[1],toViewSize(o.size));
				ctx.stroke();
				ctx.strokeStyle = "rgba(0,0,0,0)";
				*/
			}
		}
		for (i in data.lasers) {
			var o = data.lasers[i];
			var p = toView(o.start[0],o.start[1]);
			var q = o.direction;
			ctx.beginPath();
			ctx.moveTo(p[0],p[1]);
			ctx.lineTo(p[0]+toViewSize(q[0]),p[1]-toViewSize(q[1]));
			ctx.strokeStyle = "rgba(255,0,0,0.7)";
			ctx.lineWidth = toViewSize(50);
			ctx.stroke();
			ctx.strokeStyle = "rgba(0,0,0,0)";
		}
		ctx.font = "10pt monospace";
		ctx.fillStyle = "rgba(0,0,0,0.5)";
		ctx.fillRect(0,0,350,36 + n_players * 13);
		ctx.fillStyle = "rgb(0,255,0)";
		/* Players */

		var playerColors = new Object();

		for(i in data.players)
		{
			playerColors[data.players[i].name] = colors[ i % 5 ];
		}
		function sortFunc(a, b)
		{
			return b.score - a.score;
		}
		data.players.sort(sortFunc)
		for (i in data.players) {
			p = data.players[i];
			if (p.alive) {
				ctx.fillStyle = playerColors[data.players[i].name];
			} else {
				ctx.fillStyle = "rgb(255,0,0)";
			}
			var score = data.players[i].score;
				score -= (score % 100);
			ctx.font = "10pt monospace";
			ctx.fillText(data.players[i].name, 13, 20 + 23 * 2 * i);
			ctx.font = "13pt monospace";
			ctx.fillText(score, 13, 38 + 23 * 2 * i);
		}
		turn = data.turn + 1;
	}
	return true;
}

function circle(ctx, x, y, r) {
	ctx.lineWidth = Math.max(toViewSize(70), 1);

	ctx.beginPath();
	ctx.arc(x, y, r, 0, Math.PI*2, true);
	ctx.closePath();
	ctx.stroke();

	ctx.beginPath();
	ctx.arc(x, y-1.8*r, 1.5*r, Math.PI/2 - .55, Math.PI/2 + .55);
	ctx.stroke();

	ctx.beginPath();
	ctx.arc(x, y-1.4*r, 1.8*r, Math.PI/2 - .55, Math.PI/2 + .55);
	ctx.stroke();
}

function update() {
	$.getJSON(
		"/game/wait?auth=" + auth + "&turn=" + turn,
		function(data) {
			$.getJSON(
				"/game/info/visualizer?auth=" + auth,
				function(data) {
					if (draw(data)) {
						update();
					}
				}
			);
		}
	).error(function() { turn = 0; update(); });
}

function healthMeter(ctx, cx, cy, val) {
	ctx.lineWidth = toViewSize(10);
	ctx.strokeRect(cx-toViewSize(200),cy-toViewSize(40),toViewSize(400),toViewSize(80));
	ctx.fillRect(cx-toViewSize(200),cy-toViewSize(40),toViewSize(4 * val),toViewSize(80));
}

function s(ctx, cx, cy, angle, x, y) {
	ctx.lineTo(cx + Math.cos(angle) * ship_scale*toViewSize(x) - Math.sin(angle) * ship_scale*toViewSize(y), cy + Math.sin(angle) * ship_scale*toViewSize(x) + Math.cos(angle) * ship_scale*toViewSize(y));
	return 
}
function ship(ctx, cx, cy, angle) {
	angle += Math.PI;
	ctx.lineWidth = Math.max(toViewSize(30), 1);
	ctx.beginPath();
	ctx.moveTo(cx - Math.sin(angle) * ship_scale*toViewSize(200),cy + Math.cos(angle) * ship_scale*toViewSize(200));
	s(ctx,cx,cy,angle, -100, -100);
	s(ctx,cx,cy,angle, 0, -50);
	s(ctx,cx,cy,angle, 100, -100);
	s(ctx,cx,cy,angle, 0, 200);
	ctx.stroke();
}

function createAsteroidPath(asteroid) {
	var path = [];
	var angle = 0;
	var d_angle = Math.PI/4;
	var r = 2.5 * asteroid.size/2;
	var base_x = asteroid.position[0];
	var base_y = asteroid.position[1];

	function createPt() {
		return Math.floor(8 * Math.random())
	}
	var pt1 = createPt();
	var pt2 = createPt();
	while (Math.abs(pt2-pt1) <= 1) {
		pt2 = createPt();
	}

	for (var i=0; i < 8; i++) {
		var pt_r = r;
		if (i === pt1 || i === pt2) {
			pt_r *= 0.3 + (0.6*Math.random());
		}
		var x = base_x + pt_r * Math.cos(angle);
		var y = base_y + pt_r * Math.sin(angle);
		path.push([x, y]);

		angle += d_angle;
	}
	path.push(path[0]);
	
	return path;
}

function drawAsteroid(ctx, a_path) {
	ctx.beginPath();
	var first = toView(a_path[0][0], a_path[0][1]);
	ctx.moveTo(first[0], first[1]);
	for (var i=1; i < a_path.length; i++) {
		var pt = toView(a_path[i][0], a_path[i][1]);
		ctx.lineTo(pt[0], pt[1]);
	}
	ctx.stroke();
}

/*
 * Convert regular coordinates to view coordinates
 */
function toView(x,y) {
	var o = [0,0];
	o[0] = (x - screen_x) / screen_scale;
	o[0] *= h / w;
	o[0] += 0.5;
	o[1] = -(y + screen_y) / screen_scale;
	o[1] += 0.5;
	o[0] *= w;
	o[1] *= h;
	return o;
}
function toViewSize(r) {
	return r * h / screen_scale;
}


var mouseDowned = false;
var mouseDownX = 0;
var mouseDownY = 0;
$(window).mousedown(function (event) {
	mouseDowned = true;
	mouseDownX = event.pageX;
	mouseDownY = event.pageY;
});

$(window).mousemove(function (event) {
	if(mouseDowned) {
		var dX = mouseDownX - event.pageX;
		var dY = mouseDownY - event.pageY;

		mouseDownX = event.pageX;
		mouseDownY = event.pageY;

		screen_x += dX * screen_scale / h;
		screen_y += dY * screen_scale / h;
		draw(last_draw);
	}
});
$(window).mouseup(function (event) {
	mouseDowned = false;
});
$(window).mousewheel(function (event, delta) {
	screen_scale *= Math.exp(-delta / 5);
	draw(last_draw);
});

var scale = 1.0;
$(window).each(function() {
	this.ontouchstart = function(event) {
		var targetEvent = event.touches.item(0);
		mouseDownX = targetEvent.clientX;
		mouseDownY = targetEvent.clientY;
		event.preventDefault();
		return false;
	};
	this.ontouchmove = function(event) {
		var targetEvent = event.touches.item(0);
		var dX = mouseDownX - targetEvent.clientX;
		var dY = mouseDownY - targetEvent.clientY;

		mouseDownX = targetEvent.clientX;
		mouseDownY = targetEvent.clientY;

		screen_x += dX * screen_scale / h;
		screen_y += dY * screen_scale / h;
		draw(last_draw);
		event.preventDefault();
		return false;
	};
	this.ongesturechange = function(event) {
		delta = event.scale - scale;
		screen_scale *= Math.exp(-delta / 5);
		draw(last_draw);
		scale = event.scale;
	};
	this.ongestureend = function(event) {
		scale = 1.0;
	}
});

update();
