package MechMania17;

public class Soldier {
	public int totalHitPoints;
	public int hitPoints;
	public int attackDamage;
	public int attackRange;
	public int visionRange;
	private int movesLeft = 0; // initially 0

	public int id;

	private static int soldierIdCounter = 0;

	public static final int movesPerTurn = 1;

	public static Soldier builder(int hitPoints, int attackDamage,
			int attackRange, int visionRange) {
		boolean validUnit = isValid(hitPoints, attackDamage, attackRange,
				visionRange);

		if (validUnit) {
			return new Soldier(hitPoints, attackDamage, attackRange,
					visionRange);
		} else {
			return null;
		}
	}

	private static final int MAX_HITPOINTS = 1000000;
	private static final int MAX_ATTACK_DAMAGE = 1000000;
	private static final int MAX_ATTACK_RANGE = 1000000;
	private static final int MAX_VISION_RANGE = 1000000;

	private static boolean isValid(int hitPoints, int attackDamage,
			int attackRange, int visionRange) {
		if (hitPoints < 1 || hitPoints > MAX_HITPOINTS) return false;
		if (attackDamage < 0 || attackDamage > MAX_ATTACK_DAMAGE) return false;
		if (attackRange < 0 || attackRange > MAX_ATTACK_RANGE) return false;
		if (visionRange < 0 || attackRange > MAX_VISION_RANGE) return false;
		return true;
	}

	private Soldier() {/* use Soldier.builder instead for validation */}

	private Soldier(int hitPoints, int attackDamage,
			int attackRange, int visionRange) {
		this.id = soldierIdCounter++;

		this.totalHitPoints = hitPoints;
		this.hitPoints = hitPoints;
		this.attackDamage = attackDamage;
		this.attackRange = attackRange;
		this.visionRange = visionRange;
	}

	/**
	 * Shortcut method to calculate the cost of this unit.
	 * @return cost
	 */
	public int calculateCost() {
		return Cost.calculateSoldierCost(hitPoints, attackDamage, attackRange, visionRange);
	}

	public String toString() {
		String ret = "Soldier: " + id + ", hp: " + hitPoints;
		return ret;
	}

	public boolean spendAction() {
		if (movesLeft <= 0) {
			return true;
		}
		movesLeft -= 1;
		return false;
	}

	public boolean hasAction() {
		return movesLeft <= 0;
	}

	public void resetActionCount() {
		movesLeft = movesPerTurn;
	}

}
