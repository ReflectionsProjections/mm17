/**
 * MechMania
 * 
 * The big enchilada.  This class contains most of the interfacing/logic
 * required to play a game.
 * 
 * This, or imports to, should be where you make most of your modifications.
 */

package edu.uiuc.acm.mechmania;

import java.net.URL;
import java.util.LinkedList;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;


import edu.uiuc.acm.mechmania.infotypes.GameInfo;
import edu.uiuc.acm.mechmania.infotypes.PlayerInfo;
import edu.uiuc.acm.mechmania.objects.*;

public class MechMania {
	/** Some useless defaults, these should be set by the startup module **/
	private String serverHost = "localhost";
	private int serverPort = 80;
	private String authKey = "authkey";
	private String teamName = "nonameteam";
	private MechManiaHTTPInterface httpInterface;
	
	/**
	 * Constructor
	 * @param serverHost Server hostname/IP
	 * @param serverPort Server port
	 * @param authKey Authentication token
	 * @param teamName Friendly team name
	 */
	public MechMania(String serverHost, int serverPort, String authKey, String teamName) {
		this.serverHost = serverHost;
		this.serverPort = serverPort;
		this.authKey  = authKey;
		this.teamName = teamName;
		
		this.httpInterface = new MechManiaHTTPInterface(this.serverHost, this.serverPort);
	}
	
	/**
	 * Main game logic/loop
	 */
	public void playGame() {
		// Start by joining a current game...
		if (joinGame()) {
			// We're in the game, so do some things that someone that might be in the game will do...
			GameInfo gameInfo = getGameInfo();
			
			/* DEPRECATED BY LONG-WAIT CALL
			while (gameInfo.isGameRunning() == false) {
				gameInfo = getGameInfo();
				System.out.println("Waiting for game to start...");
				// sleep(1);   // Deprecated by long-wait
				
			} */
			
			// Wait for game start using new long-wait call
			waitForTurn(0);
			
			// Keep track of the turn number
			int turnNumber = -1;
			
			// Do some intermediate work and continue until the game is over...
			while (gameInfo.getPlayerList().length > 1) {
				gameInfo = getGameInfo();
				turnNumber = getTurnNumber();
				
				JSONArray actions = new JSONArray();
				
				PlayerInfo playerInfo = getPlayerInfo();
				for (Ship ship : playerInfo.getShips()) {
					System.out.println("Ship: " + ship.getId());

					/*
					 * Ships can perform multiple actions at the same time.
					 * 
					 * To demonstrate this, we'll fly and shoot in random
					 * directions (hey, you're supposed to implement the AI!)
					 */
					try {
						JSONObject shipThrustActions = new JSONObject();
						JSONObject shipFireActions = new JSONObject();
						JSONObject shipFireArgs = new JSONObject();
						JSONObject shipThrustArgs = new JSONObject();
						
							shipFireActions.put("obj_type", "Ship");
							shipFireActions.put("obj_id", ship.getId());
							shipFireActions.put("command", "fire");
							JSONArray fireList = new JSONArray();
							fireList.put(35 * (Math.random() - 0.5));
							fireList.put(35 * (Math.random() - 0.5));
							shipFireArgs.put("direction", fireList);
							shipFireActions.put("args", shipFireArgs);
							actions.put(shipFireActions);

							JSONArray accelList = new JSONArray();
							shipThrustActions.put("command", "thrust");
							accelList.put(35 * (Math.random() - 0.5));
							accelList.put(35 * (Math.random() - 0.5));
							
							shipThrustArgs = new JSONObject();
							shipThrustArgs.put("direction", accelList);
							shipThrustArgs.put("speed", 20);

							shipThrustActions.put("obj_type", "Ship");
							shipThrustActions.put("obj_id", ship.getId());
							shipThrustActions.put("args", shipThrustArgs);
							actions.put(shipThrustActions);
					} catch (JSONException e) {
						e.printStackTrace();
					}
					
				}
				
				/*
				 * You should do something similar to above for the other types
				 * of objects (refineries, planets, bases).
				 * 
				 * Perhaps consider some helper functions, though?
				 * 
				 */
				
				/* for (Planet planet : playerInfo.getPlanets()) {
					System.out.println("Planet: " + planet.getId());
				} */
				
/*				for (Refinery refinery : playerInfo.getRefineries()) {
					
				}
				
				for (Base base : playerInfo.getBases()) {
					
				}*/
				
				/*
				 * Assemble the final JSON object containing this turn's actions
				 * and send it to the server
				 */
				JSONObject postData = new JSONObject();
				try {
					postData.put("auth", authKey);
					postData.put("actions", actions);
				} catch (JSONException e) {
					e.printStackTrace();
				}
				
				URL turnUrl = httpInterface.buildRequestURL("/game/turn/" + getTurnNumber());
				System.out.println(postData.toString());
				JSONObject response = httpInterface.getResponse(turnUrl,postData);
				
				System.out.println(response.toString());  // Just so you can see what's going on
														  // You should turn this off.
				
				
				// At the end of the turn, poll every two seconds or so until the turn number changes...
				/*   DEPRECATED BY LONG-WAIT
				while (turnNumber <= gameInfo.getCurrentTurn()) {
					turnNumber = getTurnNumber();
					System.out.println("Sleeping until next turn starts... (currently turn " + turnNumber + ")");
					sleep(1);
				} */
				
				// Long-wait
				waitForTurn(turnNumber + 1);
			}
		}
		else {
			System.out.println("Couldn't join game on " + serverHost + ":" + serverPort);
		}
	}

