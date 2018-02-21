# -*- coding: utf-8 -*-
"""
Copyright François Durand
fradurand@gmail.com

This file is part of Hanabython.

    Hanabython is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    Hanabython is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with Hanabython.  If not, see <http://www.gnu.org/licenses/>.
"""
from typing import List
from hanabython.Modules.Clue import Clue
from hanabython.Modules.Card import Card
from hanabython.Modules.StringUtils import uncolor, title
from hanabython.Modules.Configuration import Configuration
from hanabython.Modules.ConfigurationEndRule import ConfigurationEndRule
from hanabython.Modules.Board import Board
from hanabython.Modules.DiscardPile import DiscardPile
from hanabython.Modules.DrawPilePublic import DrawPilePublic
from hanabython.Modules.DrawPile import DrawPile
from hanabython.Modules.Hand import Hand
from hanabython.Modules.HandPublic import HandPublic
from hanabython.Modules.StringAnsi import StringAnsi
from hanabython.Modules.Player import Player


class PlayerBase(Player):
    """
    A player for Hanabi with basic features.

    This class is meant to serve as a mother class for most AIs and interface
    for human players. It provides all basic features, such as keeping
    track of the number of cards in the draw pile, the cards in the other
    players' hands, the clues given, etc.

    Note that all the variables are "personal" to this player: the Game does
    not share access to its internal variables with the players.

    :param str name: the name of the player.

    :var list player_names: a list of string, each with a player's name. By
        convention, the list is always rotated to that this player has
        position 0, the next player has position 1, etc.
    :var int n_players: the number of players.
    :var Configuration cfg: the configuration of the game.
    :var Board board: the board.
    :var DrawPilePublic draw_pile: the draw pile.
    :var DiscardPile discard_pile: the discard pile.
    :var int n_clues: the number of clues left.
    :var int n_misfires: the number of misfires (initially 0).
    :var int hand_size: the initial hand size.
    :var list hands: a list of Hand objects. The hand in position 0,
        corresponding to this player, is never updated because the player does
        not know what she has.
    :var list hands_public: a list of HandPublic objects. This allow the player
        to keep track, not only of her own clues, but also of the clues given
        to her partners.
    :var int remaining_turns: the number of remaining turns (once the draw pile
        is empty, in the normal rule for end of game). While the draw pile
        still contains cards, this variable is `None`.
    :var bool dealing_is_ongoing: True only during the initial dealing of
        hands. Avoid useless verbose messages in the recent events.
    :var str recent_events: things that happened "recently" (typically, since
        this player's last turn).
    :var int display_width: the width of the display on the terminal (in number
        of characters).

    >>> antoine = PlayerBase(name='Antoine')
    >>> print(antoine)
    Antoine
    """
    def __init__(self, name: str):
        super().__init__(name)
        self.player_names = None        # type: List[str]
        self.n_players = None           # type: int
        self.cfg = None                 # type: Configuration
        self.board = None               # type: Board
        self.draw_pile = None           # type: DrawPilePublic
        self.discard_pile = None        # type: DiscardPile
        self.n_clues = None             # type: int
        self.n_misfires = None          # type: int
        self.hand_size = None           # type: int
        self.hands = None               # type: List[Hand]
        self.hands_public = None        # type: List[HandPublic]
        self.remaining_turns = None     # type: int
        self.dealing_is_ongoing = None  # type: bool
        self.recent_events = None       # type: str
        self.display_width = None       # type: int

    def __repr__(self) -> str:
        s = '<PlayerBase\n'
        for attr in self.__dict__:
            left = (60 - len(attr)) // 2
            right = 60 - len(attr) - left
            s += '*' * left + ' ' + attr + ' ' + '*' * right + '\n' + str(
                self.__getattribute__(attr)) + '\n'
        s += 'End PlayerBase>'
        return s

    def colored(self) -> str:
        if self.cfg is None:
            return super().colored()
        # noinspection PyListCreation
        lines = []
        lines.append(title('Recent Events', self.display_width))
        lines.append(self.recent_events)
        self.recent_events = ''
        lines.append(title('Hands', self.display_width))
        lines.append(self.colored_hands())
        lines.append(title('Board', self.display_width))
        lines.append(self.board.colored_multi_line_compact())
        lines.append(title('Discard Pile', self.display_width))
        lines.append(self.discard_pile.colored())
        lines.append(title('Status', self.display_width))
        draw_line = 'Draw pile: %s.' % self.draw_pile.colored()
        if (self.cfg.end_rule == ConfigurationEndRule.NORMAL
                and self.remaining_turns is not None):
            draw_line += ' %s turns remaining!' % self.remaining_turns
        lines.append(draw_line)
        lines.append(
            (StringAnsi.BLUE + '%s' + StringAnsi.RESET
             + ' clues left (out of %s). '
             + StringAnsi.RED + '%s' + StringAnsi.RESET
             + ' misfires (out of %s).')
            % (self.n_clues, self.cfg.n_clues,
               self.n_misfires, self.cfg.n_misfires)
        )
        return '\n'.join(lines)

    def colored_hands(self) -> str:
        """
        A string used to display the hands of all players.

        :return: the string (whose width is usually `display_width`).

        >>> antoine = PlayerBase('Antoine')
        >>> antoine.demo_game()
        >>> from hanabython import uncolor
        >>> print(uncolor(antoine.colored_hands()))
        Antoine
        [BGRWY 12345, BGRWY  2345, BGRWY 1    , BGRWY 1    , BGRWY  2345]
        <BLANKLINE>
        Donald
        [    Y2     ,     R1     ,     R3     ,     G3     ,     Y4     ]
        [BGRWY  2345, BGRWY 1    , BGRWY  2345, BGRWY  2345, BGRWY  2345]
        <BLANKLINE>
        Uwe
        [    G4     ,     B4     ,     W4     ,     G5     ,     W1     ]
        [BGRWY 12345, BGRWY 12345, BGRWY 12345, BGRWY 12345, BGRWY 12345]
        """
        # noinspection PyListCreation
        lines = []
        lines.append(self.name)
        lines.append(self.hands_public[0].colored())
        for i, name in enumerate(self.player_names):
            if i == 0:
                continue
            lines.append('')
            lines.append(name)
            lines.append('[' + ', '.join([
                self._large_card_color(card) for card in self.hands[i]
            ]) + ']')
            lines.append(self.hands_public[i].colored())
        return '\n'.join(lines)

    # noinspection PyProtectedMember
    def _large_card(self, card: Card) -> str:
        """
        A string representing a Card, with the same width as a CardPublic.

        This works only once :attr:`cfg` is initialized, which is done via
        :meth:`receive_init`. Indeed, the configuration is needed to known
        the width.

        :param card: the card.

        :return: the large string.

        >>> from hanabython import Card
        >>> antoine = PlayerBase('Antoine')
        >>> antoine.receive_init(cfg=Configuration.STANDARD,
        ...                      player_names=['Antoine', 'Donald'])
        >>> print('The card:%s.' % antoine._large_card(Card('B5')))
        The card:    B5     .
        """
        return uncolor(self._large_card_color(card))

    # noinspection PyProtectedMember
    def _large_card_color(self, card: Card) -> str:
        """
        Colored version of :meth:`_large_card`

        :return: the same string as :meth:`_large_card`, but with ANSI escape
            codes to add colors where relevant.
        """
        width = self.cfg.n_colors + self.cfg.n_values + 1
        s = str(card)
        left = (width - len(s)) // 2
        right = width - len(s) - left
        return ' ' * left + card.colored() + ' ' * right

    def log(self, o: object) -> None:
        """
        Log events.

        :param o: an object. The method adds `str(o)` to the variable
            :attr:`recent_events`, except during the initial dealing of cards
            (to avoid useless messages about each card). When using strings, do
            not forget the end-of-line character (it is not added
            automatically).

        >>> antoine = PlayerBase('Antoine')
        >>> antoine.log_init()
        >>> antoine.log('Something happens.\\n')
        >>> antoine.dealing_is_ongoing = True
        >>> antoine.log('Many useless messages.\\n')
        >>> antoine.dealing_is_ongoing = False
        >>> antoine.log('Something else happens.\\n')
        >>> print(antoine.recent_events)
        Something happens.
        Something else happens.
        <BLANKLINE>
        """
        if not self.dealing_is_ongoing:
            self.recent_events += str(o)

    def log_init(self) -> None:
        """
        Initialize the log process (at the beginning of a game).

        Empties :attr:`recent_events`.
        """
        self.recent_events = ''

    def log_forget(self) -> None:
        """
        Forget old events (during the game).

        Empties :attr:`recent_events`. In this base class, this method has the
        same implementation as :meth:`log_init`, but it could be different
        in some subclasses.
        """
        self.recent_events = ''

    def receive_init(self, cfg: Configuration, player_names: List[str]) -> None:
        """
        Receive a message: the game starts.

        Initialize all the instance variables.

        :param cfg: the configuration of the game.
        :param player_names: the names of the players, rotated so that this
            player corresponds to index 0.
        """
        self.player_names = player_names
        self.n_players = len(player_names)
        self.cfg = cfg
        self.board = Board(cfg)
        self.draw_pile = DrawPilePublic(cfg)
        self.discard_pile = DiscardPile(cfg)
        self.n_clues = cfg.n_clues
        self.n_misfires = 0
        self.hand_size = cfg.hand_size_rule.f(self.n_players)
        self.hands = [Hand() for _ in player_names]
        self.hands_public = [HandPublic(cfg) for _ in player_names]
        self.dealing_is_ongoing = False
        self.display_width = (
            self.cfg.n_colors + 3 + self.cfg.n_values) * self.hand_size
        self.log_init()
        self.log('Configuration\n')
        self.log('-------------\n')
        self.log(self.cfg.colored())
        self.log('\n')

    def receive_begin_dealing(self) -> None:
        """
        Receive a message: the initial dealing of hands begins.

        The log is turned off to avoid having a message for each card dealt.
        """
        self.dealing_is_ongoing = True

    def receive_end_dealing(self) -> None:
        """
        Receive a message: the initial dealing of hands is over.

        The hands themselves are not communicated in this message. Drawing
        cards, including for the initial hands, is always handled by
        :meth:`receive_i_draw` and :meth:`receive_partner_draws`.

        The log is turned back on.
        """
        self.dealing_is_ongoing = False
        # self.log('\nInitial hands' + '\n')
        # self.log('-------------' + '\n')
        # self.log(self.colored_hands() + '\n')
        self.log('\nFirst moves' + '\n')
        self.log('-----------' + '\n')
        self.log('The game begins.\n')

    def receive_remaining_turns(self, remaining_turns: int) -> None:
        """
        Receive a message: the number of remaining turns is now known.

        This happens with the normal rule for end of game: as soon as the
        discard pile is empty, we know how many turns are left. "Turn" means
        that one player gets to play (not all of them).

        :param remaining_turns: the number of turns left.
        """
        self.remaining_turns = remaining_turns
        self.log('%s turns remaining!\n' % self.remaining_turns)

    def receive_i_draw(self) -> None:
        """
        Receive a message: this player tries to draw a card.

        A card is actually drawn only if the draw pile is not empty.
        """
        if self.draw_pile.n_cards == 0:
            return
        self.draw_pile.give()
        self.hands_public[0].receive()
        self.log('%s draws a card.\n' % self.name)

    def receive_partner_draws(self, i_drawer: int, card: Card) -> None:
        """
        Receive a message: another player tries to draw a card.

        A card is actually drawn only if the draw pile is not empty.

        :param i_drawer: the position of the player who draws (relatively
            to this player).
        :param card: the card drawn.
        """
        if card is None:
            return
        self.draw_pile.give()
        self.hands[i_drawer].receive(card)
        self.hands_public[i_drawer].receive()
        self.log('%s draws %s.\n' % (
            self.player_names[i_drawer], card.colored()))

    def receive_someone_throws(
        self, i_thrower: int, k: int, card: Card
    ) -> None:
        """
        Receive a message: a player willingly discards a card.

        It is not necessary to check whether this action is legal: the Game
        will only send this message when it is the case.

        :param i_thrower: the position of the player who throws (relatively
            to this player).
        :param k: position of the card in the hand.
        :param card: the card thrown.
        """
        self.hands_public[i_thrower].give(k)
        if i_thrower != 0:
            self.hands[i_thrower].give(k)
        self.discard_pile.receive(card)
        self.n_clues += 1
        self.log('%s discards %s.\n' % (
            self.player_names[i_thrower], card.colored()))

    def receive_someone_plays(self, i_player: int, k: int, card: Card) -> None:
        """
        Receive a message: a player tries to play a card on the board.

        This can be a success or a misfire.

        :param i_player: the position of the player who plays the card
            (relatively to this player).
        :param k: position of the card in the hand.
        :param card: the card played.
        """
        self.hands_public[i_player].give(k)
        if i_player != 0:
            self.hands[i_player].give(k)
        success = self.board.try_to_play(card)
        if success:
            self.log('%s plays %s' % (
                self.player_names[i_player], card.colored()))
            if (card.v == self.cfg.highest[self.cfg.i_from_c(card.c)]
                    and self.n_clues < self.cfg.n_clues):
                self.n_clues += 1
                self.log(' and regains a clue.\n')
            else:
                self.log('.\n')
        else:
            self.discard_pile.receive(card)
            self.n_misfires += 1
            self.log('%s tries to play %s and misfires.\n' % (
                self.player_names[i_player], card.colored()))

    def receive_someone_clues(
        self, i_cluer: int, i_clued: int, clue: Clue, bool_list: List[bool]
    ) -> None:
        """
        Receive a message: a player gives a clue to another.

        It is not necessary to check whether this action is legal: the Game
        will only send this message when it is the case.

        :param i_cluer: the position of the player who gives the clue
            (relatively to this player).
        :param i_clued: the position of the player who receives the clue
            (relatively to this player).
        :param clue: the clue (value or color).
        :param bool_list: a list of boolean that indicates what cards
            match the clue given.
        """
        self.n_clues -= 1
        self.hands_public[i_clued].match(clue, bool_list)
        if type(clue) == int:
            clue_str = str(clue)
        else:
            # noinspection PyUnresolvedReferences
            clue_str = clue.colored()
        self.log('%s clues %s about %s.\n' % (
            self.player_names[i_cluer], self.player_names[i_clued], clue_str))

    def receive_someone_forfeits(self, i_forfeiter: int) -> None:
        """
        Receive a message: a player forfeits.

        :param i_forfeiter: the position of the player who forfeits
            (relatively to this player).
        """
        self.log('%s forfeits.\n' % self.player_names[i_forfeiter])

    def receive_action_legal(self) -> None:
        """
        Receive a message: the action chosen is legal.

        We forget the previous events.
        """
        self.log_forget()

    def receive_action_finished(self) -> None:
        """
        Receive a message: the action of the player is finished.
        """
        self.log_forget()

    def receive_lose(self, score: int) -> None:
        """
        Receive a message: the game is lost (misfires or forfeit).
        """
        self.log("%s's team loses.\n" % self.name)
        self.log('Score: %s.\n' % score)

    def receive_game_over(self, score: int) -> None:
        """
        Receive a message: the game is over and is neither really lost
        (misfires, forfeit) nor a total victory (maximal score).
        """
        self.log("%s's team has reached the end of the game.\n" % self.name)
        self.log('Score: %s.\n' % score)

    def receive_win(self, score: int) -> None:
        """
        Receive a message: the game is won (total victory).
        """
        self.log("%s's team wins!\n" % self.name)
        self.log('Score: %s.\n' % score)

    def demo_game(self) -> None:
        import random
        random.seed(0)
        cfg = Configuration.STANDARD
        draw_pile = DrawPile(cfg)
        self.receive_init(cfg=cfg, player_names=[self.name, 'Donald', 'Uwe'])
        self.receive_begin_dealing()
        my_hand = Hand()
        for k in range(self.hand_size):
            my_hand.receive(card=draw_pile.give())
            self.receive_i_draw()
            for i in range(1, self.n_players):
                self.receive_partner_draws(i_drawer=i, card=draw_pile.give())
        self.receive_end_dealing()
        self.receive_someone_clues(
            i_cluer=0, i_clued=1, clue=Clue(1),
            bool_list=self.hands[1].match(Clue(1)))
        self.receive_someone_clues(
            i_cluer=1, i_clued=0, clue=Clue(1),
            bool_list=my_hand.match(Clue(1)))
        self.receive_someone_throws(i_thrower=2, k=4, card=self.hands[2][4])
        self.receive_partner_draws(i_drawer=2, card=draw_pile.give())
        self.receive_someone_plays(i_player=0, k=1, card=my_hand[1])
        my_hand.receive(card=draw_pile.give())
        self.receive_i_draw()
        # print(my_hand.colored())


