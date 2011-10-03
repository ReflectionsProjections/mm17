/**
 * LAUNCHER/STARTUP CLASS
 * 
 * Handles taking in a server, port number, authentication token, and a visual team name from
 * command line. This could easily be augmented to start up just with settings inside this
 * class, but this isn't recommended for competition play.
 */
package edu.uiuc.acm.mechmania;

public class MechManiaStartup {
	
	public static void main (String[] args) {
		long runtime = System.currentTimeMillis();
		
		if (args.length != 4) {
			printUsage();
			System.exit(1);
		}
		
		String serverHost = args[0];
		int serverPort = Integer.parseInt(args[1]);
		String authKey = args[2];
		String teamName = args[3];
		
		/****** START GAME ******/
		MechMania mechmania = new MechMania(serverHost, serverPort, authKey, teamName);
		mechmania.playGame();
		
		/****** GAME OVER ******/
		System.out.println("Run complete: " + (System.currentTimeMillis() - runtime) + " milliseconds");
	}
	
	private static void printUsage() {
		System.out.println("MechMania AI");
		System.out.println();
		System.out.println("Arguments: <server_host> <port> <authkey> <friendlyname>");
	}
	
}
