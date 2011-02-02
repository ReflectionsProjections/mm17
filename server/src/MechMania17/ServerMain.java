package MechMania17;

import gnu.getopt.Getopt;

import java.io.IOException;
import java.net.*;
import java.util.*;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.CountDownLatch;
import java.util.logging.*;

import MechMania17.Mm17.Actions;
import MechMania17.Mm17.ClientConnect;
import MechMania17.Mm17.GameState;
import MechMania17.Mm17.InitialResources;

import com.google.protobuf.GeneratedMessage;

public class ServerMain {


	public static class OneLineFormatter extends java.util.logging.Formatter {
		public OneLineFormatter() {
		}

		public String format(LogRecord record) {
			return "[" + record.getLevel() + "] " + record.getMessage() + "\n";
		}
	}

	public static void main(String[] argv) throws IOException {
		int turncount = 500;
		boolean verbose = false;
		String mapFile = null;

		Getopt g = new Getopt("MM16", argv, "p:t:m:v");
		int c;
		String arg;

		int PLAYER_COUNT = 1; // Just a default
		int PLAYERS_CONNECTED = 0;

		int SERVER_PORT = 6969;

		while ((c = g.getopt()) != -1) {
			switch (c) {
			case 'p':
				arg = g.getOptarg();
				try {
					PLAYER_COUNT = Integer.parseInt(arg);
				} catch (NumberFormatException ne) {
					System.err.println("You gave -p a noninteger: " + arg);
					System.exit(-1);
				}
				break;
			case 't':
				arg = g.getOptarg();
				try {
					turncount = Integer.parseInt(arg);
				} catch (NumberFormatException ne) {
					System.err.println("You gave -t a noninteger: " + arg);
					System.exit(-1);
				}
				break;
			case 'm':
				mapFile = g.getOptarg();
				break;
			case 'v':
				verbose = true;
				break;
			case '?':
				break;
			default:
				System.out.println("FAIL");
				break;
			}
		}
		ServerSocket serverSocket = null;

		try {
			serverSocket = new ServerSocket(SERVER_PORT);
		} catch (IOException e) {
			e.printStackTrace();
			System.exit(-1);
		}

		// TODO: Add support for more debug levels
		Handler logging = new ConsoleHandler();
		logging.setFormatter(new OneLineFormatter());
		if (verbose)
			logging.setLevel(Level.FINE);
		else
			logging.setLevel(Level.INFO);

		logging.publish(new LogRecord(Level.INFO, "== Starting MechMania17 Server =="));

		serverSocket.setSoTimeout(10000);
		ArrayList<Player> players = new ArrayList<Player>();
		for (PLAYERS_CONNECTED = 1; PLAYERS_CONNECTED <= PLAYER_COUNT; PLAYERS_CONNECTED++) {
			try {
				Socket socket = serverSocket.accept();
				Player player = new Player(PLAYERS_CONNECTED, socket);
				PlayerThread player_thread = new PlayerThread(player, socket, logging);
				players.add(player);
				player_thread.start();
			} catch (SocketTimeoutException e) {
				logging.publish(new LogRecord(Level.SEVERE, "Timed out waiting to accept new connections"));
				break;
			} catch (Exception e) {
				e.printStackTrace();
			}
		}

		MapGrid map = new MapGrid(mapFile);

		Game mm = new Game(turncount, map, players, logging);
		mm.play();
	}
}
