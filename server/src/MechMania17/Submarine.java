package MechMania17;

import java.util.HashMap;

public class Submarine {
	private int movesLeft = 0; // initially 0

	public int id;
	public int owner;

	Location loc;

	public int movesToGo;

	public boolean submerged = false;

	public HashMap<Integer, Soldier> internalStorage;

	private static int submarineIdCounter = 0;

	public static final int movesPerTurn = 1;

	public static Submarine builder(MapGrid map, Location loc, Player p) {
		boolean validUnit = isValid(map, loc);

		if (validUnit) {
			return new Submarine(p.id, loc);
		} else {
			return null;
		}
	}

	private static boolean isValid(MapGrid map, Location loc) {
		return map.isTileWater(loc);
	}

	private Submarine() {
	}

	private Submarine(int owner, Location loc) {
		this.id = submarineIdCounter++;
		this.loc = loc;
		this.owner = owner;
		internalStorage = new HashMap<Integer, Soldier>();
	}

	/**
	 * Calculates the cost of a submarine of this type.
	 * @return cost
	 */
	public static int calculateCost() {
		return Cost.calculateSubmarineCost();
	}

	public String toString() {
		String ret = "Submarine: " + id;
		return ret;
	}

	public void load(Soldier unit) {
		internalStorage.put(unit.id, unit);
	}

	public void move(Location dest) {
		int distance = loc.getDistance(dest);
		submerged = true;
		this.loc = dest;
		movesToGo = calculateTime(distance);
	}

	private int calculateTime(int distance) {
		return 4; // chosen by fair dice roll
	}

	public boolean spendAction() {
		return movesLeft-- <= 0;
	}

	public boolean isSubmerged() {
		return submerged;
	}

	public Location getLocation() {
		return loc;
	}

	public boolean hasAction() {
		return movesLeft <= 0;
	}

	public void resetActionCount() {
		movesLeft = movesPerTurn;
		for (Soldier u : internalStorage.values()) {
			u.resetActionCount();
		}
		movesToGo--;
		if (movesToGo == 0) {
			submerged = false;
		}
	}
}
