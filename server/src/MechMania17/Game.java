package MechMania17;

import java.io.*;
import java.util.*;
import java.util.concurrent.*;
import java.util.logging.*;

import com.google.protobuf.GeneratedMessage;
import com.google.protobuf.*;
import MechMania17.Mm17.*;
import MechMania17.Mm17.Actions.*;
import MechMania17.Mm17.Command.*;

public class Game {
	private List<Player> all_players;
	private List<Player> active_players;

	private MapGrid map;

	private Handler logging;

	private VizLogger vizLog = null;

	private int num_turns;

	private class SummonCommandHelper {
		public Player player;
		public Command command;
		public SummonCommandHelper(Player player, Command command) {
			this.player = player;
			this.command = command;
		}
	}

	public Game(int num_turns, MapGrid map, List<Player> all_players, Handler logging) throws FileNotFoundException, UnsupportedEncodingException, IOException {
		this.active_players = new ArrayList<Player>(all_players);
		this.all_players = all_players;
		this.logging = logging;
		this.num_turns = num_turns;
		this.map = map;
	}

	private void send_initial_resources(InitialResources initial_resources_proto) {
		Iterator<Player> itr = active_players.iterator();
		while (itr.hasNext()) {
			Player player = itr.next();
			InitialResources.Builder initial_resources_builder = InitialResources.newBuilder(initial_resources_proto);
			initial_resources_builder.setId(player.id);
			InitialResources initial_resources = initial_resources_builder.build();
			try {
				player.writeInitialResources(initial_resources);
			} catch (IOException e) {
				player.alive = false;
				active_players.remove(player);
				if (player.disconnect_reason == null) {
					player.disconnect_reason = "Could not send player initial resources: " + e.getMessage();
				}
			}
		}
	}

	private void reset_unit_actions() {
		// reset all units move counts
		for (int x = 0; x < map.size; x++) {
			for (int y = 0; y < map.size; y++) {
				Tile tile = map.getTile(x, y);
				for (Soldier unit : tile.getAllUnits()) {
					unit.resetActionCount();
				}
			}
		}
	}

	private void reset_sub_actions() {
		for (Player player : active_players) {
			for (Submarine sub : player.submarines.values()) {
				sub.resetActionCount();
			}
		}
	}

	private void reset_actions() {
		reset_unit_actions();
		reset_sub_actions();
	}

	private void send_gamestate(CountDownLatch latch) throws UnsupportedEncodingException, IOException {
		Iterator<Player> itr = active_players.iterator();
		while (itr.hasNext()) {
			Player player = itr.next();
			GameState game_state = getGameState(player);
			vizLog.addGameState(game_state);
			player.latch = latch;
			if (player.message_queue_to.offer(game_state) == false) {
				// terminate the player
				player.alive = false;
				itr.remove();
				latch.countDown();
				if (player.disconnect_reason == null) {
					player.disconnect_reason = "Player was too slow sending actions";
				}
			}
		}
	}

	private Map<Player, ListIterator<Command>> receive_actions() {
		Map<Player, ListIterator<Command>> player_commands = new HashMap<Player, ListIterator<Command>>();

		Iterator<Player> itr = active_players.iterator();
		itr = active_players.iterator();
		while (itr.hasNext()) {
			Player player = itr.next();
			Actions turnActions = player.message_queue_from.poll();
			if (turnActions == null) {
				player.alive = false;
				itr.remove();
				if (player.disconnect_reason == null) {
					player.disconnect_reason = "Player was too slow receiving actions";
				}
			} else {
				player_commands.put(player, turnActions.getActionsList().listIterator());
			}
		}
		return player_commands;
	}

