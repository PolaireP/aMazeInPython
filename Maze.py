from random import randint, shuffle

class Maze:
    """
    Classe Labyrinthe
    Représentation sous forme de graphe non-orienté
    dont chaque sommet est une cellule (un tuple (l,c))
    et dont la structure est représentée par un dictionnaire
      - clés : sommets
      - valeurs : ensemble des sommets voisins accessibles
    """
    def __init__(self, height, width, empty):
        """
        Constructeur d'un labyrinthe de height cellules de haut 
        et de width cellules de large 
        Les voisinages sont initialisés à des ensembles vides
        Remarque : dans le labyrinthe créé, chaque cellule est complètement emmurée
        """
        self.height    = height
        self.width     = width
        self.neighbors = {(i,j): set() for i in range(height) for j in range (width)}

        if empty :
            for i in range(self.height) :
                for j in range(self.width):
                    if i - 1 >= 0 :
                        self.neighbors[(i,j)].add((i-1, j))
                    if i + 1 < self.height :
                        self.neighbors[(i,j)].add((i+1, j))
                    if j - 1 >= 0 :
                        self.neighbors[(i,j)].add((i, j-1))
                    if j + 1 < self.width :
                        self.neighbors[(i,j)].add((i, j+1))

    def info(self):
        """
        **NE PAS MODIFIER CETTE MÉTHODE**
        Affichage des attributs d'un objet 'Maze' (fonction utile pour deboguer)
        Retour:
            chaîne (string): description textuelle des attributs de l'objet
        """
        txt = "**Informations sur le labyrinthe**\n"
        txt += f"- Dimensions de la grille : {self.height} x {self.width}\n"
        txt += "- Voisinages :\n"
        txt += str(self.neighbors)+"\n"
        valid = True
        for c1 in {(i, j) for i in range(self.height) for j in range(self.width)}:
            for c2 in self.neighbors[c1]:
                if c1 not in self.neighbors[c2]:
                    valid = False
                    break
            else:
                continue
            break
        txt += "- Structure cohérente\n" if valid else f"- Structure incohérente : {c1} X {c2}\n"
        return txt

    def __str__(self):
        """
        **NE PAS MODIFIER CETTE MÉTHODE**
        Représentation textuelle d'un objet Maze (en utilisant des caractères ascii)
        Retour:
             chaîne (str) : chaîne de caractères représentant le labyrinthe
        """
        txt = ""
        # Première ligne
        txt += "┏"
        for j in range(self.width-1):
            txt += "━━━┳"
        txt += "━━━┓\n"
        txt += "┃"
        for j in range(self.width-1):
            txt += "   ┃" if (0,j+1) not in self.neighbors[(0,j)] else "    "
        txt += "   ┃\n"
        # Lignes normales
        for i in range(self.height-1):
            txt += "┣"
            for j in range(self.width-1):
                txt += "━━━╋" if (i+1,j) not in self.neighbors[(i,j)] else "   ╋"
            txt += "━━━┫\n" if (i+1,self.width-1) not in self.neighbors[(i,self.width-1)] else "   ┫\n"
            txt += "┃"
            for j in range(self.width):
                txt += "   ┃" if (i+1,j+1) not in self.neighbors[(i+1,j)] else "    "
            txt += "\n"
        # Bas du tableau
        txt += "┗"
        for i in range(self.width-1):
            txt += "━━━┻"
        txt += "━━━┛\n"

        return txt
    

    def add_wall(self, c1, c2):
        # Facultatif : on teste si les sommets sont bien dans le labyrinthe
        assert 0 <= c1[0] < self.height and \
            0 <= c1[1] < self.width and \
            0 <= c2[0] < self.height and \
            0 <= c2[1] < self.width, \
            f"Erreur lors de l'ajout d'un mur entre {c1} et {c2} : les coordonnées de sont pas compatibles avec les dimensions du labyrinthe"
        # Ajout du mur
        if c2 in self.neighbors[c1]:      # Si c2 est dans les voisines de c1
            self.neighbors[c1].remove(c2) # on le retire
        if c1 in self.neighbors[c2]:      # Si c3 est dans les voisines de c2
            self.neighbors[c2].remove(c1) # on le retire
    

    def remove_wall(self, c1, c2):
        """Enlève un mur entre les cellules c1 et c2

        Args:
            c1 (_type_): Cellule 1
            c2 (_type_): Cellule 2
        """
        # Test si les sommets sont dans le labyrinthe
        assert 0 <= c1[0] < self.height and \
            0 <= c1[1] < self.width and \
            0 <= c2[0] < self.height and \
            0 <= c2[1] < self.width, \
            f"Erreur lors de la suppression d'un mur entre {c1} et {c2} : les coordonnées de sont pas compatibles avec les dimensions du labyrinthe"
        if c1 not in self.neighbors[c2]:
            self.neighbors[c2].add(c1)
        if c2 not in self.neighbors[c1]:
            self.neighbors[c1].add(c2)


    def get_cells(self):
        """Renvoi toutes les cellules du labyrinthe

        Returns:
            List: cellules du labyrinthe
        """

        L = []

        for i in range(0, self.height):
            for j in range(0, self.width):
                L.append((i, j))
        
        return L
    

    def get_walls(self):
        """Récupère la liste des murs du labyrinthe

        Returns:
            list: list des murs du labyrinthe
        """
        walls = []
        # Pour chaque ligne
        for i in range(self.height) :
                # Pour chaque cellule de la ligne
                for j in range(self.width):
                    # Vérifier si il y'as un mur à droite et en bas de la cellule
                    if i + 1 < self.height and (i+1, j) not in self.neighbors[(i, j)] :
                        walls.append([(i,j), (i+1, j)])
                    if j + 1 < self.width and (i, j+1) not in self.neighbors[(i, j)] :
                        walls.append([(i,j), (i, j+1)])
        return walls
    

    def empty(self):
        """Supprime tous les murs d'un labyrinthe
        """
        # Pour chaque ligne
        for i in range(self.height) :
                # Pour chaque cellule
                for j in range(self.width):
                    # Supprimer les murs si ils sont dans le labyrinthe
                    if i - 1 >= 0 :
                        self.remove_wall((i, j), (i-1, j))
                    if i + 1 < self.height :
                        self.remove_wall((i, j), (i+1, j))
                    if j - 1 >= 0 :
                        self.remove_wall((i, j), (i, j-1))
                    if j + 1 < self.width :
                        self.remove_wall((i, j), (i, j+1))
    

    def fill(self):
        """Remplis le labyrinthe de murs
        """
        # Pour chaque ligne
        for i in range(self.height) :
                # Pour chaque cellule de la ligne
                for j in range(self.width):
                    # Ajouter chaque mur s'ils ne dépassent pas du labyrinthe
                    if i - 1 >= 0 :
                        self.add_wall((i,j), (i-1, j))
                    if i + 1 < self.height :
                        self.add_wall((i,j), (i+1, j))
                    if j - 1 >= 0 :
                        self.add_wall((i,j), (i, j-1))
                    if j + 1 < self.width :
                        self.add_wall((i,j), (i, j+1))
    
    def get_contiguous_cells(self, c):
        """Renvoi les voisins touchant la cellule

        Args:
            c (tuple): Cellule

        Returns:
            list: cellules touchant la cellule c
        """
        assert 0 <= c[0] < self.height and \
            0 <= c[1] < self.width, \
            f"La cellule {c} est en dehors du labyrinthe"
        
        cells = []

        if c[0] - 1 >= 0 :
            cells.append((c[0]-1, c[1]))
        if c[0] + 1 < self.width :
            cells.append((c[0]+1, c[1]))
        if c[1] - 1 >= 0 :
            cells.append((c[0], c[1]-1))
        if c[1] + 1 < self.width :
            cells.append((c[0], c[1]+1))
        
        return cells
    

    def get_reachable_cells(self, c):
        """Récupère les cellules reliées à c

        Args:
            c (tuple): cellule

        Returns:
            list: cellules reliées
        """

        assert 0 <= c[0] < self.height and \
            0 <= c[1] < self.width, \
            f"La cellule {c} est en dehors du labyrinthe"
        
        return list(self.neighbors[c])


    @classmethod
    def gen_btree(cls, h, w):
        """
        Algorithme de génération de labyrinthe par arbre binaire
        """
        # Initialisation d'un labyrinthe plein
        maze = cls(h, w, empty = False)
        
        # Pour chaque cellule du labyrinthe :
        for cell in maze.get_cells():
            cell_EST = (cell[0], cell[1]+1)
            cell_SUD = (cell[0]+1, cell[1])
            mur_EST = [cell, (cell[0], cell[1]+1)]
            mur_SUD = [cell, (cell[0]+1, cell[1])]
            liste_mur = maze.get_walls()
            
            # Si le mur entre la cellule courante et la cellule EST existe 
            # OU si le mur entre la cellule courante et la cellule SUD existe
            if mur_EST in liste_mur or mur_SUD in liste_mur:

                # Si le mur entre la cellule courante et la cellule EST existe 
                # ET si le mur entre la cellule courante et la cellule SUD existe
                # Alors supprimer aléatoirement le mur EST ou le mur SUD

                if mur_EST in liste_mur and mur_SUD in liste_mur:
                    maze.remove_wall(cell, [cell_EST, cell_SUD][randint(0,1)])

                # Sinon si le mur entre la cellule courante et la cellule EST existe
                # Alors supprimer le mur EST
                elif mur_EST in liste_mur:
                    maze.remove_wall(cell, cell_EST)

                # Sinon supprimer le mur SUD
                else:
                    maze.remove_wall(cell, cell_SUD)
        
        return maze


    @classmethod
    def gen_sidewinder(cls, h, w):
        """
        Algorithme de génération sidewinder
        """
        # Initialisation : création d’un labyrinthe plein
        maze = cls(h, w, empty = False)
        
        # Pour i allant de 0 à hauteur-2 :
        for i in range(h-1):
            # Initialiser une variable séquence comme liste vide
            sequence = []
            
            # Pour j allant de 0 à largeur-2 :
            for j in range(w-1):
                # Ajouter la cellule (i, j) à la séquence
                sequence.append((i,j))
                
                # Tirer à pile ou face :
                # Si c’est pile : Casser le mur EST de la cellule (i, j)
                if randint(0,1) == 1:
                    maze.remove_wall((i,j), (i,j+1))
                
                # Si c’est face :
                else:
                    # Casser le mur SUD d’une des cellules (choisie au hasard) qui 
                    # constituent le séquence qui vient d’être terminée.
                    cellule_aleatoire = sequence[randint(0, len(sequence)-1)]
                    maze.remove_wall(cellule_aleatoire, (cellule_aleatoire[0]+1, cellule_aleatoire[1]))
                    # Réinitialiser la séquence à une liste vide
                    sequence = []
            
            # Ajouter la dernière cellule à la séquence
            sequence.append((i,j+1))
            
            # Tirer une cellule au sort dans la séquence et casser son mur SUD
            cellule_aleatoire = sequence[randint(0, len(sequence)-1)]
            maze.remove_wall(cellule_aleatoire, (cellule_aleatoire[0]+1, cellule_aleatoire[1]))
        
        # Casser tous les murs EST de la dernière ligne
        for k in range(w-1):
            maze.remove_wall((h-1, k), (h-1, k+1))
            
        return maze
    

    @classmethod
    def gen_fusion(cls, h, w):
        """
        Algorithme de fusion de chemin
        """
        # Initialisation : création d’un labyrinthe plein
        maze = cls(h, w, empty = False)
        
        # On labélise les cellules de 1 à n
        label = {}
        liste_cellule = maze.get_cells()
        for i in range(1, h*w+1):
            label[liste_cellule[i-1]] = i
        
        # On extrait la liste de tous les murs et on les permute aléatoirement
        liste_murs = maze.get_walls()
        shuffle(liste_murs)
        
        # Pour chaque mur de la liste :
        for mur in liste_murs:
            # Si les deux cellules séparées par le mur n’ont pas le même label :
            if label[mur[0]] != label[mur[1]]:
                # casser le mur
                maze.remove_wall(mur[0], mur[1])
                
                # affecter le label de l’une des deux cellules, à l’autre,
                # et à toutes celles qui ont le même label que la deuxième
                label_temp = label[mur[1]]
                for cell in liste_cellule:
                    if label[cell] == label_temp:
                        label[cell] = label[mur[0]]
        
        return maze
    

    @classmethod
    def gen_exploration(cls, h, w):
        """Generation par exploration exhaustive

        Args:
            h (int): Hauteur du labyrinthe
            w (int): Largeur du labyrinthe

        Returns:
            Maze: Labyrinthe généré
        """

        # Initialisation du labyrinthe
        maze = cls(h, w, empty = False)

        # Choix de la première cellule
        firstCell = (randint(0, h-1), randint(0, w-1))

        # Création de l'ensemble des cellules visité et ajout de la première cellule
        visitedCells = set()
        visitedCells.add(firstCell)

        # Création de la pile avec la première cellule
        pile = [firstCell]

        # Tant que la pile n'est pas vide
        while len(pile) != 0 :

            # Prendre la cellule en haut de la pile
            actualCell = pile.pop(len(pile)-1)

            # Création du paramètre pour vérifier si des voisins sont déjà visités
            hasUnvisitedContigous = False

            # Récupération des cellules voisines de actualCell
            voisines = maze.get_contiguous_cells(actualCell)

            # Pour chaque cellule voisine
            for cellule in  voisines:

                # Vérifier si elle n'est pas visité
                if cellule not in visitedCells :
                    # Changer le paramètre a vrai
                    hasUnvisitedContigous = True
            
            # Si des voisins ne sont pas visités
            if hasUnvisitedContigous :

                #Réajouter actualCell a la pile
                pile.append(actualCell)

                # Récupérer un voisin non visité
                newCell = voisines[randint(0, len(voisines)-1)]
                while newCell in visitedCells :
                    newCell = voisines[randint(0, len(voisines)-1)]

                # Supprimer le mur entre actualCell et son voisin non visité
                maze.remove_wall(actualCell, newCell)
                
                # Ajouter le voisin aux cellules visités et au haut de la pile
                visitedCells.add(newCell)
                pile.append(newCell)
                
        return maze



    @classmethod
    def gen_wilson(cls, h, w):
        """Generation par algorithme wilson

        Args:
            h (int): Hauteur du labyrinthe
            w (int): Largeur du labyrinthe

        Returns:
            Maze: Labyrinthe généré
        """
        # Initialisation du labyrinthe
        maze = cls(h, w, empty = False)

        # Choix de la première cellule
        firstCell = (randint(0, h-1), randint(0, w-1))

        # Création de l'ensemble des cellules visité et ajout de la première cellule et récupération de toutes les cellules
        visitedCells = set()
        visitedCells.add(firstCell)
        mazeCells = maze.get_cells()

        # Tant que toutes les cellules ne sont pas marquées
        while len(maze.get_cells()) != len(visitedCells):
            
            # Prendre une cellule au hasard qui n'est pas marqué
            actualCell = mazeCells[randint(0, len(mazeCells)-1)]
            while actualCell in visitedCells :
                actualCell = mazeCells[randint(0, len(mazeCells)-1)]
            
            # Initialisation des étapes et du paramètre de marquage
            etapes = [actualCell]
            hasVisited = False

            # Tant que on ne tombe pas sur une cellule marquée
            while hasVisited == False :

                # Récupérer et piocher une cellule voisine au hasard
                voisines = maze.get_contiguous_cells(etapes[len(etapes)-1])
                randomVoisine = voisines[randint(0, len(voisines)-1)]
                
                # Si la voisine est déjà dans étape (boucle), enlever l'étape d'avant
                if randomVoisine in etapes :
                    etapes.pop(len(etapes)-1)

                # Sinon ajouter la voisine a étape et vérifier si elle n'est pas visité
                # Dans ce cas, change le paramètre
                else :
                    etapes.append(randomVoisine)
                    if randomVoisine in visitedCells :
                        hasVisited = True
            
            # Ajout de chaque cellule des étapes comme étant visitée, et suppression des murs
            # entre chaque cellule
            for i in range(len(etapes)-1):
                visitedCells.add(etapes[i])
                maze.remove_wall(etapes[i], etapes[i+1])
        
        return maze


    def overlay(self, content=None):
        """
        Rendu en mode texte, sur la sortie standard, \
        d'un labyrinthe avec du contenu dans les cellules
        Argument:
            content (dict) : dictionnaire tq content[cell] contient le caractère à afficher au milieu de la cellule
        Retour:
            string
        """
        if content is None:
            content = {(i,j):' ' for i in range(self.height) for j in range(self.width)}
        else:
            # Python >=3.9
            #content = content | {(i, j): ' ' for i in range(
            #    self.height) for j in range(self.width) if (i,j) not in content}
            # Python <3.9
            new_content = {(i, j): ' ' for i in range(self.height) for j in range(self.width) if (i,j) not in content}
            content = {**content, **new_content}
        txt = r""
        # Première ligne
        txt += "┏"
        for j in range(self.width-1):
            txt += "━━━┳"
        txt += "━━━┓\n"
        txt += "┃"
        for j in range(self.width-1):
            txt += " "+content[(0,j)]+" ┃" if (0,j+1) not in self.neighbors[(0,j)] else " "+content[(0,j)]+"  "
        txt += " "+content[(0,self.width-1)]+" ┃\n"
        # Lignes normales
        for i in range(self.height-1):
            txt += "┣"
            for j in range(self.width-1):
                txt += "━━━╋" if (i+1,j) not in self.neighbors[(i,j)] else "   ╋"
            txt += "━━━┫\n" if (i+1,self.width-1) not in self.neighbors[(i,self.width-1)] else "   ┫\n"
            txt += "┃"
            for j in range(self.width):
                txt += " "+content[(i+1,j)]+" ┃" if (i+1,j+1) not in self.neighbors[(i+1,j)] else " "+content[(i+1,j)]+"  "
            txt += "\n"
        # Bas du tableau
        txt += "┗"
        for i in range(self.width-1):
            txt += "━━━┻"
        txt += "━━━┛\n"
        return txt
    
    
    def solve_dfs(self, start, stop):
        """
        Algorithme de résolution parcours en profondeur
        """
        
        # Parcours du graphe jusqu’à ce qu’on trouve stop
        # Placer start dans la pile et marquer start
        pile = [start]
        visite = []
        # Mémoriser l’élément prédécesseur de start comme étant start
        pred = {start : start}
        
        # Tant qu’il reste des cellules non-marquées :
        while len(pile) > 0:
            # Prendre la première cellule et la retirer de la pile (appelons c, cette cellule)
            c = pile[0]
            del pile[0]
            # Si c correspond à A :
            if c == stop:
                # C’est terminé, on a trouvé un chemin vers la cellule de destination
                continue
            # Sinon :
            else:
                # Pour chaque voisine de c :
                for voisin in self.get_reachable_cells(c):
                    # Si elle n’est pas marquée :
                    if voisin not in visite:
                        # On la marque
                        visite.append(voisin)
                        # La mettre dans la pile
                        pile = [voisin] + pile
                        # Mémoriser son prédécesseur comme étant c
                        pred[voisin] = c
        
        # Reconstruction du chemin à partir des prédécesseurs
        chemin = []
        # Initialiser c à stop
        c = stop
        # Tant que c n’est pas start :
        while c != start:
            # ajouter c au chemin
            chemin.append(c)
            # mettre le prédécesseur de c dans c
            c = pred[c]
        # Ajouter start au chemin
        chemin.append(start)
        
        return chemin
    
    
    def solve_bfs(self, start, stop):
        """
        Algorithme de résolution parcours en largeur
        """
        
        # Parcours du graphe jusqu’à ce qu’on trouve stop
        # Placer start dans la file et marquer start
        file = [start]
        visite = []
        # Mémoriser l’élément prédécesseur de start comme étant start
        pred = {start : start}
        
        # Tant qu’il reste des cellules non-marquées :
        while len(file) > 0:
            # Prendre la première cellule et la retirer de la file (appelons c, cette cellule)
            c = file[0]
            del file[0]
            # Si c correspond à A :
            if c == stop:
                # C’est terminé, on a trouvé un chemin vers la cellule de destination
                continue
            # Sinon :
            else:
                # Pour chaque voisine de c :
                for voisin in self.get_reachable_cells(c):
                    # Si elle n’est pas marquée :
                    if voisin not in visite:
                            # On la marque
                            visite.append(voisin)
                            # La mettre dans la file
                            file.append(voisin)
                            # Mémoriser son prédécesseur comme étant c
                            pred[voisin] = c
        
        # Reconstruction du chemin à partir des prédécesseurs
        chemin = []
        # Initialiser c à stop
        c = stop
        # Tant que c n’est pas start :
        while c != start:
            # ajouter c au chemin
            chemin.append(c)
            # mettre le prédécesseur de c dans c
            c = pred[c]
        # Ajouter start au chemin
        chemin.append(start)
        
        return chemin