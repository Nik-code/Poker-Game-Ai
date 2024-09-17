# backend.py

from cards.py import Deck
from hand_strength.py import evaluate_hand

class Player:
    def __init__(self, name, is_human=False):
        self.name = name
        self.hand = []
        self.is_human = is_human

    def receive_card(self, card):
        self.hand.append(card)

    def show_hand(self):
        return ', '.join(str(card) for card in self.hand)

class Game:
    def __init__(self, num_players=2):
        self.players = []
        self.deck = Deck()
        self.num_players = num_players

    def setup_players(self):
        # Add human player
        self.players.append(Player(name="You", is_human=True))
        # Add AI players
        for i in range(1, self.num_players):
            self.players.append(Player(name=f"AI Player {i}"))

    def deal_cards(self):
        for _ in range(5):  # Assuming 5-card draw poker
            for player in self.players:
                card = self.deck.deal()
                player.receive_card(card)

    def evaluate_players(self):
        results = []
        for player in self.players:
            strength = evaluate_hand(player.hand)
            results.append((player, strength))
        return results

    def determine_winner(self, results):
        results.sort(key=lambda x: x[1]['rank'], reverse=True)
        return results[0][0], results

    def play(self):
        self.setup_players()
        self.deal_cards()
        results = self.evaluate_players()
        winner, sorted_results = self.determine_winner(results)
        return winner, sorted_results
