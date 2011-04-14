package MechMania17;

import java.util.List;

import MechMania17.Mm17.GameState;

public class Submarine {
	private int x;
	private int y;
	private int id;
	private boolean submerged;
	private List<Unit> units;

	public Submarine(GameState.Submarine s, List<Unit> subUnits) {
		x = s.getX();
		y = s.getY();
		submerged = s.getSubmerged();
		id = s.getId();
		units = subUnits;
	}
	
	public List<Unit> getUnits() {
		return units;
	}

	public int getX() {
		return x;
	}

	public int getY() {
		return y;
	}

	public int getId() {
		return id;
	}

	public boolean isSubmerged() {
		return submerged;
	}

}
