package MechMania17;

import MechMania17.Game.Terrain;
import java.util.ArrayList;

public class Tile {
	private int owner = 0;
	private int x;
	private int y;
	private Terrain terrain;
	public ArrayList<Unit> unitsOnTile = new ArrayList<Unit>();

	Tile(int _owner, int _x, int _y, Terrain _terrain) {
		owner = _owner;
		x = _x;
		y = _y;
		terrain = _terrain;
	}

	public int getOwner() {
		return owner;
	}

	public int getX() {
		return x;
	}

	public int getY() {
		return y;
	}
	
	public Terrain getTerrain() {
		return terrain;
	}
	
	public String toString() {
		return "owner: " + owner + ", terrain: " + terrain;
	}
}