	/**
	 * Builds and sends
	 * @return boolean representing successful join
	 */
	private boolean joinGame() {
		String[] joinArguments = {"auth=" + authKey, 
								  "name=" + teamName};
		URL joinGameUrl = httpInterface.buildRequestURL("/game/join", joinArguments);
		JSONObject response = httpInterface.getResponse(joinGameUrl);
		
		try {
			return (response.getBoolean("success") == true);  // Did we get in?
		} catch (JSONException e) {
			return false;
		}
	}
	
	/**
	 * Get game status info
	 * @return GameInfo object representing the current game status
	 */
	private GameInfo getGameInfo() {
		URL gameInfoUrl = httpInterface.buildRequestURL("/game/info");
		JSONObject response = httpInterface.getResponse(gameInfoUrl);

		GameInfo returnVal = new GameInfo();
		try {
			returnVal.setGameRunning(response.getBoolean("game_active"));
			returnVal.setCurrentTurn(response.getInt("turn"));
			
			JSONArray playerArray = response.getJSONArray("active_players");
			String[] playerList = new String[playerArray.length()];
			for (int i = 0; i < playerArray.length(); i++) {
				playerList[i] = playerArray.getString(i);
			}
			returnVal.setPlayerList(playerList);
			
		}
		catch (Exception e) {
			e.printStackTrace();
		}
		
		return returnVal;
	}
	
	/**
	 * Get current player info
	 * @return PlayerInfo representing current player/piece/event status
	 */
	private PlayerInfo getPlayerInfo() {
		String[] requestArguments = {"auth=" + authKey};
		URL gameInfoUrl = httpInterface.buildRequestURL("/game/info/all", requestArguments);
		JSONObject response = httpInterface.getResponse(gameInfoUrl);

		PlayerInfo returnVal = new PlayerInfo();
		try {
			long myID = response.getLong("you");  // We receive a special "owner" token each turn
			JSONArray objects = response.getJSONArray("objects");
			System.out.println(objects.toString()); 
			
			LinkedList<Base> baseList = new LinkedList<Base>();
			LinkedList<Refinery> refineryList = new LinkedList<Refinery>();
			LinkedList<Ship> shipList = new LinkedList<Ship>();
			
			// Iterate throught the list of objects we get back
			for (int i = 0; i < objects.length(); i++) {
				JSONObject object = (JSONObject) objects.get(i);
				String objectType = object.getString("type");
				long objectOwner;
				try {
					objectOwner = object.getLong("owner");  
				}
				catch (JSONException e) {
					objectOwner = 0;
				}
				
				// Return the list of our ships, so make sure they have our owner token
				if (objectType.equals("Ship") && objectOwner == myID) {
					Ship newShip = new Ship();
					newShip.setDirection(object.getInt("direction"));
					newShip.setHealth(object.getInt("health"));
					newShip.setId(object.getLong("id"));
					shipList.add(newShip);
				}
				
				//TODO: You'll want to iterate through the other types of objects
			}
			
			// Add the three 
			returnVal.setBases(baseList.toArray(new Base[0]));
			returnVal.setRefineries(refineryList.toArray(new Refinery[0]));
			returnVal.setShips(shipList.toArray(new Ship[0]));
		}
		catch (Exception e) {
			e.printStackTrace();
		}
		
		return returnVal;
	}
	
	/**
	 * Gets current turn number
	 * @return turn number
	 */
	private int getTurnNumber() {
		URL turnNumberUrl = httpInterface.buildRequestURL("/game/turn");
		JSONObject response = httpInterface.getResponse(turnNumberUrl);
		
		try {
			return response.getInt("turn");
		} catch (JSONException e) {
			return -1;
		}
		
	}

	/**
	 * Returns the instance of the HTTP interface in use
	 * @return HTTP interface object
	 */
	protected MechManiaHTTPInterface getInterface() {
		return this.httpInterface;
	}
	
	/**
	 * Makes a call to the new long-polling wait
	 * @param waitUntilTurnNumber Turn number to wait until
	 */
	private void waitForTurn(int waitUntilTurnNumber) {
		String[] turnWaitArgs = {"turn=" + waitUntilTurnNumber};
		URL waitURL = httpInterface.buildRequestURL("/game/wait",turnWaitArgs);
		httpInterface.getResponse(waitURL);
	}
	
	/**
	 * Convenience function to pause execution temporarily
	 * (we don't want to constantly poll the server, do we?)
	 *
	 * @deprecated
	 * @param secs Number of seconds to wait
	 */
	private void sleep(int secs) {
		try {  // Wait 3s to start again...
			Thread.sleep(secs * 1000);
		} catch (InterruptedException e) {}
	}
	
}