	public void play() throws IOException {
		for (Player player : active_players) {
			map.add(player);
		}

		InitialResources initial_resources_proto = getInitialResources().setId(0).build();
		vizLog = new VizLogger(all_players, initial_resources_proto);
		send_initial_resources(initial_resources_proto);

		int turnCount = 0;
		for (; turnCount < num_turns; turnCount++) {
			reset_actions();

			CountDownLatch latch = new CountDownLatch(active_players.size());
			vizLog.newTurn();
			send_gamestate(latch);

			// sleep for two seconds
			try {
				latch.await(2L, TimeUnit.SECONDS);
			} catch (InterruptedException ie) {
				ie.printStackTrace();
			}

			Map<Player, ListIterator<Command>> player_commands = receive_actions();

			List<Player> playing_players = new ArrayList<Player>(active_players);

			ArrayList<SummonCommandHelper> summon_commands = new ArrayList<SummonCommandHelper>();

			while (!playing_players.isEmpty()) {
				Collections.shuffle(playing_players);
				Iterator<Player> itr = active_players.iterator();
				itr = playing_players.iterator();
				while (itr.hasNext()) {
					Player player = itr.next();
					ListIterator<Command> command_itr = player_commands.get(player);
					while (command_itr.hasNext()) {
						Command command = command_itr.next();
						if (command.getType() == CommandType.SUMMON) {
							summon_commands.add(new SummonCommandHelper(player, command));
						} else {
							boolean succeeded = playAction(player, command);
							vizLog.addCommand(player, command, succeeded);
							break;
						}
					}
					if (!command_itr.hasNext()) {
						itr.remove();
					}
				}
			}

			for (SummonCommandHelper summon_command : summon_commands) {
				Player player = summon_command.player;
				Command command = summon_command.command;
				boolean succeeded = playAction(player, command);
				vizLog.addCommand(player, command, succeeded);
			}

			int playersWithUnits = 0;
			for (Player player : all_players) {
				player.tilesOwned = map.tilesOwnedByPlayer(player.id);
				if (player.unitsOwned > 0) {
					++playersWithUnits;
				}
			}
			for (Player player : active_players) {
				incrementGold(player);
			}
			vizLog.endTurn();

			printInfo("TURN " + turnCount);
			if (all_players.size() > 1) {
				if (playersWithUnits <= 1) {
					break;
				}
			}
		}

		if (turnCount != num_turns) {
			vizLog.newTurn();
			for (Player player : all_players) {
				player.tilesOwned = map.tilesOwnedByPlayer(player.id);
				if (player.unitsOwned > 0) {
					GameState game_state = getGameState(player);
					vizLog.addGameState(game_state);
				}
			}
			vizLog.endTurn();
		}

		// Endgame logic
		printInfo("==== Scores ====");
		printInfo("Player\tScore");
		for (Player player : all_players) {
			printInfo(Integer.toString(player.id) + "\t" + player.tilesOwned);
		}
		vizLog.writeOutput();
		System.exit(0);
	}

	public InitialResources.Builder getInitialResources() {
		InitialResources.Builder initial = InitialResources.newBuilder();
		initial.setMapWidth(map.size);
		for (int y = 0; y < map.size; y++) {
			for (int x = 0; x < map.size; x++) {
				InitialResources.Tile.Builder tile = InitialResources.Tile
					.newBuilder();
				tile.setType(map.getTile(x, y).toProtoType());
				tile.setX(x);
				tile.setY(y);
				initial.addTiles(tile);
			}
		}
		return initial;
	}

