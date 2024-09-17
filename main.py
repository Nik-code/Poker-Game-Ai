from backend.py import Game
from ai_strategy.py import ai_decision
from hand_strength.py import evaluate_hand

def main():
    num_players = 4  # You can change the number of AI players
    game = Game(num_players=num_players)
    winner, results = game.play()

    # Show hands
    for player, evaluation in results:
        print(f"\n{player.name}'s hand: {player.show_hand()}")
        print(f"Hand Strength: {evaluation['hand_type']}")

    # Human player's turn to discard and draw new cards
    human_player = game.players[0]
    print(f"\nYour hand: {human_player.show_hand()}")
    discard_indices = input("Enter the card positions (1-5) you want to discard, separated by spaces: ")
    discard_indices = [int(idx)-1 for idx in discard_indices.strip().split()]
    for idx in sorted(discard_indices, reverse=True):
        del human_player.hand[idx]
        human_player.receive_card(game.deck.deal())

    # Re-evaluate hands
    results = game.evaluate_players()
    winner, sorted_results = game.determine_winner(results)

    # Show final hands
    for player, evaluation in sorted_results:
        print(f"\n{player.name}'s final hand: {player.show_hand()}")
        print(f"Final Hand Strength: {evaluation['hand_type']}")

    # Determine winner
    if winner.is_human:
        print("\nCongratulations! You win!")
    else:
        print(f"\n{winner.name} wins!")

if __name__ == "__main__":
    main()
