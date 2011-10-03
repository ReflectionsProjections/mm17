var w = 1;
var h = 1;
var screen_scale = 60000;
var screen_x = 0;
var screen_y = 0;
var last_draw = 0;
var t = 0.0;

function draw(data) {
	if (data) {
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
		ctx.lineCap = "round";
		ctx.lineJoin = "round";
		for (i in data.players) {
			players[data.players[i].id + "_"] = data.players[i];
			n_players++;
		}
		for (i in data.objects) {
			var o = data.objects[i];
			if (o.type == "Ship") {
				if (o.health == 0)
					continue;
				var p = toView(o.position[0],o.position[1]);
				//circle(ctx,p[0],p[1],toViewSize(100));
				ship(ctx,p[0],p[1],o.direction);
				ctx.fillStyle = "rgb(0,255,0)";
				ctx.font = Math.max(toViewSize(100),8) + "pt monospace";
				ctx.fillText(players[o.owner + "_"].name,p[0]+toViewSize(100),p[1]+toViewSize(30));
				ctx.strokeStyle = "rgb(0,255,0)";
				ctx.fillStyle = "rgba(0,255,0,0.7)";
				healthMeter(ctx, p[0], p[1] - toViewSize(150), o.health);
			} else if (o.type == "Planet") {
				var p = toView(o.position[0],o.position[1]);
				if (o.base) {
					ctx.strokeStyle = "rgb(0,0,255)";
					ctx.fillStyle = "rgba(0,0,255,0.7)";
					healthMeter(ctx, p[0], p[1] - toViewSize(o.size + 170), o.base.health);
					ctx.strokeStyle = "rgba(0,255,0,1)";
					ctx.lineWidth = toViewSize(200);
					ctx.fillStyle = "rgb(0,0,255)";
					ctx.font = Math.max(toViewSize(200),8) + "pt monospace";
					ctx.fillText(players[o.base.owner + "_"].name,p[0]+toViewSize(o.size + 110),p[1]);
				} else {
					ctx.strokeStyle = "rgba(0,0,0,0)";
				}
				ctx.fillStyle = "rgb(0,0,255)";
				circle(ctx,p[0],p[1],toViewSize(o.size));
				ctx.stroke();
				ctx.strokeStyle = "rgba(0,0,0,0)";
			} else if (o.type == "Asteroid") {
				var p = toView(o.position[0],o.position[1]);
				if (o.refinery) {
					ctx.strokeStyle = "rgba(0,255,0,1)";
					ctx.lineWidth = toViewSize(100);
				} else {
					ctx.strokeStyle = "rgba(0,0,0,0)";
				}
				ctx.fillStyle = "rgb(255,0,255)";
				circle(ctx,p[0],p[1],toViewSize(o.size));
				ctx.stroke();
				ctx.strokeStyle = "rgba(0,0,0,0)";
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
		ctx.fillText("Turn " + data.turn.toString(), 2, 12);
		ctx.fillText("[" + Math.floor(screen_x) + "," + Math.floor(screen_y) + "]", 200, 12);
		ctx.fillText("Players (" + data.players.length.toString() + ")", 2, 26);
		/* Players */
		for (i in data.players) {
			p = data.players[i];
			if (p.alive) { 
				ctx.fillStyle = "rgb(0,255,0)";
			} else {
				ctx.fillStyle = "rgb(255,0,0)";
			}
			ctx.fillText(p.name + "  [o:" + p.resources + " b:" + p.bases.length + " r:" + p.refineries.length + " s:" + p.ships.length + "]", 2, 40 + 13 * i);
		}
	}
}

function circle(ctx, x, y, r) {
	ctx.beginPath();
	ctx.arc(x, y, r, 0, Math.PI*2, true);
	ctx.closePath();
	ctx.fill();
}

function update() {
	$.getJSON(
		"/game/info/visualizer?auth=123456",
		function(data) {
			draw(data);
		}
	);
}

function healthMeter(ctx, cx, cy, val) {
	ctx.lineWidth = toViewSize(10);
	ctx.strokeRect(cx-toViewSize(200),cy-toViewSize(40),toViewSize(400),toViewSize(80));
	ctx.fillRect(cx-toViewSize(200),cy-toViewSize(40),toViewSize(4 * val),toViewSize(80));
}

function s(ctx, cx, cy, angle, x, y) {
	ctx.lineTo(cx + Math.cos(angle) * toViewSize(x) - Math.sin(angle) * toViewSize(y), cy + Math.sin(angle) * toViewSize(x) + Math.cos(angle) * toViewSize(y));
	return 
}
function ship(ctx, cx, cy, angle) {
	angle += Math.PI;
	ctx.strokeStyle = "rgba(0,255,0,1.0)";
	ctx.lineWidth = toViewSize(20);
	ctx.beginPath();
	ctx.moveTo(cx - Math.sin(angle) * toViewSize(200),cy + Math.cos(angle) * toViewSize(200));
	s(ctx,cx,cy,angle, -100, -100);
	s(ctx,cx,cy,angle, 0, -50);
	s(ctx,cx,cy,angle, 100, -100);
	s(ctx,cx,cy,angle, 0, 200);
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


stateTimer = setInterval(function() {update();}, 500);
