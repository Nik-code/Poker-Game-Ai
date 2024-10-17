# game.py

from deck import Deck
from player import Player
from hand_evaluator import HandEvaluator

class Game:
    """
    Controls the flow of the poker game.
    """

    def __init__(self):
        self.players = []
        self.deck = Deck()
        self.community_cards = []
        self.pot = 0
        self.small_blind = 10
        self.big_blind = 20
        self.current_bet = 0
        self.current_player_index = 0
        self.round_over = False  # Indicates if the round has ended

    def add_player(self, player):
        """
        Adds a player to the game.
        """
        self.players.append(player)

    def setup(self):
        """
        Prepares the game for a new round.
        """
        self.deck = Deck()
        self.deck.shuffle()
        self.community_cards = []
        self.round_over = False
        for player in self.players:
            player.reset_for_new_round()

        # Deal hole cards
        for player in self.players:
            player.hole_cards = self.deck.deal(2)

        # Collect blinds
        self.collect_blinds()

    def collect_blinds(self):
        """
        Collects blinds from players.
        """
        num_players = len(self.players)
        small_blind_player = self.players[self.current_player_index % num_players]
        big_blind_player = self.players[(self.current_player_index + 1) % num_players]

        small_blind_amount = min(self.small_blind, small_blind_player.balance)
        big_blind_amount = min(self.big_blind, big_blind_player.balance)

        small_blind_player.place_bet(small_blind_amount)
        big_blind_player.place_bet(big_blind_amount)
        self.pot += small_blind_amount + big_blind_amount
        self.current_bet = big_blind_player.current_bet
        print(f"{small_blind_player.name} posts small blind of {small_blind_amount}")
        print(f"{big_blind_player.name} posts big blind of {big_blind_amount}")

    def betting_round(self):
        """
        Conducts a betting round.
        """
        num_players = len(self.players)
        for p in self.players:
            p.current_bet = 0  # Reset current bets

        # Determine first player to act
        if len(self.community_cards) == 0:
            # Pre-flop, first player after big blind
            first_player_index = (self.current_player_index + 2) % num_players
        else:
            # Post-flop, first active player to the left of dealer
            first_player_index = (self.current_player_index + 1) % num_players

        # Initialize current bet for post-flop rounds
        if len(self.community_cards) != 0:
            self.current_bet = 0

        active_players = [p for p in self.players if p.is_active and not p.has_folded]
        players_needed_to_act = active_players.copy()

        index = first_player_index

        while players_needed_to_act:
            player = self.players[index % num_players]
            index += 1

            if player in players_needed_to_act and not player.is_all_in and player.current_bet < self.current_bet:
                self.player_action(player)

                # After action, check if only one player remains
                active_players = [p for p in self.players if p.is_active and not p.has_folded]
                if len(active_players) == 1:
                    winner = active_players[0]
                    print(f"\nAll other players have folded. {winner.name} wins the pot of {self.pot}!")
                    winner.balance += self.pot
                    self.pot = 0
                    self.round_over = True
                    return

                if player.current_bet > self.current_bet:
                    # Player raised
                    self.current_bet = player.current_bet
                    # Reset players_needed_to_act to all active players except the raiser
                    players_needed_to_act = [p for p in self.players if p.is_active and not p.has_folded and p != player and not p.is_all_in]
                    index = index % num_players  # Reset index to start from next player
                else:
                    # Player called or folded
                    players_needed_to_act.remove(player)
            else:
                # Player doesn't need to act
                if player in players_needed_to_act:
                    players_needed_to_act.remove(player)

    def player_action(self, player):
        """
        Handles a player's action.
        """
        if player.is_bot:
            self.bot_action(player)
        else:
            self.human_action(player)

    def human_action(self, player):
        """
        Prompts the human player for an action.
        """
        try:
            print(f"\n{player.name}'s turn.")
            print(f"Your cards: {', '.join(str(card) for card in player.hole_cards)}")
            print(f"Community cards: {', '.join(str(card) for card in self.community_cards)}")
            amount_to_call = self.current_bet - player.current_bet
            print(f"Current bet to call: {amount_to_call}")
            print(f"Pot: {self.pot}")
            print(f"Your balance: {player.balance}")
            action = input("Choose action (fold, check, call, raise, all-in): ").strip().lower()
            if action == 'fold':
                player.fold()
                print(f"{player.name} folds.")
            elif action == 'check':
                if amount_to_call == 0:
                    print(f"{player.name} checks.")
                else:
                    print("Cannot check, you need to call, raise, or fold.")
                    self.human_action(player)
            elif action == 'call':
                amount_to_call = min(amount_to_call, player.balance)
                amount_placed = player.place_bet(amount_to_call)
                self.pot += amount_placed
                print(f"{player.name} calls {amount_placed}.")
            elif action == 'raise':
                max_raise = player.balance - (self.current_bet - player.current_bet)
                if max_raise <= 0:
                    print("You don't have enough balance to raise. You can call or go all-in.")
                    self.human_action(player)
                else:
                    raise_amount = int(input(f"Enter raise amount (maximum {max_raise}): "))
                    if raise_amount > max_raise:
                        print("You cannot raise more than your available balance.")
                        self.human_action(player)
                    else:
                        total_bet = (self.current_bet - player.current_bet) + raise_amount
                        amount_placed = player.place_bet(total_bet)
                        self.pot += amount_placed
                        self.current_bet = player.current_bet
                        print(f"{player.name} raises by {raise_amount}.")
            elif action == 'all-in':
                amount_placed = player.place_bet(player.balance)
                self.pot += amount_placed
                if player.current_bet > self.current_bet:
                    self.current_bet = player.current_bet
                print(f"{player.name} goes all-in with {amount_placed}.")
            else:
                print("Invalid action.")
                self.human_action(player)
        except ValueError:
            print("Invalid input. Please enter a number for the raise amount.")
            self.human_action(player)
        except Exception as e:
            print(f"An error occurred: {e}")
            self.human_action(player)

    def bot_action(self, player):
        """
        Handles bot AI actions.
        """
        import random
        print(f"\n{player.name}'s turn (Bot).")
        amount_to_call = self.current_bet - player.current_bet
        decision = random.choice(['call', 'fold', 'raise', 'all-in'])
        if decision == 'fold':
            player.fold()
            print(f"{player.name} folds.")
        elif decision == 'call':
            amount_to_call = min(amount_to_call, player.balance)
            amount_placed = player.place_bet(amount_to_call)
            self.pot += amount_placed
            print(f"{player.name} calls {amount_placed}.")
        elif decision == 'raise':
            max_raise = player.balance - amount_to_call
            if max_raise <= 0:
                # Not enough balance to raise, call or all-in instead
                if player.balance <= amount_to_call:
                    # Go all-in
                    amount_placed = player.place_bet(player.balance)
                    self.pot += amount_placed
                    print(f"{player.name} goes all-in with {amount_placed}.")
                else:
                    amount_placed = player.place_bet(amount_to_call)
                    self.pot += amount_placed
                    print(f"{player.name} calls {amount_placed}.")
            else:
                raise_amount = random.randint(1, max_raise)
                total_bet = amount_to_call + raise_amount
                amount_placed = player.place_bet(total_bet)
                self.pot += amount_placed
                self.current_bet = player.current_bet
                print(f"{player.name} raises by {raise_amount}.")
        elif decision == 'all-in':
            amount_placed = player.place_bet(player.balance)
            self.pot += amount_placed
            if player.current_bet > self.current_bet:
                self.current_bet = player.current_bet
            print(f"{player.name} goes all-in with {amount_placed}.")

    def play_round(self):
        """
        Plays a full round including all betting phases.
        """
        # Pre-flop betting
        self.betting_round()
        if self.round_over:
            return

        # Flop
        self.community_cards.extend(self.deck.deal(3))
        print(f"\nFlop: {', '.join(str(card) for card in self.community_cards)}")
        self.betting_round()
        if self.round_over:
            return

        # Turn
        self.community_cards.extend(self.deck.deal(1))
        print(f"\nTurn: {self.community_cards[-1]}")
        self.betting_round()
        if self.round_over:
            return

        # River
        self.community_cards.extend(self.deck.deal(1))
        print(f"\nRiver: {self.community_cards[-1]}")
        self.betting_round()
        if self.round_over:
            return

        # Showdown
        self.showdown()

    def showdown(self):
        """
        Determines the winner at the showdown.
        """
        active_players = [p for p in self.players if not p.has_folded]
        hands = []
        for player in active_players:
            total_cards = player.hole_cards + self.community_cards
            rank_index, rank_cards = HandEvaluator.evaluate_hand(total_cards)
            hands.append((player, rank_index, rank_cards))
            print(f"{player.name} has {', '.join(str(card) for card in player.hole_cards)}")
        # Determine winner
        hands.sort(key=lambda x: (x[1], x[2]), reverse=True)
        winner = hands[0][0]
        print(f"\n{winner.name} wins the pot of {self.pot}!")
        winner.balance += self.pot
        self.pot = 0

    def play(self):
        """
        Starts the game loop.
        """
        while len([p for p in self.players if p.balance > 0]) > 1:
            self.setup()
            self.play_round()
            # Remove players with zero balance
            self.players = [p for p in self.players if p.balance > 0]
            self.current_player_index = (self.current_player_index + 1) % len(self.players)
            input("\nPress Enter to continue to the next round...")
