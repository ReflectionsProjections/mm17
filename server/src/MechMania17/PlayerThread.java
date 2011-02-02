package MechMania17;

import java.io.*;
import java.net.*;
import java.util.HashMap;
import java.util.concurrent.*;
import java.util.concurrent.atomic.*;
import java.util.logging.*;

import MechMania17.Mm17.*;
import MechMania17.Mm17.Actions.*;

public class PlayerThread extends Thread {
	private Socket socket = null;
	private BufferedInputStream bis = null;
	private Handler logging = null;
	private Player player = null;

	public PlayerThread(Player player, Socket socket, Handler logging) throws Exception {
		this.socket = socket;
		this.player = player;
		this.logging = logging;
		this.bis = new BufferedInputStream(socket.getInputStream());

		ClientConnect hello = ClientConnect.parseDelimitedFrom(bis);
		this.player.name = hello.getName();
		logging.publish(new LogRecord(Level.INFO, "Player " + Integer.toString(player.id) + ": " + this.player.name));
	}

	private void writeGameState(GameState game_state) throws IOException {
		game_state.writeDelimitedTo(socket.getOutputStream());
	}

	private Actions readActions() throws IOException {
		return Actions.parseDelimitedFrom(bis);
	}

	public void run() {
		while (true) {
			try {
				writeGameState(player.message_queue_to.take());
				// check if I should die
				if (!player.alive) {
					logging.publish(new LogRecord(Level.INFO, "Player " + player.id + " was disconnected"));
					break;
				}
				Actions actions = readActions();
				if (actions == null) {
					player.disconnect_reason = "Could not parse client actions";
					break;
				}
				player.message_queue_from.put(actions);
				player.latch.countDown();
			} catch (IOException ioe) {
				player.disconnect_reason = ioe.getMessage();
				ioe.printStackTrace();
				break;
			} catch (InterruptedException iee) {
				iee.printStackTrace();
			}
		}
		player.alive = false;
		try {
			socket.close();
		} catch (IOException ioe) {
			ioe.printStackTrace();
		}
	}
}
