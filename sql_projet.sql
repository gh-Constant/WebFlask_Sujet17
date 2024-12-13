-- Create database
CREATE DATABASE IF NOT EXISTS monuments_db;
USE monuments_db;

-- Create type_epoque table
CREATE TABLE type_epoque (
    id INT PRIMARY KEY AUTO_INCREMENT,
    libelle VARCHAR(50) NOT NULL
);

-- Create tableau table
CREATE TABLE tableau (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nomTableau VARCHAR(100) NOT NULL,
    prixAssurance DECIMAL(10,2),
    dateRealisation DATE,
    peintre VARCHAR(100),
    localisationMusee VARCHAR(100),
    photo VARCHAR(100),
    mouvement VARCHAR(50),
    typeEpoque_id INT,
    FOREIGN KEY (typeEpoque_id) REFERENCES type_epoque(id)
);

-- Insert type_epoque data
INSERT INTO type_epoque (id, libelle) VALUES 
(1, 'Renaissance'),
(2, 'Temps Modernes'),
(3, 'Contemporain'),
(4, 'Moyen-Age');

-- Insert tableau data
INSERT INTO tableau (id, nomTableau, prixAssurance, dateRealisation, peintre, localisationMusee, photo, mouvement, typeEpoque_id) VALUES 
(1, 'La Joconde', 4000, '1506-10-21', 'Léonard de Vinci', 'Louvre', 'laJoconde.jpeg', NULL, 1),
(2, 'Le Radeau de La Méduse', 300.2, '1819-03-15', 'Théodore Géricault', 'Louvre', 'leRadeauDeLaMeduse.jpeg', 'romantisme', 3),
(3, 'Guernica', 200.6, '1937-06-04', 'Pablo Picasso', 'Reina Sofia', 'guernica.jpeg', 'cubisme', 3),
(4, "L'Ecole d'Athène", 105.3, '1512-02-21', 'Raphaël', 'Vatican', 'lEcoleDAthene.jpeg', 'maniérisme', 1),
(5, 'La Jeune Fille à la perle', 2040, '1665-11-12', 'Johannes Vermeer', 'Mauritshuis', 'laJeuneFilleALaPerle.jpeg', 'baroque', 2),
(6, 'La Laitière', 3040, '1658-05-30', 'Johannes Vermeer', 'Rijksmuseum', 'laLaitière.jpeg', 'baroque', 2),
(7, 'Le Calvaire', 5060, '1505-09-30', 'Josse Lieferinxe', 'Louvre', 'leCalvaire.jpeg', NULL, 1),
(9, 'Portrait du bouffon Gonella', 1230, '1445-03-18', 'Jean Fouquet', 'Kunsthistorisches Museum', 'leProtraitduBouffonGonella.jpeg', NULL, 4),
(10, 'La liberté guidant le peuple', 150.5, '1830-12-25', 'Eugène DelaCroix', 'Louvre', 'laLiberteGuidantlePeuple.jpeg', 'romantisme', 3),
(11, "Rentable de l'Agneau mystique", 1010, '1432-01-05', 'Jan van Eyck', 'Cathédrale Saint-Bavon de Gand', 'AgneauMystique.jpeg', NULL, 4);