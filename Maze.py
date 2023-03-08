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

        for i in range(0, self.height-1):
            for j in range(0, self.width-1):
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