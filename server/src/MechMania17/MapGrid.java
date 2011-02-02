package MechMania17;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;

public class MapGrid {
	private Tile[][] tiles;
	public int size = 0; // initialize to nonsense
	private HashMap<Integer, Location> unitLocations;

	public MapGrid(String file) throws IOException {
		if (file == null) file = "default.map";
		BufferedReader in = new BufferedReader(new FileReader("maps/" + file));
		String line;
		List<char[]> lines = new ArrayList<char[]>();
		int width = 0;
		while ((line = in.readLine()) != null) {
			if (width == 0) {
				width = line.length();
			}
			assert width == line.length();

			lines.add(line.toCharArray());
		}
		in.close();

		assert lines.size() == width;

		tiles = new Tile[lines.size()][lines.size()];
		for (int y = 0; y < lines.size(); y++) {
			for (int x = 0; x < lines.size(); x++) {
				tiles[x][y] = new Tile(lines.get(y)[x]);
			}
		}
		unitLocations = new HashMap<Integer, Location>();

		size = tiles.length; // square maps, so only one length is needed
	}

	/**
	 * Adds a player to the map by picking a random starting position and
	 * putting them there
	 * @param player
	 */
	public void add(Player player) {
		for (int y = 0; y < tiles.length; y++) {
			for (int x = 0; x < tiles.length; x++) {
				if (tiles[x][y].isStart() && tiles[x][y].getOwner() == 0) {
					Soldier initialUnit = Soldier.builder(1, 0, 0, 1);
					addUnit(new Location(x, y), initialUnit);
					tiles[x][y].setOwner(player.id);
					return;
				}
			}
		}
		throw new RuntimeException("Could not find starting position for player "
				+ player.id);
	}

	public boolean isValid(Location loc) {
		if (!Location.isValid(loc)) return false;

		return isValid(loc.getX(), loc.getY());
	}

	public boolean isValid(int x, int y) {
		if (x < 0 || y < 0) return false;

		if (x >= size || y >= size) return false;

		return true;
	}

	public Tile getTileUnsafe(Location loc) {
		return tiles[loc.getX()][loc.getY()];
	}

	public Tile getTile(Location loc) {
		if (!isValid(loc)) return null;

		return tiles[loc.getX()][loc.getY()];
	}

	public Tile getTile(int x, int y) {
		if (!isValid(x, y)) return null;

		return tiles[x][y];
	}

	/**
	 * Method to add a unit to a tile and update the indexes.
	 * @param location
	 * @param unit
	 */
	public void addUnit(Location location, Soldier unit) {
		Tile tile = getTile(location);
		tile.units.put(unit.id, unit);
		unitLocations.put(unit.id, location);
	}

	public Location setUnitLocation(int id, Location loc) {
		return unitLocations.put(id, loc);
	}

	public Location getUnitLocation(int id) {
		return unitLocations.get(id);
	}

	public boolean isTilePassable(Location destination) {
		if (!isValid(destination)) return false;

		Tile tile = tiles[destination.getX()][destination.getY()];
		return tile.getTerrainType() == Tile.Terrain.LAND;
	}

	public boolean isTileWater(Location destination) {
		if (!isValid(destination)) return false;

		Tile tile = tiles[destination.getX()][destination.getY()];
		return tile.getTerrainType() == Tile.Terrain.WATER;
	}

	public void moveUnit(Soldier unit, Location destination) {
		Location sourceLocation = getUnitLocation(unit.id);
		Tile sourceTile = getTile(sourceLocation);

		Tile destinationTile = getTile(destination);

		// might want to move this verification code up a level
		int sourceOwner = sourceTile.getUnitOwner(unit);
		int destOwner = destinationTile.getOwner();
		if (destinationTile.getOwner() != 0 && sourceOwner != destOwner) {
			return;
		}

		sourceTile.removeUnit(unit);

		if (sourceTile.units.size() == 0) {
			sourceTile.setOwner(0);
		}

		destinationTile.units.put(unit.id, unit);
		unitLocations.put(unit.id, destination);
		destinationTile.setOwner(sourceOwner);
	}

	public void removeUnit(Soldier target) {
		Location location = unitLocations.get(target.id);
		Tile tile = getTile(location);
		tile.units.remove(target.id);
		unitLocations.remove(target.id);

		if (tile.units.size() == 0) {
			tile.setOwner(0);
		}
	}

	public int tilesOwnedByPlayer(int player_id)
	{
		int owned = 0;
		for (Tile[] rows : tiles) {
			for (Tile column : rows) {
				if (column.getOwner() == player_id) {
					owned++;
				}
			}
		}
		return owned;
	}

}
