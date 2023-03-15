import pygame, sys, random, time
from Maze import Maze

def generateModel(laby, height, width):
    liste_cellules = laby.get_cells()
    
    # Creation labyritnhe plein
    maze = []
    tab = []
    for ligne in range(height):
        tab.append([])
        for colonne in range(width*2):
            if colonne % 2 == 0:
                tab[ligne].append(1)
            else:
                tab[ligne].append(0)
        tab[ligne].append(1)
    
    for i in range(height):
        maze.append([1]*(1+width*2))
        maze.append(tab[i])
    maze.append([1]*(1+width*2))
    
    # Attribuer valeur
    for ligne in range(len(maze)):
        for colonne in range(len(maze[0])):
            if maze[ligne][colonne] == 0:
                maze[ligne][colonne] = liste_cellules[0]
                del liste_cellules[0]
    
    for ligne in range(1, len(maze)-1):
        for colonne in range(1, len(maze[0])-1):
            if maze[ligne][colonne] != 1 and maze[ligne][colonne] != 0:
                if colonne+2 < len(maze[0]) and maze[ligne][colonne+2] in laby.get_reachable_cells(maze[ligne][colonne]):
                    maze[ligne][colonne+1] = 0
                if ligne+2 < len(maze) and maze[ligne+2][colonne] in laby.get_reachable_cells(maze[ligne][colonne]):
                    maze[ligne+1][colonne] = 0
    
    for ligne in range(len(maze)):
        for colonne in range(len(maze[0])):
            if maze[ligne][colonne] != 1 and maze[ligne][colonne] != 0:
                maze[ligne][colonne] = 0
    
    maze[len(maze)-2][len(maze[0])-1] = 0
                    
    return maze

dimension = 8
laby = Maze.gen_wilson(dimension,dimension)
maze = generateModel(laby, dimension, dimension)

pygame.init()
pygame.font.init()
# Temps
clock = pygame.time.Clock()
# Initialisation du chronomètre
start_time = time.time()
# Estimation du temps
duration = (laby.distance_geo((0,0), (dimension-1, dimension-1)) * 2) + 2

screen_width = 700
screen_height = 700
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Laby')

block_size = 30

score_font = pygame.font.SysFont("roboto", 50)
indications_font = pygame.font.SysFont("roboto", 20)

# Labyrinthe
maze_lenght = len(maze[0]) * block_size
maze_width = len(maze) * block_size
maze_x = (screen_width / 2) - (maze_lenght / 2)
maze_y = (screen_height / 2) - (maze_width / 2)

point_arrivee = pygame.Rect(maze_width + maze_x, (maze_lenght + maze_y) - 2 * block_size, block_size, block_size)

# Joueur
player_size = block_size / 2
player_start = ((maze_x + player_size/2) + block_size, (maze_y + player_size/2) + block_size)
player = pygame.Rect(player_start[0], player_start[1], player_size, player_size)

# Partie
level = 1

# Musique
#pygame.mixer.music.load("music.mp3")
#pygame.mixer.music.set_volume(0.20)
#pygame.mixer.music.play(-1)


black = (0,0,0)
violet = ("#752092")
violet_clair = ("#C957BC")
orange = ("#FFC872")
beige = ("#faf0e6")

while True:

    # Enregistrement dernière position
    previous_location_player = (player.x, player.y)

    #Handling input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                player.y += block_size
            if event.key == pygame.K_UP:
                player.y -= block_size
            if event.key == pygame.K_LEFT:
                player.x -= block_size
            if event.key == pygame.K_RIGHT:
                player.x += block_size
    

    # Génération du labyrinthe
    screen.fill(beige)
    wall_x = maze_x
    wall_y = maze_y
    wall_list = []
    for ligne in range(len(maze)):
        for colonne in range(len(maze[0])):
            if maze[ligne][colonne] == 1:
                wall = pygame.Rect(wall_x, wall_y, block_size, block_size)
                wall_list.append(wall)
                pygame.draw.rect(screen, orange, wall)
            wall_x += block_size
        wall_x = maze_x
        wall_y += block_size

    # Lancement du chronomètre
    temps_ecoule = time.time() - start_time
    temps_restant = duration - temps_ecoule
    minutes, seconds = divmod(temps_restant, 60)

    if temps_restant <= 0:
        print("Le minuteur est terminé.")
        break

    # Collision mur
    for i in range(len(wall_list)):
        if player.colliderect(wall_list[i]):
            player.x = previous_location_player[0]
            player.y = previous_location_player[1]
    

    if player.colliderect(point_arrivee):
        
        # Regeneration map
        dimension += 1
        level += 1
        while len(maze) * block_size > 0.7 * screen_width:
            block_size -= 1
        laby = Maze.gen_wilson(dimension,dimension)
        maze = generateModel(laby, dimension, dimension)

        maze_lenght = len(maze[0]) * block_size
        maze_width = len(maze) * block_size
        maze_x = (screen_width / 2) - (maze_lenght / 2)
        maze_y = (screen_height / 2) - (maze_width / 2)
        point_arrivee = pygame.Rect(maze_width + maze_x, (maze_lenght + maze_y) - 2 * block_size, block_size, block_size)

        # Reset chrono
        start_time = time.time()
        duration = (laby.distance_geo((0,0), (dimension-1, dimension-1)) * 2) + 2

        # Nouvelle position joueur
        player_size = block_size / 2
        player_start = ((maze_x + player_size/2) + block_size, (maze_y + player_size/2) + block_size)
        player = pygame.Rect(player_start[0], player_start[1], player_size, player_size)


    score = score_font.render(f"Niveau : {level}", 1, violet_clair)
    indications = indications_font.render("Utilisez les flèches pour vous déplacer", 1, violet_clair)
    screen.blit(score, (screen_width/2.5, 10))
    screen.blit(indications, (screen_width/3, screen_height - 50))

    # Affichage chronomètre
    chrono = score_font.render('{:02d}:{:02d}'.format(int(minutes), int(seconds)), True, violet_clair)
    screen.blit(chrono, (screen_width - 150, 10))

    pygame.draw.rect(screen, violet_clair, point_arrivee)
    pygame.draw.ellipse(screen, violet_clair, player)


    #Updating the window
    pygame.display.flip()
    clock.tick(60)