if __name__ == '__main__':
    # alice = PlayerBase(name='Alice')
    # alice.receive_init(cfg=Configuration.STANDARD,
    #                    player_names=['Alice', 'Bob', 'Cat'])
    my_antoine = PlayerBase(name='Antoine')
    my_antoine.demo_game()
    print(my_antoine.colored())

    # alice.receive_i_draw()
    # alice.receive_i_draw()
    # alice.receive_i_draw()
    # alice.receive_i_draw()
    # alice.receive_i_draw()
    # alice.receive_partner_draws(i_drawer=1, card=Card('B1'))
    # alice.receive_partner_draws(i_drawer=1, card=Card('B2'))
    # alice.receive_partner_draws(i_drawer=1, card=Card('B3'))
    # alice.receive_partner_draws(i_drawer=1, card=Card('B4'))
    # alice.receive_partner_draws(i_drawer=1, card=Card('B5'))
    # alice.receive_someone_clues(
    #     i_cluer=0, i_clued=1, clue=1,
    #     bool_list=[False, False, False, False, True])
    # alice.receive_someone_throws(i_thrower=1, k=2, card=Card('B5'))
    # alice.receive_someone_throws(i_thrower=0, k=2, card=Card('Y2'))
    # alice.receive_i_draw()
    # alice.receive_someone_plays(i_player=1, k=3, card=Card('B1'))
    # alice.receive_someone_plays(i_player=1, k=2, card=Card('B2'))
    # alice.receive_someone_plays(i_player=0, k=0, card=Card('Y1'))
    # alice.receive_remaining_turns(3)
    # # print(alice)
    # print(alice.colored())
    #
    import doctest
    doctest.testmod()
