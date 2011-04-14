package MechMania17;

import MechMania17.Mm17.Command.Direction;

public class Location {
	private int x = -1;
	private int y = -1;
	
	Location(int _x, int _y) {
		x = _x;
		assert x > -1;
		y = _y;
		assert y > -1;
	}
	
	public int getX() {
		return x;
	}
	
	public int getY() {
		return y;
	}
	
	public String toString() {
		return "loc(" + x + ", " + y + ")";
	}

	@Override
	public int hashCode() {
		final int prime = 31;
		int result = 1;
		result = prime * result + x;
		result = prime * result + y;
		return result;
	}

	@Override
	public boolean equals(Object obj) {
		if (this == obj)
			return true;
		if (obj == null)
			return false;
		if (getClass() != obj.getClass())
			return false;
		Location other = (Location) obj;
		if (x != other.x)
			return false;
		if (y != other.y)
			return false;
		return true;
	}
	
	/**
	 * Gives relative Location needed to arrive at another Location
	 * nulls mean that you are in line with that axis
	 * @param other - Other location
	 * @return [North | South | null, East | West | null]
	 */
	public Direction[] to(Location other){
		Direction[] to = new Direction[2];
		if (other.getX() < getX()){
			to[0] = Direction.WEST;
		} else if (other.getX() == getX()) {
			to[0] = null;
		}
		else {
			to[0] = Direction.EAST;
		}
		if (other.getY() < getY()) {
			to[1] = Direction.NORTH;
		} else if (other.getY() == getY()) {
			to[1] = null;
		} else {
			to[1] = Direction.SOUTH;
		}
		return to;
	}
	public int calcDistance(Location other){
		int distance = Math.abs((Math.abs(this.getX()) - Math.abs(other.getX())) + (Math.abs(this.getY()) - Math.abs(other.getY())));
		return distance;
	}
}
