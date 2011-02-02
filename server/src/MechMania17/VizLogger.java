package MechMania17;

import java.io.*;
import java.util.*;
import java.util.zip.*;
import java.util.concurrent.*;
import java.util.concurrent.atomic.*;

import com.google.protobuf.GeneratedMessage;
import MechMania17.Mm17.*;
import MechMania17.Mm17.Command.*;

public class VizLogger {
	private int turnCount = 0;
	private ConcurrentLinkedQueue<TurnContainer> turn_queue = new ConcurrentLinkedQueue<TurnContainer>();
	private AtomicBoolean finished = new AtomicBoolean(false);
	private CountDownLatch writeLatch = new CountDownLatch(1);

	public VizLogger(List<Player> players, InitialResources initial_resources) throws FileNotFoundException, IOException {
		VizLoggerThread vlt = new VizLoggerThread(players, initial_resources, turn_queue, writeLatch, finished);
		vlt.start();
	}

	public void newTurn() {
		++turnCount;
	}

	public void endTurn() {
	}

	public void addCommand(Player p, Command com, boolean succeeded) {
		turn_queue.add(new TurnContainer(p, com, succeeded, turnCount));
	}

	public void addGameState(GameState game_state) {
		turn_queue.add(new TurnContainer(game_state, turnCount));
	}

	public void writeOutput() {
		finished.set(true);
		for (;;) {
			try {
				writeLatch.await();
				break;
			} catch (InterruptedException ie) {
			}
		}
	}
}
