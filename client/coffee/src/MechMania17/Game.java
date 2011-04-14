package MechMania17;

import java.io.BufferedInputStream;
import java.io.IOException;
import java.net.Socket;
import java.net.InetSocketAddress;
import java.net.UnknownHostException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import MechMania17.Mm17.Actions;
import MechMania17.Mm17.ClientConnect;
import MechMania17.Mm17.GameState;
import MechMania17.Mm17.InitialResources;
import MechMania17.Mm17.CommandType;
import MechMania17.Mm17.Command;
import MechMania17.Mm17.Command.AttachSubCommand;
import MechMania17.Mm17.Command.AttackCommand;
import MechMania17.Mm17.Command.Direction;
import MechMania17.Mm17.Command.LoadSubCommand;
import MechMania17.Mm17.Command.MoveCommand;
import MechMania17.Mm17.Command.MoveSubCommand;
import MechMania17.Mm17.Command.SummonCommand;
import MechMania17.Mm17.Command.SummonSubCommand;

import com.google.protobuf.InvalidProtocolBufferException;

public class Game {
	private Socket socket;
	private int playerId = 0;
	private int gold = 0;
	private int turnCount = 0;
	private int mapSize = 0;
	private Actions.Builder actions = null;
	private Terrain[][] terrain;
	public Map<Location, Tile> visibleTiles;
	public List<Tile> myTiles;
	public List<Tile> unownedTiles;
	public List<Tile> theirTiles;
	public List<Unit> myUnits;
	public List<Unit> theirUnits;
	public List<Submarine> mySubmarines;
	private BufferedInputStream bis;

	public enum Terrain {
		PLAIN, OCEAN, MOUNTAIN
	}

	/**
	 * Constructor for Game object -- Interface between client and server,
	 * queryable for parameters of the game state
	 * 
	 * @param name Name of your team
	 * @param host Host of the server
	 * @param port Port of the server
	 * @throws UnknownHostException 
	 * @throws IOException
	 */
	public Game(String name, String host, int port) throws UnknownHostException, IOException {
		socket = new Socket();
		socket.connect(new InetSocketAddress(host, port));
		bis = new BufferedInputStream(socket.getInputStream());

		ClientConnect.Builder hello = ClientConnect.newBuilder();
		hello.setName(name);
		hello.build().writeDelimitedTo(socket.getOutputStream());

		InitialResources initial = InitialResources.parseDelimitedFrom(bis);
		playerId = initial.getId();
		readTerrain(initial.getMapWidth(), initial.getTilesList());

		readGamestate();
	}

	private void readTerrain(int mapSize, List<InitialResources.Tile> tilesList) {
		this.mapSize = mapSize;
		terrain = new Terrain[mapSize][mapSize];
		for (InitialResources.Tile t : tilesList) {
			int x = t.getX();
			int y = t.getY();

			Terrain value;
			switch (t.getType()) {
			case OCEAN:
				value = Terrain.OCEAN;
				break;
			case MOUNTAIN:
				value = Terrain.MOUNTAIN;
				break;
			case PLAIN:
			default:
				value = Terrain.PLAIN;
				break;
			}

			terrain[x][y] = value;
		}
	}

	private boolean readGamestate() throws InvalidProtocolBufferException, IOException {
		GameState gs = GameState.parseDelimitedFrom(bis);
		if (gs == null) {
			return false;
		}
		gold = gs.getGold();

		visibleTiles = new HashMap<Location, Tile>();
		myTiles = new ArrayList<Tile>();
		unownedTiles = new ArrayList<Tile>();
		theirTiles = new ArrayList<Tile>();

		myUnits = new ArrayList<Unit>();
		theirUnits = new ArrayList<Unit>();

		for (GameState.Tile t : gs.getTilesList()) {
			int x = t.getX();
			int y = t.getY();
			Tile tile = new Tile(t.getOwner(), x, y, terrain[x][y]);

			visibleTiles.put(new Location(x, y), tile);
			if (tile.getOwner() == getPlayerId()) {
				myTiles.add(tile);
				for (GameState.Unit u : t.getUnitsList()) {
					Unit unit = new Unit(u, new Location(x, y));
					tile.unitsOnTile.add(unit);
					myUnits.add(unit);
				}
			} else if (tile.getOwner() == 0) {
				unownedTiles.add(tile);
			} else {
				theirTiles.add(tile);
				for (GameState.Unit u : t.getUnitsList()) {
					Unit unit = new Unit(u, new Location(x, y));
					tile.unitsOnTile.add(unit);
					theirUnits.add(unit);
				}
			}
		}

		mySubmarines = new ArrayList<Submarine>();
		for (GameState.Submarine s : gs.getSubmarinesList()) {
			int x = s.getX();
			int y = s.getY();
			List<Unit> subUnits = new ArrayList<Unit>();
			for (GameState.Unit u : s.getUnitsList()) {
				subUnits.add(new Unit(u, new Location(x, y)));
			}
			
			mySubmarines.add(new Submarine(s, subUnits));
			myUnits.addAll(subUnits);
		}

		actions = Actions.newBuilder();
		return true;
	}