	/**
	 * Generates a GameState object for the given player based on what they can
	 * see at a given time.
	 * @param player
	 * @return state
	 */
	public GameState getGameState(Player player) {
		GameState.Builder gameState = GameState.newBuilder();
		gameState.setGold(player.gold);
		gameState.setId(player.id);

		// Find what tiles to tell them about
		boolean[][] visibleTiles = new boolean[map.size][map.size];
		for (int x = 0; x < map.size; x++) {
			for (int y = 0; y < map.size; y++) {
				Tile tile = map.getTile(x, y);
				if (tile.hasUnitFromPlayer(player)) {
					visibleTiles[x][y] = true;
					// find the unit with the best sight, then mark all the offsets
					int maxVision = tile.getMaxVisionForPlayer(player);

					Location unitLocation = new Location(x, y);
					for (int x2 = 0; x2 < map.size; x2++) {
						for (int y2 = 0; y2 < map.size; y2++) {
							Location targetLocation = new Location(x2, y2);
							if (unitLocation.getDistance(targetLocation) <= maxVision) {
								visibleTiles[x2][y2] = true;
							}
						}
					}
				}
			}
		}

		for (int x = 0; x < map.size; x++) {
			for (int y = 0; y < map.size; y++) {
				if (visibleTiles[x][y]) {
					Tile tile = map.getTile(x, y);
					GameState.Tile.Builder gameStateTile = GameState.Tile.newBuilder();
					gameStateTile.setOwner(tile.getOwner());
					gameStateTile.setX(x);
					gameStateTile.setY(y);

					// I wish there was a nicer way of doing this.
					// I guess we could hold the unit internally as a PB object, but... no.
					for (Soldier unit : tile.getAllUnits()) {
						GameState.Unit.Builder gameStateUnit =
							GameState.Unit.newBuilder();
						gameStateUnit.setHp(unit.hitPoints);
						gameStateUnit.setDamage(unit.attackDamage);
						gameStateUnit.setRange(unit.attackRange);
						gameStateUnit.setVision(unit.visionRange);
						gameStateUnit.setId(unit.id);
						gameStateUnit.setOwner(tile.getUnitOwner(unit));

						gameStateTile.addUnits(gameStateUnit);
					}
					gameState.addTiles(gameStateTile);
				}
			}
		}

		for (Submarine sub : player.submarines.values()) {
			GameState.Submarine.Builder gameStateSub =
				GameState.Submarine.newBuilder();
			gameStateSub.setId(sub.id);
			gameStateSub.setX(sub.loc.getX());
			gameStateSub.setY(sub.loc.getY());
			gameStateSub.setSubmerged(sub.submerged);

			for (Soldier unit : sub.internalStorage.values()) {
				GameState.Unit.Builder gameStateUnit =
					GameState.Unit.newBuilder();
				gameStateUnit.setHp(unit.hitPoints);
				gameStateUnit.setDamage(unit.attackDamage);
				gameStateUnit.setRange(unit.attackRange);
				gameStateUnit.setVision(unit.visionRange);
				gameStateUnit.setId(unit.id);
				gameStateUnit.setOwner(player.id);

				gameStateSub.addUnits(gameStateUnit);
			}
			gameState.addSubmarines(gameStateSub);
		}

		return gameState.build();
	}

	public boolean playAction(Player p, Command action) {
		boolean succeeded = false;

		// note that the action might be not set if they did not provide it

		switch (action.getType()) {
		case SUMMON:
			if (!action.hasSummon()) {
				printInfo("protocol error: no summon message with summon type");
			} else {
				succeeded = playSummonCommand(p, action.getSummon());
			}
			break;

		case MOVE:
			if (!action.hasMove()) {
				printInfo("protocol error: no move message with move type");
			} else {
				succeeded = playMoveCommand(p, action.getMove());
			}
			break;

		case ATTACK:
			if (!action.hasAttack()) {
				printInfo("protocol error: no attack message with attack type");
			} else {
				succeeded = playAttackCommand(p, action.getAttack());
			}
			break;

		case LOADSUB:
			if (!action.hasLoadSub()) {
				printInfo("protocol error: no load sub message with load sub type");
			} else {
				printFine("Loading sub");
				succeeded = playLoadSubCommand(p, action.getLoadSub());
			}
			break;

		case MOVESUB:
			if (!action.hasMoveSub()) {
				printInfo("protocol error: no move sub message with move sub type");
			} else {
				printFine("Moving sub");
				succeeded = playMoveSubCommand(p, action.getMoveSub());
			}
			break;

		case ATTACHSUB:
			if (!action.hasAttachSub()) {
				printInfo("protocol error: no AttachSub message with AttachSub type");
			} else {
				printFine("Attaching sub");
				succeeded = playAttachSubCommand(p, action.getAttachSub());
			}
			break;

		case SUMMONSUB:
			if (!action.hasSummonSub()) {
				printInfo("protocol error: no summon sub message with summon sub type");
			} else {
				printFine("Summoning sub");
				succeeded = playSummonSubCommand(p, action.getSummonSub());
			}
			break;

		default:
			printSevere("player: " + p.id + " with " + action.getType() + " not implemented :(");
		}
		return succeeded;
	}

