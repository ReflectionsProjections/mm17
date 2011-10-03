package edu.uiuc.acm.mechmania.objects;

public class Ship {
	private boolean alive;
	private double direction;
	private int[] position;
	private long id;
	private int[] velocity;
	private int health;
	private String owner;
	
	public boolean isAlive() {
		return alive;
	}
	public void setAlive(boolean alive) {
		this.alive = alive;
	}
	public double getDirection() {
		return direction;
	}
	public void setDirection(double direction) {
		this.direction = direction;
	}
	public int[] getPosition() {
		return position;
	}
	public void setPosition(int[] position) {
		this.position = position;
	}
	public long getId() {
		return id;
	}
	public void setId(long id) {
		this.id = id;
	}
	public int[] getVelocity() {
		return velocity;
	}
	public void setVelocity(int[] velocity) {
		this.velocity = velocity;
	}
	public int getHealth() {
		return health;
	}
	public void setHealth(int health) {
		this.health = health;
	}
	public String getOwner() {
		return owner;
	}
	public void setOwner(String owner) {
		this.owner = owner;
	}
}
