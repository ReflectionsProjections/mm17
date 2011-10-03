/**
 * Simple data structure for player information
 * 
 * Some of this may or may not be relevant as the development of the game
 * itself progresses.
 */

package edu.uiuc.acm.mechmania.infotypes;

import java.awt.Color;

import edu.uiuc.acm.mechmania.objects.Base;
import edu.uiuc.acm.mechmania.objects.Planet;
import edu.uiuc.acm.mechmania.objects.Refinery;
import edu.uiuc.acm.mechmania.objects.Ship;

public class PlayerInfo {
	private String name;
    private int id;
    private int ore_amount;
    private Ship[] ships;
    private Base[] bases;
    private Refinery[] refineries;
    private Planet[] planets;
    private Color color; 
	
    public String getName() {
		return name;
	}
	public void setName(String name) {
		this.name = name;
	}
	public int getId() {
		return id;
	}
	public void setId(int id) {
		this.id = id;
	}
	public int getOre_amount() {
		return ore_amount;
	}
	public void setOre_amount(int ore_amount) {
		this.ore_amount = ore_amount;
	}
	public Ship[] getShips() {
		return ships;
	}
	public void setShips(Ship[] ships) {
		this.ships = ships;
	}
	public Base[] getBases() {
		return bases;
	}
	public void setBases(Base[] bases) {
		this.bases = bases;
	}
	public Refinery[] getRefineries() {
		return refineries;
	}
	public void setRefineries(Refinery[] refineries) {
		this.refineries = refineries;
	}
	public Color getColor() {
		return color;
	}
	public void setColor(Color color) {
		this.color = color;
	}
	public Planet[] getPlanets() {
		return planets;
	}

}
