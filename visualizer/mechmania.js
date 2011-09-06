// Utility functions

function pointInRect(x, y, r)
{
	var rx = r.x;
	var ry = r.y;
	var rw = r.width;
	var rh = r.height;
	
	if(x < rx || x > rx+rw || y < ry || y > ry+rh)
	{
		return false;
	}
	
	return true;
}

// Classes

function Camera (x, y, width, height) {
	this.x = x;
	this.y = y;
	this.width = width;
	this.height = height;
}

function World (width, height) {
	this.width = width;
	this.height = height;
	this.starfield = [];
}

World.prototype.init = function ()
{
	// Initialize starfield
	for(var layer = 1; layer <= 3; layer++)
	{
		for(var n = 0; n < 100/layer; n++)
		{
			this.starfield.push([Math.random()*this.width, Math.random()*this.height, layer]);
		}
	}
};

World.prototype.render = function (context, camera)
{
	context.fillStyle = "#000000";
	context.fillRect(0, 0, canvas.width, canvas.height);
				
	// Render starfield
	// the layer param of a star is also it's parallax factor
	context.fillStyle = "#ffffff";
	context.strokeStyle = "#ffffff";
	
	for(var i in this.starfield)
	{
		star = this.starfield[i];
		if(pointInRect(star[0], star[1], camera))
		{
			context.beginPath();
			context.arc(star[0], star[1], star[2], 0, 2*Math.PI, true);
			context.fill();
		}
	}
};
