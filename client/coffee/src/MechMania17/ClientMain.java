package MechMania17;

import java.io.IOException;
import java.net.*;

public class ClientMain {
	public static String HOST = "localhost";
	public static int PORT = 6969;

	public static void main(String[] args) throws UnknownHostException,IOException {
		if (args.length < 1) {
			System.err.println("You must specify a name!");
			System.exit(-1);
		}
		Game g = new Game(args[0], HOST, PORT);

		do {
			System.out.println("turn: " + g.getTurnCount() + ", gold: " + g.getGold());
		} while (g.sendActions());
	}
}
