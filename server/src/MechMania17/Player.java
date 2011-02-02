package MechMania17;

import java.io.*;
import java.net.*;
import java.util.HashMap;
import java.util.concurrent.*;
import java.util.concurrent.atomic.*;
import java.util.logging.*;

import MechMania17.Mm17.*;
import MechMania17.Mm17.Actions.*;

public class Player {
	public int gold = 500; // some starting gold

	public int id;
	volatile public int tilesOwned;
	public HashMap<Integer, Submarine> submarines = new HashMap<Integer, Submarine>();
	volatile public String name = "unknown";
	volatile public CountDownLatch latch;
	public BlockingQueue<Actions> message_queue_from = new LinkedBlockingQueue<Actions>(1);
	public BlockingQueue<GameState> message_queue_to = new LinkedBlockingQueue<GameState>(1);
	public int unitsOwned = 1;

	volatile public boolean alive = true;
	volatile public String disconnect_reason = null;
	volatile public InitialResources initial_resources = null;
	private Socket socket;

	public Player(int id, Socket socket) throws Exception {
		this.id = id;
		this.tilesOwned = 1;
		this.socket = socket;
	}

	public Submarine locateSubmarineById(int id) {
		return submarines.get(id);
	}

	public void addSubmarine(Submarine sub) {
		submarines.put(sub.id, sub);
	}

	public void removeSubmarine(Submarine sub) {
		submarines.remove(sub.id);
	}

	public void writeInitialResources(InitialResources initial_resources) throws IOException {
		initial_resources.writeDelimitedTo(socket.getOutputStream());
	}
}
