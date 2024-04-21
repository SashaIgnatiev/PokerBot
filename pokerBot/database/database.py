import sqlite3

#Method will increment win or lose by one when called
"""
Tracking the overall performance of the bot against all players it faces.
Method should be called at the beginning, and the end of a session.
"""
pokerBot_name = 'PokerBot_MK1'
def performance_stat_tracker(player, mychips, playerchips, start = True, game_id = None, hands_played = None):
    global pokerBot_name
    con = sqlite3.connect('../Poker_Stats')
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

        return game_id
    else:
        if hands_played == None:
            raise Exception('Hands Played can not be None')
        if game_id == None:
            raise Exception('Game_id can not be None')

        cur.execute('UPDATE Performance SET chips_after = ?, player_chips_after = ?, hands_player = ? WHERE game_id = ?', (mychips, playerchips, hands_played, game_id))


    cur.execute()
    con.commit()
    cur.close()

def game_stat_tracker(player_name, state):
    con = sqlite3.connect('Poker_Stats')
    cur = con.cursor()

    try:
        #sql = 'SELECT player_name FROM Player_Games WHERE player_name = {player_name};'.format(player_name=player_name)
        cur.execute('SELECT player_name FROM Player_Games WHERE player_name = ?;', (player_name, ))
    except:
        #sql = 'INSERT INTO Player_Games VALUES (?, 0, 0, 0, 0);'
        cur.execute('INSERT INTO Player_Games VALUES (?, 0, 0, 0, 0);', (player_name, ))
        

    if state == 'WIN':
        sql = 'SELECT hands_won FROM Player_Games WHERE player_name = {player_name};'.format(player_name = player_name)
        win_int = cur.execute(sql)
        for i in win_int:
            win_counter = int(i[0])
            win_counter += 1
            break
        #sql = 'UPDATE Player_Games SET hands_won = {win_counter} WHERE player_name = {player_name};'.format(win_counter = win_counter, player_name = player_name)
        cur.execute('UPDATE Player_Games SET hands_won = ? WHERE player_name = ?;', (win_counter, player_name, ))

    if state == 'LOSE':
        #sql = 'SELECT hands_lost FROM Player_Games WHERE player_name = ?;'
        lose_int = cur.execute('SELECT hands_lost FROM Player_Games WHERE player_name = ?;', (player_name, ))
        lose_counter = 0
        for i in lose_int:
            lose_counter = int(i[0])
            lose_counter += 1
            break
        #sql = 'UPDATE Player_Games SET hands_lost = {lose_counter} WHERE player_name = {player_name};'.format(lose_counter=lose_counter, player_name=player_name)
        cur.execute('UPDATE Player_Games SET hands_lost = ? WHERE player_name = ?;', (lose_counter, player_name, ))

    if state == 'TIE':
        #sql = 'SELECT hands_tied FROM Player_Games WHERE player_name = {player_name};'.format(player_name=player_name)
        tie_int = cur.execute('SELECT hands_tied FROM Player_Games WHERE player_name = ?;', (player_name, ))
        for i in tie_int:
            tie_counter = int(i[0])
            tie_counter += 1
            break
        #sql = 'UPDATE Player_Games SET hands_tied = {tie_counter} WHERE player_name = {player_name};'.format(tie_counter = tie_counter, player_name=player_name)
        cur.execute('UPDATE Player_Games SET hands_tied = ? WHERE player_name = ?;', (tie_counter, player_name))

    #sql = 'SELECT hands_played FROM Player_Games WHERE player_name = {player_name};'.format(player_name=player_name)
    counter = cur.execute('SELECT hands_played FROM Player_Games WHERE player_name = ?;', (player_name, ))
    for i in counter:
        counter = int(i[0])
        counter += 1
        break
    #sql = 'UPDATE Player_Games SET hands_played = {counter} WHERE player_name = {player_name};'.format(counter=counter, player_name=player_name)
    cur.execute('UPDATE Player_Games SET hands_played = ? WHERE player_name = ?;', (counter, player_name, ))
    con.commit()
    cur.close()











if __name__ == "__main__":
    game_stat_tracker(player_name = 'TEST', state = 'LOSE')

