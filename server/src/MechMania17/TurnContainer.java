package MechMania17;

import MechMania17.Mm17.*;

public class TurnContainer {
	public int turnCount;
	public GameState game_state = null;
	public Player player = null;
	public Command command = null;
	public boolean succeeded;
	TurnContainer(GameState game_state, int turnCount) {
		this.game_state = game_state;
		this.turnCount = turnCount;
	}
	TurnContainer(Player player, Command command, boolean succeeded, int turnCount) {
		this.player = player;
		this.command = command;
		this.succeeded = succeeded;
		this.turnCount = turnCount;
	}
}
