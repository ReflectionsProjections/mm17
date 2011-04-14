package MechMania17;

import MechMania17.Mm17.GameState;

public class Unit {
	private int owner;
	private int id;
	private int hp;
	private int damage;
	private int range;
	private int vision;
	private Location location;

	Unit(GameState.Unit u, Location loc) {
		owner = u.getOwner();
		id = u.getId();
		hp = u.getHp();
		location = loc;
		damage = u.getDamage();
		range = u.getRange();
		vision = u.getVision();
	}

	public int getOwner() {
		return owner;
	}

	public int getId() {
		return id;
	}

	public int getHp() {
		return hp;
	}

	public int getDamage() {
		return damage;
	}

	public int getRange() {
		return range;
	}

	public int getX() {
		return location.getX();
	}

	public int getY() {
		return location.getY();
	}
	
	public Location getLocation() {
		return location;
	}

	public int getVision() {
		return vision;
	}

	@Override
	public int hashCode() {
		final int prime = 31;
		int result = 1;
		result = prime * result + id;
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
		Unit other = (Unit) obj;
		if (id != other.id)
			return false;
		return true;
	}
}
