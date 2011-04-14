package MechMania17;

import java.lang.*;

class Cost
{
	private static final int SUBMARINE_COST = 200;

	/**
	 * Calculates the cost of a soldier
	 * @param hitPoints
	 * @param attackDamage
	 * @param attackRange
	 * @param visionRange
	 * @return cost
	 */
	public static int calculateSoldierCost(int hitPoints, int attackDamage,
			int attackRange, int visionRange) {
		// base cost is 50 per guy
		int cost = 50;

		int hitPointCost = 2 * ((int)Math.sqrt(hitPoints) + 1);
		int attackDamageCost = (int)Math.sqrt(attackDamage) + 1;
		int attackRangeCost = attackRange;
		int visionRangeCost = visionRange * visionRange;
		if (visionRangeCost < visionRange) {
			visionRangeCost = -1;
		}

		if (hitPointCost <= 0)
			return -1;
		cost += hitPointCost;

		if (Integer.MAX_VALUE - attackDamageCost < cost || attackDamageCost < 0)
			return -1;
		cost += attackDamageCost;

		if (Integer.MAX_VALUE - attackRangeCost < cost || attackRangeCost < 0)
			return -1;
		cost += attackRangeCost;

		if (Integer.MAX_VALUE - visionRangeCost < cost || visionRangeCost < 0)
			return -1;
		cost += visionRangeCost;

		return cost;
	}

	/**
	 * Calculates the cost of a submarine
	 */
	public static int calculateSubmarineCost() {
		return SUBMARINE_COST;
	}

};
