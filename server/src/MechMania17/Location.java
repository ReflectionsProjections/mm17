package MechMania17;

import MechMania17.Mm17.Command.*;

public class Location {
	private int x;
	private int y;

	public Location() {
		x = -1;
		y = -1;
	}

	public Location(int x, int y) {
		this.x = x;
		this.y = y;
	}

	public int getX() {
		return x;
	}

	public int getY() {
		return y;
	}

	public int getDistance(Location other) {
		return Math.abs(x - other.x) + Math.abs(y - other.y);
	}

	public Location of(Direction direction) {
		switch (direction)
		{
			case NORTH:
				return new Location(x, y - 1);
			case SOUTH:
				return new Location(x, y + 1);
			case EAST:
				return new Location(x + 1, y);
			case WEST:
				return new Location(x - 1, y);
			default:
				return null;
		}
	}

	static public boolean isValid(Location l) {
		if (l == null)
			return false;
		return (l.x >= 0) && (l.y >= 0);
	}

	public String toString() {
		return "(" + Integer.toString(x) + ", " + Integer.toString(y) + ")";
	}
}

