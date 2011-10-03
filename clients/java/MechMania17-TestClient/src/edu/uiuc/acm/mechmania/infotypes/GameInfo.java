/**
 * GameInfo Data structures
 * 
 * Just some basic status info about the game in progress
 */

package edu.uiuc.acm.mechmania.infotypes;

public class GameInfo {
	private boolean gameRunning = false;
	private int currentTurn = 0;
	private String[] playerList;
	
	public boolean isGameRunning() {
		return gameRunning;
	}
	public void setGameRunning(boolean gameRunning) {
		this.gameRunning = gameRunning;
	}
	public int getCurrentTurn() {
		return currentTurn;
	}
	public void setCurrentTurn(int currentTurn) {
		this.currentTurn = currentTurn;
	}
	public String[] getPlayerList() {
		return playerList;
	}
	public void setPlayerList(String[] playerList) {
		this.playerList = playerList;
	}
}
