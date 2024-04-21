# PokerBot - an autonomous online poker agent

This script was designed by Alexander Ignatiev and Chad Gothelf. It is able to play online poker on the application
PokerStars, without using any of PokerStar's API. By simply analyzing the content of the computer's screen, this program
is able to avoid bot detection software. By running this code on a Raspberry Pi, and utilizing a microcontroller to
simulate mouse movement, one is able to avoid detection from kernel-level anti-cheats.


> [!IMPORTANT]
> We do not condone the use of PokerBot for any commercial purposes, including online cash games or tournaments. This
> project was simply an experiment to see if such a bot was possible to make. For this reason, we are not including any 
> installation manual along with our code.

## Alogorithm overview


PokerBot creates its strategy by calculating its equity against its opponent's potential hand distribution. It then uses that calculation to determine which action would net him the most money in the long run, but calculating the expected value of each action. The bot is even capable of elementary bluffing, when it believes that its hand isn’t good enough to win on average, but could potentially scare the opponent into folding. 

Because the player pool is relatively small for each poker website, it is quite common for our bot to run into the same players at different tables over days, months or even years. For this reason, Poker Bot was designed to remember how a certain player bets after a game has concluded, and store that information in a database. The bot can then access this database, and retrieve its knowledge on the player’s behavior the next time it runs into him. This allows the bot to adapt its strategy much faster to the player’s actions, resulting in better returns over many games.

Our algorithm is far from perfect, as it can be exploited fairly easily by a smart player. Because of our over reliance on expected value derived from pot odds, it is quite easy to bluff against our bot. For this reason, we are going to have to improve this algorithm a lot by the time we release PokerBot II. 


## Demonstration

Below is a video illustrating PokerBot in action. 

