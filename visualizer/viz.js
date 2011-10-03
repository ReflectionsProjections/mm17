var w = 1;
var h = 1;
var screen_scale = 60000;
var screen_x = 0;
var screen_y = 0;
var last_draw = 0;

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
		ctx.font = "10pt monospace";
		ctx.fillStyle = "rgb(0,255,0)";
		ctx.fillText("Turn " + data.turn.toString(), 2, 10);
		ctx.fillText("Players (" + data.players.length.toString() + ")", 2, 26);
		/* Players */
		var players = Array();
		for (i in data.players) {
			p = data.players[i];
			players[p.id + "_"] = p;
			if (p.alive) { 
				ctx.fillStyle = "rgb(0,255,0)";
			} else {
				ctx.fillStyle = "rgb(255,0,0)";
			}
			ctx.fillText(p.name + "  [o:" + p.resources + " b:" + p.bases.length + " r:" + p.refineries.length + " s:" + p.ships.length + "]", 2, 40 + 13 * i);
		}
		for (i in data.objects) {
			var o = data.objects[i];
			if (o.type == "ship") {
				if (o.health == 0)
					continue;
				var p = toView(o.position[0],o.position[1]);
				ctx.fillStyle = "rgb(0,255,0)";
				circle(ctx,p[0],p[1],toViewSize(100));
				ctx.fillStyle = "rgb(0,255,0)";
				var d = toViewSize(110);
				ctx.fillText(Math.floor(o.health).toString() + " " + o.id,p[0]+d,p[1]-5);
				ctx.fillText(players[o.owner + "_"].name,p[0]+d,p[1]+7);
			} else if (o.type == "Planet") {
				var p = toView(o.position[0],o.position[1]);
				ctx.fillStyle = "rgb(0,0,255)";
				if (o.base) {
					ctx.strokeStyle = "rgba(0,255,0,1)";
					ctx.lineWidth = toViewSize(200);
				} else {
					ctx.strokeStyle = "rgba(0,0,0,0)";
				}
				circle(ctx,p[0],p[1],toViewSize(o.size));
				ctx.stroke();
			} else if (o.type == "asteroid") {
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
			}
		}
		for (i in data.lasers) {
			var o = data.lasers[i];
			var p = toView(o.start[0],o.start[1]);
			var q = o.direction;
			ctx.moveTo(p[0],p[1]);
			ctx.lineTo(p[0]+toViewSize(q[0]),p[1]-toViewSize(q[1]));
			ctx.strokeStyle = "rgb(255,0,0)";
			ctx.lineWidth = toViewSize(50);
			ctx.stroke();
			ctx.strokeStyle = "rgba(0,0,0,0)";
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
