package MechMania17;

import java.io.*;
import java.util.*;
import java.util.zip.*;
import java.util.concurrent.*;
import java.util.concurrent.atomic.*;

import com.google.protobuf.GeneratedMessage;
import MechMania17.Mm17.*;
import MechMania17.Mm17.Command.*;

public class VizLoggerThread extends Thread {
	private final static String proto_logfile = "viz.pb.gz";
	private final static String arena_logfile = "arena.pb";

	private FileOutputStream os_proto = new FileOutputStream(proto_logfile);
	private GZIPOutputStream gz_proto = new GZIPOutputStream(os_proto);

	private FileOutputStream os_arena = new FileOutputStream(arena_logfile);

	private List<Player> players = null;
	private InitialResources initial_resources = null;
	private ConcurrentLinkedQueue<TurnContainer> turn_queue = null;
	private CountDownLatch writeLatch = null;
	private AtomicBoolean finished = null;

	public VizLoggerThread(List<Player> players, InitialResources initial_resources,
			ConcurrentLinkedQueue<TurnContainer> turn_queue, CountDownLatch writeLatch,
			AtomicBoolean finished) throws FileNotFoundException, IOException {
		this.players = players;
		this.initial_resources = initial_resources;
		this.turn_queue = turn_queue;
		this.finished = finished;
		this.writeLatch = writeLatch;
	}

	public void run() {
		try {
			setPlayers(players);
			setInitialResources(initial_resources);

			for (;;) {
				TurnContainer tc = turn_queue.poll();
				if (tc != null) {
					if (tc.game_state != null) {
						addGameState(tc.game_state, tc.turnCount);
					} else {
						addCommand(tc.player, tc.command, tc.succeeded, tc.turnCount);
					}
				} else if (finished.get()) {
					break;
				}
			}

			DeadPlayers.Builder deadPlayersBuilder = DeadPlayers.newBuilder();
			for (Player player : players) {
				if (player.alive == false) {
					DeadPlayers.DeadPlayer.Builder deadPlayer = DeadPlayers.DeadPlayer.newBuilder();
					deadPlayer.setName(player.name);
					if (player.disconnect_reason != null) {
						deadPlayer.setReason(player.disconnect_reason);
					} else {
						deadPlayer.setReason("unknown");
					}
					deadPlayersBuilder.addPlayers(deadPlayer.build());
				}
			}

			deadPlayersBuilder.build().writeDelimitedTo(os_arena);

			FinalScores.Builder finalScoreBuilder = FinalScores.newBuilder();
			for (Player player : players) {
				FinalScores.Score.Builder score = FinalScores.Score.newBuilder();
				score.setName(player.name);
				score.setScore(player.tilesOwned);
				finalScoreBuilder.addScores(score.build());
			}
			finalScoreBuilder.build().writeDelimitedTo(os_arena);

			System.out.println("flushing viz output");

			if (gz_proto != null) {
				gz_proto.finish();
				os_proto.flush();
				os_proto.close();
			}

			if (os_arena != null) {
				os_arena.flush();
				os_arena.close();
			}
		} catch (UnsupportedEncodingException uee) {
			uee.printStackTrace();
		} catch (IOException ie) {
			ie.printStackTrace();
		} finally {
			System.out.println("done flushing viz output");
			writeLatch.countDown();
		}
	}

	private void setPlayers(List<Player> players) throws UnsupportedEncodingException, IOException {
		PlayerList.Builder playerList = PlayerList.newBuilder();
		for (Player player : players) {
			ClientConnect.Builder clientConnectBuilder = ClientConnect.newBuilder();
			clientConnectBuilder.setName(player.name);
			clientConnectBuilder.setId(player.id);
			playerList.addPlayers(clientConnectBuilder.build());
		}
		playerList.build().writeDelimitedTo(gz_proto);
	}

	private void setInitialResources(InitialResources initial_resources) throws UnsupportedEncodingException, IOException {
		InitialResources.Builder initial_resources_builder = InitialResources.newBuilder(initial_resources);
		initial_resources_builder.build().writeDelimitedTo(gz_proto);
	}

	private void addCommand(Player p, Command com, boolean succeeded, int turnCount) throws UnsupportedEncodingException, IOException {
		Command.Builder command_builder = Command.newBuilder(com);
		command_builder.setId(p.id);
		command_builder.setSucceeded(succeeded);
		Turn.Builder turn_builder = Turn.newBuilder();
		turn_builder.setTurnCount(turnCount);
		turn_builder.setCommand(command_builder.build());
		turn_builder.build().writeDelimitedTo(gz_proto);
	}

	private void addGameState(GameState game_state, int turnCount) throws UnsupportedEncodingException, IOException {
		Turn.Builder turn_builder = Turn.newBuilder();
		turn_builder.setGameState(game_state);
		turn_builder.setTurnCount(turnCount);
		turn_builder.build().writeDelimitedTo(gz_proto);
	}
}
