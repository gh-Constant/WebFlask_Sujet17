CREATE DATABASE IF NOT EXISTS monuments_db;
USE monuments_db;

DROP TABLE IF EXISTS tableaux;
DROP TABLE IF EXISTS type_epoque;

CREATE TABLE type_epoque (
    id INT PRIMARY KEY AUTO_INCREMENT,
    libelle VARCHAR(50) NOT NULL
);

CREATE TABLE tableaux (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nomTableau VARCHAR(100) NOT NULL,
    prixAssurance DECIMAL(10,2),
    dateRealisation DATE,
    peintre VARCHAR(100),
    localisationMusee VARCHAR(100),
    photo VARCHAR(100),
    mouvement VARCHAR(50),
    typeEpoque_id INT,
    CONSTRAINT constraint_type_epoque FOREIGN KEY (typeEpoque_id) REFERENCES type_epoque(id)
);

INSERT INTO type_epoque (id, libelle) VALUES 
(1, 'Renaissance'),
(2, 'Temps Modernes'),
(3, 'Contemporain'),
(4, 'Moyen-Age');


INSERT INTO tableaux (id, nomTableau, prixAssurance, dateRealisation, peintre, localisationMusee, photo, mouvement, typeEpoque_id) VALUES 
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

ALTER TABLE tableaux DROP CONSTRAINT constraint_type_epoque;

ALTER TABLE tableaux ADD CONSTRAINT constraint_type_epoque FOREIGN KEY (typeEpoque_id) REFERENCES type_epoque(id);

SELECT 
    type_epoque.libelle AS Epoque,
    COUNT(tableaux.id) AS Nombre_Tableaux,
    ROUND(AVG(tableaux.prixAssurance), 2) AS Prix_Moyen_Assurance
FROM type_epoque
LEFT JOIN tableaux ON type_epoque.id = tableaux.typeEpoque_id
GROUP BY type_epoque.id, type_epoque.libelle
ORDER BY type_epoque.libelle;

PREPARE tableau_prepare FROM 'INSERT INTO tableaux (nomTableau, prixAssurance, dateRealisation, peintre, localisationMusee, photo, mouvement, typeEpoque_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?)';

SET @nom = 'Les Nymphéas';
SET @prix = 2500.00;
SET @date = '1920-01-01';
SET @peintre = 'Claude Monet';
SET @musee = 'Musée de l\'Orangerie';
SET @photo = 'nympheas.jpeg';
SET @mouvement = 'impressionnisme';
SET @type_id = 3;

EXECUTE tableau_prepare USING @nom, @prix, @date, @peintre, @musee, @photo, @mouvement, @type_id;

DEALLOCATE PREPARE tableau_prepare;

SELECT * FROM tableaux

