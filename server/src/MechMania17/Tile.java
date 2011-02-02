package MechMania17;

import java.util.HashMap;
import java.util.ArrayList;
import java.util.Iterator;

import MechMania17.Mm17.InitialResources;

public class Tile {
	public static enum Terrain {
		LAND, WATER, IMPASSABLE
	}

	public static final int UNIT_CAP = 9;

	public HashMap<Integer, Soldier> units;
	public HashMap<Integer, Submarine> submarines;
	private int owner = 0;
	public char terrain;

	public Tile(char c) {
		terrain = c;
		units = new HashMap<Integer, Soldier>();
		submarines = new HashMap<Integer, Submarine>();
	}

	public int getOwner() {
		return owner;
	}

	public void setOwner(int owner) {
		this.owner = owner;
	}

	public boolean isStart() {
		return terrain == 's';
	}

	public Terrain getTerrainType() {
		switch (terrain) {
		case 'w':
			return Terrain.WATER;
		case 'm':
			return Terrain.IMPASSABLE;
		case 's':
		case 'p':
		default:
			return Terrain.LAND;
		}
	}

	public boolean hasUnitFromPlayer(Player p) {
		if (owner == p.id) {
			return true;
		}
		for (Submarine sub : submarines.values()) {
			if (sub.owner == p.id) {
				return true;
			}
		}
		return false;
	}

	public Soldier getUnitById(int unit) {
		if (getTerrainType() == Terrain.LAND) {
			return units.get(unit);
		} else {
			for (Submarine sub : submarines.values()) {
				if (sub.internalStorage.containsKey(unit)) {
					return sub.internalStorage.get(unit);
				}
			}
		}
		return null;
	}

	public void removeUnit(Soldier unit) {
		if (getTerrainType() == Terrain.LAND) {
			units.remove(unit.id);
		} else {
			for (Submarine sub : submarines.values()) {
				if (sub.internalStorage.containsKey(unit.id)) {
					sub.internalStorage.remove(unit.id);
				}
			}
		}
	}

	public int getUnitOwner(Soldier unit) {
		if (getTerrainType() == Terrain.LAND) {
			return owner;
		} else {
			for (Submarine sub : submarines.values()) {
				if (sub.internalStorage.containsKey(unit.id)) {
					return sub.owner;
				}
			}
		}
		return 0;
	}

	public int getMaxVisionForPlayer(Player p) {
		int maxVision = 0;
		if (getTerrainType() == Terrain.LAND) {
			if (p.id == owner) {
				for (Soldier unit : units.values()) {
					maxVision = Math.max(unit.visionRange, maxVision);
				}
			}
		} else {
			for (Submarine sub : submarines.values()) {
				if (p.id == sub.owner) {
					for (Soldier unit : sub.internalStorage.values()) {
						maxVision = Math.max(unit.visionRange, maxVision);
					}
				}
			}
		}
		return maxVision;
	}

	public ArrayList<Soldier> getAllUnits() {
		ArrayList<Soldier> bigcollection = new ArrayList<Soldier>(units.values());
		Iterator<Submarine> itr = submarines.values().iterator();
		while(itr.hasNext()) {
			Submarine sub = itr.next();
			bigcollection.addAll(sub.internalStorage.values());
			if (sub.internalStorage.isEmpty()) {
				itr.remove();
			}
		}
		return bigcollection;
	}

	public InitialResources.Tile.Terrain toProtoType() {
		switch (terrain) {
		case 'w':
			return InitialResources.Tile.Terrain.OCEAN;
		case 'm':
			return InitialResources.Tile.Terrain.MOUNTAIN;
		case 'p':
		case 's':
		default:
			return InitialResources.Tile.Terrain.PLAIN;
		}
	}

	public boolean hasSubmarineFromPlayer(Player p) {
		for (Submarine sub : submarines.values()) {
			if (sub.owner == p.id) {
				return true;
			}
		}
		return false;
	}
}
