var MechMania = {};

MechMania.World = function ()
{
	this.starfield = [];	// [[x,y,r],...]
	this.starfieldSize = 0;
}

MechMania.World.prototype.generateStarfield = function(meanSpacing, stdevSpacing, nStars)
{
	var dimStars = Math.ceil(Math.sqrt(nStars));

	this.starfield = [];
	this.starfieldSize = dimStars * meanSpacing;

	for(var j = 0; j < dimStars; j++)
	{
		for(var i = 0; i < dimStars; i++)
		{
			var inverseErf = function(x)
			{
				var w = Math.log(1.0 - x*x);
				var m = Math.sqrt(Math.sqrt(18.75537 - 2.47197*w + 0.25*w*w) - 4.33074 - 0.5*w);

				return (x > 0 ? m : -m);
			};

			var dR = Math.sqrt(2*stdevSpacing) * inverseErf(Math.random());
			var dTheta = Math.random() * 2*Math.PI;
			var dX = dR * Math.cos(dTheta);
			var dY = dR * Math.sin(dTheta);

			this.starfield.push([ i*meanSpacing + dX, j*meanSpacing + dY, [1,2,3][Math.floor(Math.random()*3)] ]);
		}
	}
}

MechMania.World.prototype.renderStarfield = function(scale, originX, originY, canvas, context)
{
	var blockRepeatX = 1 + canvas.width / (scale * this.starfieldSize);	// real space spanned by the screen divided by real space spanned by the starfield
	var blockRepeatY = 1 + canvas.height / (scale * this.starfieldSize);
	var modTransformX = originX % this.starfieldSize;					// origin transform modulo starfieldSize
	var modTransformY = originY % this.starfieldSize;

	if(modTransformX < 0) modTransformX += blockRepeatX;
	if(modTransformY < 0) modTransformY += blockRepeatY;

	context.save();

	context.fillStyle = "#000000";
	context.fillRect(0, 0, canvas.width, canvas.height);
	context.translate(-modTransformX, -modTransformY);

	context.fillStyle = "#eeeeee";

	for(var j = -1; j < blockRepeatY; j++)
	{
		for(var i = -1; i < blockRepeatX; i++)
		{
			for(var n in this.starfield)
			{
				var centerX = scale * (this.starfield[n][0] + i*this.starfieldSize);
				var centerY = scale * (this.starfield[n][1] + j*this.starfieldSize);
				var radius = Math.max(this.starfield[n][2] * scale, 1);

				context.beginPath();
				context.arc(centerX, centerY, radius, 0, 2*Math.PI, true);
				context.fill();
			}
		}
	}

	context.restore();
}