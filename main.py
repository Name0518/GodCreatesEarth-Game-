import pgzrun
import random
#imports pygame zero and random package to use in the game

HEIGHT = 500  #Sets height for game
WIDTH = 600  #Sets width for game
god = Actor('god')
objective = Actor('objective1')
titlescreen = Actor('titlescreen')
waterdrop = Actor('waterdrop')
ending = Actor('ending')
#Initializes all the actors and images used in the game
god.y = 400  #Initializes the y position of the god
current_level = 0  #Initializes current level index
islands = []  #Initializes the list of islands
island_coord = []  #Initializes island coordinates
clay = []  #Initializes the list of clay
clay_counter = 0  #Initializes the clay counter to use for the while loop
score = 0  #initializes the score for the 1st level
score2 = 0  #initializes the score for the 2nd level

while clay_counter < 5:
  clay.append(Rect((random.randint(0, 500), random.randint(0, 500)), (40, 40)))
  clay_counter += 1
#Uses a while loops for the clay to spawn in random locations


def draw():
  global current_level  #calls global variables for current level
  screen.clear()
  screen.fill('blue')
  titlescreen.draw(
  )  #Clears the screen and fills the background with blue, drawing the main title screen later
  if current_level == 0:
    level_zero()
  elif current_level == 1:
    level_one()
  elif current_level == 2:
    level_two()
  elif current_level == 3:
    level_three()
  #Calls a different draw function based on the current level


def update():
  global islands
  global god
  global score
  global score2
  if keyboard.left and god.x > 69:
    god.x -= 5
  elif keyboard.right and god.x < 531:
    god.x += 5
  if keyboard.space:
    titlescreen.y = 1000
  if keyboard.up and god.y > 69:
    god.y -= 5
  elif keyboard.down and god.y < 431:
    god.y += 5
  #Initializes basic controls for the god, and makes sure the god stays in the screen
  if current_level == 1:
    for i in range(len(clay)):
      if god.colliderect(clay[i - 1]):
        del clay[i - 1]
        score += 1
  #Will check if the god collides with the clay and if so, it will delete the clay and add 1 to the score
  elif current_level == 2:
    god.y = 400  #Sets y position of the player to 400 for level 3
    if beat_level() == False:
      waterdrop.y += 3
      if waterdrop.y > 500:
        waterdrop.x = random.randint(0, 500)
        waterdrop.y = 0
        #Water will keep dropping in random locations until the player beats the level
      if god.colliderect(waterdrop):
        score2 += 1
        waterdrop.x = random.randint(0, 500)
        waterdrop.y = 0
        #Adds a point to the score if the player collides with the water, resets the water to the top of the screen
    else:
      waterdrop.y = 1000
      #the water will stay at y = 1000 if the player beat the level


def on_key_down(key):
  global current_level
  global islands
  global island_coord
  if current_level == 0:
    if key == keys.A:
      islands.append(Actor('island'))
      island_coord.append(
          [god.x, god.y]
      )  #for the first level, the island will be added to the list to be drawn and the coordinates will be added to another list to be spawned later
      if beat_level():
        current_level += 1  #Advances the level index if the level is beat
  elif current_level == 1:
    if key == keys.A and beat_level():
      current_level += 1  #If the second level is beat the player will advance to the third level when A is pressed
  elif current_level == 2:
    if key == keys.A:  #If the third level is beat the player will advance to the fourth level when A is pressed
      current_level += 1
  elif current_level == 3:
    if key == keys.X:
      exit()  #The game will exit when X is pressed


def level_zero():
  global islands
  global island_coord
  global current_level
  for i in range(len(islands)):
    islands[i].x = island_coord[i][0]
    islands[i].y = island_coord[i][1]
    islands[i].draw()  #Generate islands based on the coordinates in the list
  if titlescreen.y == 1000:
    god.draw()
    objective.draw(
    )  #Draws the god  and objective panel if the titlescreen is out of the bounds
  if len(islands) == 5 and beat_level():
    screen.clear(
    )  #If the level is beat, clear the level and advance to the next level
    current_level += 1


def level_one():
  global score
  screen.fill('dark green')  #fills the screen with dark green
  god.draw()  #Draws god in another y position
  objective.image = 'objective2'  #changes objective image to the next level objective and draws it
  objective.draw()
  for i in range(len(clay)):
    screen.draw.filled_rect(clay[i], "grey")  #Spawns clay in random locations
  screen.draw.text(f'Score: {str(score)}', (100, 100),
                   color='white')  #Initializes score board
  if score == 5:
    screen.draw.text(good_job_text(score), (100, 150), color='white')
    screen.draw.text(
        f'Press A to continue', (100, 200), color='white'
    )  #Congratulates player with the good job text function and prompts them to advance to the next level
    if current_level == 2:
      screen.clear()  #clears screen after


def level_two():
  global score2
  screen.fill('dark green')  #fills the screen with dark green
  god.image = 'god_bucket'  #changes the player image to the bucket image
  god.draw()  #Draws player
  objective.image = 'objective3'  #changes objective image to the next level objective and draws it
  objective.draw()
  waterdrop.draw()  #Draws the objective panel and waterdrop
  if score2 > 0:
    god.image = 'god_bucketwater'
    god.draw(
    )  #Switches the god image and redraws it if the player has collected a point
  screen.draw.text(f'Score: {str(score2)}',
                   (100, 150))  #Initializes score board
  if beat_level():
    screen.draw.text(f'good job! now you have {score2} drops of water!',
                     (100, 175),
                     color='white')
    screen.draw.text(f'Press A to continue', (100, 200), color='white')


#If the level is beat it will congratulate the player with the good job text function and prompts them to advance to the next level


def level_three():
  screen.clear()
  ending.draw()


#Draws the ending screen for the final level


def good_job_text(pts):
  return f"{'good job!'.upper()} Now you have {str(pts)} pieces of clay!"
  #A function that returns a string that is used to congralutate the player for beating the level and collecting the required amount of clay (5) needed


def beat_level():
  global current_level, islands
  beat = False
  if current_level == 0:
    if len(islands) == 5:
      return not beat
    else:  #Will return a boolean depending on if the player has finished the required objective or not
      return beat
  elif current_level == 1:
    if score == 5:
      return not beat  #Will return a boolean depending on if the player has finished the required objective or not
    else:
      return beat
  elif current_level == 2:
    if score2 == 10:
      return not beat  #Will return a boolean depending on if the player has finished the required objective or not
    else:
      return beat


pgzrun.go()
#Runs the game
