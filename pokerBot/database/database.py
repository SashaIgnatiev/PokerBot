import sqlite3

#Method will increment win or lose by one when called
"""
Tracking the overall performance of the bot against all players it faces.
Method should be called at the beginning, and the end of a session.
"""
pokerBot_name = 'PokerBot_MK1'
def performance_stat_tracker(player, mychips, playerchips, start = True, game_id = None, hands_played = None):
    global pokerBot_name
    con = sqlite3.connect('Poker_Stats')
    cur = con.cursor()
    if start == True:
        cur.execute('INSERT INTO Performance (poker_bot_version, player_id, chips_before, player_chips_before) VALUES (?, ?, ?, ?)', (pokerBot_name, player, mychips, playerchips))
        x = cur.execute('SELECT max(game_id) FROM Performance')
        for i in x:
            game_id = i[0]
            break
        print(f'Game id: {game_id}')
        """
        When the method is initially called it will return the game id of the current game. 
        Store the game id in a variable and call the function again with the game id to call 
        the correct column and store the results of the game.
        """
        con.commit()
        cur.close()
        return game_id
    else:
        if hands_played == None:
            raise Exception('Hands Played can not be None')
        if game_id == None:
            raise Exception('Game_id can not be None')

        cur.execute('UPDATE Performance SET chips_after = ?, player_chips_after = ?, hands_played = ? WHERE game_id = ?', (mychips, playerchips, hands_played, game_id))


    con.commit()
    cur.close()



def game_stat_tracker(self, game_id, hand_id, bot_cards, chips_before, chips_after):
    con = sqlite3.connect('Poker_stats')
    cur = con.cursor()
    cur.execute('SELECT game_id FROM Performance')
def remove_elements(table):
    con = sqlite3.connect('Poker_Stats')
    cur = con.cursor()
    cur.execute('DELETE FROM "{table}" ;'.format(table = table))

    con.commit()
    cur.close()








if __name__ == "__main__":
    remove_elements('Performance')