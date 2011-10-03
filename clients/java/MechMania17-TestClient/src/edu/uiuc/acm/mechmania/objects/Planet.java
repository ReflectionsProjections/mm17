/**
 * Planet
 * 
 * Contains relevant information about a planet
 * 
 */

package edu.uiuc.acm.mechmania.objects;

public class Planet {
	private long id;
	private int resources;
	private int[] position;
	private int size;
	private int base = 0;
	
	public long getId() {
		return id;
	}
	public void setId(long id) {
		this.id = id;
	}
	public int getResources() {
		return resources;
	}
	public void setResources(int resources) {
		this.resources = resources;
	}
	public int[] getPosition() {
		return position;
	}
	public void setPosition(int[] position) {
		this.position = position;
	}
	public int getSize() {
		return size;
	}
	public void setSize(int size) {
		this.size = size;
	}
	public int getBase() {
		return base;
	}
	public void setBase(int base) {
		this.base = base;
	}
}