	private boolean playSummonCommand(Player p, SummonCommand summon) {
		// check if tile is passable
		Location location = new Location(summon.getX(), summon.getY());
		if (!map.isTilePassable(location)) {
			printInfo("summon: passability mismatch");
			return false;
		}

		// check ownership
		Tile tile = map.getTile(summon.getX(), summon.getY());
		if (tile.getOwner() != p.id) {
			printInfo("summon: ownership mismatch");
			return false;
		}

		if (tile.units.size() >= Tile.UNIT_CAP) {
			printInfo("summon: unit cap reached at: " + location);
			return false;
		}

		Soldier unit = Soldier.builder(summon.getHp(), summon.getDamage(),
				summon.getRange(), summon.getVision());

		if (unit == null) {
			printInfo("unit properties are not valid");
			return false;
		}

		// check cost
		int cost = unit.calculateCost();
		if (cost > p.gold || cost <= 0) {
			printInfo("unit cost error: not affordable by player OR unit is free/negative priced");
			return false;
		}
		p.gold -= cost;
		printFine("cost of unit was " + Integer.toString(cost) + ", player has " + Integer.toString(p.gold) + " gold left");

		// actually place unit
		map.addUnit(location, unit);

		// change ownership
		map.getTile(summon.getX(), summon.getY()).setOwner(p.id);
		++p.unitsOwned;
		return true;
	}

	private boolean playLoadSubCommand(Player p, LoadSubCommand load) {
		Location pair = map.getUnitLocation(load.getUnit());
		if (pair == null) return false;

		Tile tile = map.getTileUnsafe(pair);
		Soldier unit = tile.getUnitById(load.getUnit());

		Submarine sub = p.locateSubmarineById(load.getSubmarine());

		if (unit == null || sub == null) {
			printInfo("Sub or unit is null! Badness!" + unit + " " + sub);
			return false;
		}

		// check if soldier can get on sub
		Location unitLocation = map.getUnitLocation(unit.id);
		if (!Location.isValid(unitLocation)) return false;

		if (unitLocation.getDistance(sub.getLocation()) > 1) {
			printInfo("cannot board from that far away");
			return false;
		}

		if (sub.internalStorage.size() >= Tile.UNIT_CAP) {
			printInfo("sub " + sub.id + " is full");
			return false;
		}

		if (sub.hasAction() && unit.hasAction()) {
			printInfo("sub " + sub.id + " does not have action or unit does not have action");
			return false;
		}
		sub.spendAction();
		unit.spendAction();

		printFine("Loading sub " + sub.id + " with " + unit.id);
		// put soldier on sub
		sub.load(unit);
		// delete soldier from world
		map.removeUnit(unit);
		return true;
	}

	private boolean playMoveSubCommand(Player p, MoveSubCommand movesub) {
		Submarine sub = p.locateSubmarineById(movesub.getSubmarine());

		if (sub == null) {
			printInfo("Sub is null! Badness!");
			return false;
		}

		if (sub.isSubmerged()) {
			printInfo("submarine " + sub.id  + " cannot be moved while submerged");
			return false;
		}

		Location loc = new Location(movesub.getX(), movesub.getY());
		if (!map.isTileWater(loc)) {
			printInfo("sub " + sub.id  + " cannot move here " + loc + "!");
			return false;
		}

		// can we actually move? if not, don't move
		if (sub.spendAction()) {
			printInfo("sub " + sub.id + " does not have action");
			return false;
		}

		printFine("Moving sub " + sub.id + " to " + loc);
		sub.move(loc);
		return true;
	}

	private boolean playAttachSubCommand(Player p, AttachSubCommand attachsub) {
		Submarine sub = p.locateSubmarineById(attachsub.getSubmarine());

		if (sub == null) {
			printInfo("Sub is null! Badness!");
			return false;
		}

		Tile tile = map.getTile(sub.loc);

		if (sub.isSubmerged()) {
			printInfo("submarine " + sub.id  + " cannot attach while submerged");
			return false;
		}

		if (!map.isTilePassable(sub.loc.of(Direction.NORTH)) &&
				!map.isTilePassable(sub.loc.of(Direction.SOUTH)) &&
				!map.isTilePassable(sub.loc.of(Direction.EAST)) &&
				!map.isTilePassable(sub.loc.of(Direction.WEST))) {
			printInfo("must have land to attach sub");
			return false;
		}

		if (tile.hasSubmarineFromPlayer(p)) {
			printInfo("[attach] already has submarine from player");
			return false;
		}

		if (sub.spendAction()) {
			printInfo("sub " + sub.id + " does not have action");
			return false;
		}

		printFine("Attaching sub " + sub.id + " at " + sub.loc);
		tile.submarines.put(sub.id, sub);
		for (Soldier unit : sub.internalStorage.values()) {
			map.setUnitLocation(unit.id, sub.loc);
		}
		p.removeSubmarine(sub);
		return true;
	}