	public int getPlayerId() {
		return playerId;
	}

	public int getGold() {
		return gold;
	}

	public int getTurnCount() {
		return turnCount;
	}

	public int getMapSize() {
		return mapSize;
	}

	public int getUnitCost(int hp, int damage, int range, int vision) {
		return Cost.calculateSoldierCost(hp, damage, range, vision);
	}

	public int getSubCost() {
		return Cost.calculateSubmarineCost();
	}

	public Terrain getTerrain(Location loc) {
		return terrain[loc.getX()][loc.getY()];
	}

	public Direction North() {
		return Direction.NORTH;
	}

	public Direction East() {
		return Direction.EAST;
	}

	public Direction West() {
		return Direction.WEST;
	}

	public Direction South() {
		return Direction.SOUTH;
	}

	/**
	 * Builds a unit.
	 * @param hp Must be >=1
	 * @param damage Must be non-negative
	 * @param range Must be non-negative
	 * @param vision Must be non-negative
	 * @param loc (x,y) coordinates to spawn
	 */
	public void summon(int hp, int damage, int range, int vision, Location loc) {
		// TODO: asserts for the values

		SummonCommand.Builder summon = SummonCommand.newBuilder();
		summon.setHp(hp);
		summon.setDamage(damage);
		summon.setRange(range);
		summon.setVision(vision);
		summon.setX(loc.getX());
		summon.setY(loc.getY());

		Command.Builder command = Command.newBuilder();
		command.setSummon(summon);
		command.setType(CommandType.SUMMON);
		actions.addActions(command);
	}

	/**
	 * Moves a unit in a certain direction
	 * @param unit Unit to move
	 * @param dir Direction to move
	 */
	public void move(Unit unit, Direction dir) {
		MoveCommand.Builder move = MoveCommand.newBuilder();
		move.setDirection(dir);
		move.setId(unit.getId());

		Command.Builder command = Command.newBuilder();
		command.setMove(move);
		command.setType(CommandType.MOVE);
		actions.addActions(command);
	}

	/**
	 * Attack another unit
	 * @param source Unit to attack with
	 * @param target Unit to attack
	 */
	public void attack(Unit source, Unit target) {
		AttackCommand.Builder attack = AttackCommand.newBuilder();
		attack.setSource(source.getId());
		attack.setTarget(target.getId());

		Command.Builder command = Command.newBuilder();
		command.setAttack(attack);
		command.setType(CommandType.ATTACK);
		actions.addActions(command);
	}

	/**
	 * Summon a sub at a given location
	 * @param loc Location
	 */
	public void summonSub(Location loc) {
		SummonSubCommand.Builder sub = SummonSubCommand.newBuilder();
		sub.setX(loc.getX());
		sub.setY(loc.getY());

		Command.Builder command = Command.newBuilder();
		command.setSummonSub(sub);
		command.setType(CommandType.SUMMONSUB);
		actions.addActions(command);
	}

	/**
	 * Load a unit onto a submarine
	 * @param sub Submarine you want to load a unit onto
	 * @param unit Unit to load
	 */
	public void loadSub(Submarine sub, Unit unit) {
		LoadSubCommand.Builder load = LoadSubCommand.newBuilder();
		load.setSubmarine(sub.getId());
		load.setUnit(unit.getId());

		Command.Builder command = Command.newBuilder();
		command.setLoadSub(load);
		command.setType(CommandType.LOADSUB);
		actions.addActions(command);
	}

	/**
	 * Move a submarine to another water tile
	 * Fails if you try to move to a non-water tile
	 * @param sub Submarine to move
	 * @param loc Location to move to
	 */
	public void moveSub(Submarine sub, Location loc) {
		MoveSubCommand.Builder ms = MoveSubCommand.newBuilder();
		ms.setX(loc.getX());
		ms.setY(loc.getY());
		ms.setSubmarine(sub.getId());

		Command.Builder command = Command.newBuilder();
		command.setMoveSub(ms);
		command.setType(CommandType.MOVESUB);
		actions.addActions(command);
	}

	/**
	 * Attaches a sub to the land, causes all units in the sub to be at the location of the sub
	 * The sub is unusable afterwards
	 * @param sub Submarine to attach
	 */
	public void attachSub(Submarine sub) {
		AttachSubCommand.Builder as = AttachSubCommand.newBuilder();
		as.setSubmarine(sub.getId());

		Command.Builder command = Command.newBuilder();
		command.setAttachSub(as);
		command.setType(CommandType.ATTACHSUB);
		actions.addActions(command);
	}

	/**
	 * Send actions to the server
	 * @return 
	 * @throws InvalidProtocolBufferException
	 * @throws IOException
	 */
	public boolean sendActions() throws InvalidProtocolBufferException, IOException {
		actions.build().writeDelimitedTo(socket.getOutputStream());

		turnCount++;
		return readGamestate();
	}
}