	private boolean playSummonSubCommand(Player p, SummonSubCommand summon) {
		// check if tile is water
		Location loc = new Location(summon.getX(), summon.getY());
		if (!map.isTileWater(loc)) {
			return false;
		}

		Submarine sub = Submarine.builder(map, loc, p);

		if (sub == null) {
			printInfo("unit properties are not valid");
			return false;
		}

		// check cost
		int cost = sub.calculateCost();
		if (cost > p.gold || cost <= 0) {
			printInfo("unit cost error: not affordable by player OR unit is free/negative priced");
			return false;
		}
		p.gold -= cost;
		printFine("cost of submarine was " + Integer.toString(cost) + ", player has " + Integer.toString(p.gold) + " gold left");

		p.addSubmarine(sub);
		printFine("Summoning sub success! at: " + loc);
		return true;
	}

	private boolean playAttackCommand(Player p, AttackCommand attack) {
		Location unitLocation = map.getUnitLocation(attack.getSource());
		if (unitLocation == null) return false;

		Soldier source = map.getTileUnsafe(unitLocation).getUnitById(attack.getSource());

		Location targetLocation = map.getUnitLocation(attack.getTarget());
		if (targetLocation == null) return false;

		Soldier target = map.getTileUnsafe(targetLocation).getUnitById(attack.getTarget());

		// range check
		if (unitLocation.getDistance(targetLocation) > source.attackRange) {
			printFine("[attack] pid=" + p.id + "'s unit " + attack.getSource() + " with range " + source.attackRange
					+ " cannot attack unit " + attack.getTarget() + " from " + unitLocation + " to " + targetLocation);
			return false;
		}

		if (source.spendAction()) {
			printFine("[attack] pid=" + p.id + "'s unit " + attack.getSource() + " has already performed an action this turn");
			return false;
		}

		// apply damage
		target.hitPoints -= source.attackDamage;
		printFine("[attack] pid=" + p.id + "'s unit " + attack.getSource() + " has done " + source.attackDamage + " damage");

		// removal check
		if (target.hitPoints <= 0) {
			printFine("[attack] pid=" + p.id + "'s unit " + attack.getSource() + " has killed " + attack.getTarget());
			Tile tile = map.getTileUnsafe(targetLocation);
			for (Player target_player : all_players) {
				if (target_player.id == tile.getOwner()) {
					--target_player.unitsOwned;
					break;
				}
			}
			map.removeUnit(target);
		}
		return true;
	}

	private boolean playMoveCommand(Player p, MoveCommand move) {
		Location unitLocation = map.getUnitLocation(move.getId());
		if (unitLocation == null) return false;

		Tile tile = map.getTileUnsafe(unitLocation);

		Soldier unit = tile.getUnitById(move.getId());

		if (tile.getUnitOwner(unit) != p.id) {
			printFine("[move] pid=" + p.id + " does not own unit " + unit.id);
			return false;
		}

		Location destination = unitLocation.of(move.getDirection());

		if (!map.isTilePassable(destination)) {
			printFine("[move] pid=" + p.id + "'s unit " + unit.id + " cannot move to " + destination + "!");
			return false;
		}

		Tile destination_tile = map.getTileUnsafe(destination);

		if (destination_tile.units.size() >= Tile.UNIT_CAP) {
			printInfo("[move]: unit cap reached at: " + destination);
			return false;
		}

		if (unit.spendAction()) {
			return false;
		}

		map.moveUnit(unit, destination);
		return true;
	}

	public void incrementGold(Player p) {
		p.gold += 50 * p.tilesOwned;
	}

	public void printInfo(String stmt) {
		logging.publish(new LogRecord(Level.INFO, stmt));
	}

	public void printFine(String stmt) {
		logging.publish(new LogRecord(Level.FINE, stmt));
	}

	public void printSevere(String stmt) {
		logging.publish(new LogRecord(Level.SEVERE, stmt));
	}
}
