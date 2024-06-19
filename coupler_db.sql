-- MySQL dump 10.13  Distrib 8.0.33, for Win64 (x86_64)
--
-- Host: localhost    Database: coupler
-- ------------------------------------------------------
-- Server version	8.0.33

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `chats`
--

DROP TABLE IF EXISTS `chats`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `chats` (
  `chats_id` int NOT NULL AUTO_INCREMENT,
  `match_id_fk` int DEFAULT NULL,
  `couple_id_fk` int DEFAULT NULL,
  `message` varchar(250) DEFAULT NULL,
  `date` datetime DEFAULT NULL,
  `read` tinyint DEFAULT '0',
  PRIMARY KEY (`chats_id`),
  KEY `fk_from_couple_idx` (`match_id_fk`)
) ENGINE=InnoDB AUTO_INCREMENT=598 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `chats`
--

LOCK TABLES `chats` WRITE;
/*!40000 ALTER TABLE `chats` DISABLE KEYS */;
INSERT INTO `chats` VALUES (1,1,2,'Hola, como estais =)','2023-09-19 22:40:04',0),(2,1,5,'Holaa, bien, y vosotros?','2023-09-19 22:40:05',0),(3,2,2,'Hola lidia y vanessa!','2023-09-21 12:20:00',0),(4,3,2,'Nos ha gustado vuestro Perfil, como estais?','2023-09-22 12:20:00',1),(5,4,4,'Hola!! que chula esta app verdad? Es divertidisima','2023-08-22 12:20:00',1),(6,5,2,'Buenas! nosotros vivimos cerca parece!','2023-08-14 12:20:00',1),(7,6,7,'Hola, pareceis majos =)','2023-09-26 12:20:00',1),(8,1,5,'Nosotros de camino al cine.','2023-09-26 12:20:00',1),(592,3,1,'Hola!! Y a mi el vuestro =D','2024-02-06 14:25:47',1),(593,49,1,'Buenas tardes!','2024-02-06 14:25:58',1),(594,7,2,'Hola?','2024-02-06 14:27:53',1),(595,47,2,'Buenas tardes Estefanía','2024-02-06 14:28:10',1),(596,3,2,'Que suerte!','2024-02-06 14:28:58',1),(597,3,1,'Ya ves!!','2024-02-06 14:32:06',1);
/*!40000 ALTER TABLE `chats` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `conversations`
--

DROP TABLE IF EXISTS `conversations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `conversations` (
  `conversation_id` int NOT NULL AUTO_INCREMENT,
  `couple1_id_fk` int DEFAULT NULL,
  `couple2_id_fk` int DEFAULT NULL,
  `match_id_fk` int DEFAULT NULL,
  PRIMARY KEY (`conversation_id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `conversations`
--

LOCK TABLES `conversations` WRITE;
/*!40000 ALTER TABLE `conversations` DISABLE KEYS */;
INSERT INTO `conversations` VALUES (1,2,5,NULL),(2,3,2,NULL),(3,2,1,NULL),(4,4,2,NULL),(5,6,2,NULL),(6,2,7,NULL),(7,8,2,NULL);
/*!40000 ALTER TABLE `conversations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `couples`
--

DROP TABLE IF EXISTS `couples`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `couples` (
  `couple_id` int NOT NULL AUTO_INCREMENT,
  `name1` varchar(45) DEFAULT NULL,
  `name2` varchar(45) DEFAULT NULL,
  `age1` int DEFAULT NULL,
  `age2` int DEFAULT NULL,
  `couple_description` varchar(1000) DEFAULT NULL,
  `date_profile` datetime DEFAULT NULL,
  `email` varchar(105) DEFAULT NULL,
  `gender1` varchar(10) DEFAULT NULL,
  `gender2` varchar(10) DEFAULT NULL,
  `number_of_photos` int DEFAULT NULL,
  `folder` varchar(105) DEFAULT NULL,
  PRIMARY KEY (`couple_id`)
) ENGINE=InnoDB AUTO_INCREMENT=30 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `couples`
--

LOCK TABLES `couples` WRITE;
/*!40000 ALTER TABLE `couples` DISABLE KEYS */;
INSERT INTO `couples` VALUES (1,'Lucía','Paco',29,32,'¡Somos nuevos en la ciudad!\r\nNos gusta salir a correr después de trabajar y hacemos rutas los domingos. También los juegos de mesa. Buscamos hacer amigos y divertirnos. ¡Escríbenos para tomar algo!','2023-08-25 13:38:49','joseluis@gmail.com','Hombre','Mujer',4,''),(2,'Joge','Pepa',33,29,'Somos divertidos y activos. Nos gusta el deporte, la cultura, los planes al aire libre y filosofar sobre la vida. \r\nViajamos mucho, por eso las fotos!','2023-08-25 13:38:49','medinamaria90@gmail.com','Otros','No binario',4,''),(3,'Juan','Alma',43,62,'Buscamos amigos para salir a tomar fotos, que es lo que más nos gusta!! Únete a nosotros =D','2023-08-25 13:38:49',NULL,'No binario','Mujer',6,''),(4,'Alex','Carmen',21,22,'Probando esta app a ver qué tal! Con ganas de conocer gente y demás. Escríbenos =)','2023-08-25 13:38:49',NULL,'Hombre','Mujer',4,''),(5,'Ana','Blanca',23,27,'Somos hermanas y queremos conocer a gente diferente!!','2023-08-25 13:38:49',NULL,'Mujer','Mujer',5,''),(6,'Alicia','Jorge',23,43,'Amigos con ganas de hacer planes con gente nueva!','2023-08-25 13:38:49',NULL,'No binario','Mujer',5,''),(7,'Luis','Francisco',35,54,'Somos divertidos y honestos. Buscamos ampliar un poco nuestro circulo.','2023-09-18 16:55:20','mmcprogramacion@gmail.com','Hombre','Hombre',5,''),(8,'Emilio','Alicia',34,32,'Somos diseñadores y fotógrafos. Buscamos nuevos creativos para seguir aportando.','2023-09-18 16:55:20',NULL,'Mujer','Otros',3,''),(9,'Fran','Elvira',34,32,'De viaje, pero volvemos pronto!! Déjanos algún mensaje!!','2023-09-18 16:55:20',NULL,'Hombre','Mujer',4,''),(10,'Enma','Andalucía',27,36,'Yo soy abogada, Enma es ingeniera. Queremos emprender, te apuntas?','2023-08-25 13:38:49','joseluis@gmail.com','Mujer','Mujer',4,''),(11,'Louis','Francisca',33,45,'Somos fotógrafos de paisajes naturales, nos gusta la campiña cordobesa mucho.','2023-08-25 13:38:49','medinamaria90@gmail.com','Mujer','Mujer',3,''),(12,'Lope','Acisclo',43,48,'Las hojas y ramas secas son mi mayor afición. ¿Por qué? Pregúntamelo...','2023-08-25 13:38:49',NULL,'Hombre','Mujer',4,''),(13,'Alexander','Carmela',21,22,'Nos interesan las estructuras y cableado en el cielo, por ejemplo.','2023-08-25 13:38:49',NULL,'Hombre','Mujer',3,''),(14,'Ricardo','Sofía',23,43,'Fotografía abstracta de puestas de sol es nuestro hobby. ¿Cuál es el tuyo?','2023-08-25 13:38:49',NULL,'No binario','Mujer',4,''),(15,'Emiliano','Josephine',35,43,'Vehiculos, del derecho y del revés. Tenemos una casa en la montaña, estas invitado!','2023-09-18 16:55:20','mmcprogramacion@gmail.com','Mujer','Hombre',3,''),(16,'Hector','Elga',27,36,'Trabajamos en un puerto marítimo y también nos gusta ir al cine los sábados.','2023-08-25 13:38:49','joseluis@gmail.com','Hombre','Mujer',5,''),(17,'Jesus','Raquel',33,32,'Si no has estado en las medulas del Bierzo, tienes que ir cuanto antes!!! Es precioso. Vamos 20 veces al año. Apúntate la próxima! ','2023-08-25 13:38:49','medinamaria90@gmail.com','Otros','No binario',4,''),(18,'Alba','Lola',43,48,'A nosotras lo que nos gusta es el agua, ya sea sucia, limpia, de mar, de río, de lavabo o de garrafa. Danos agua, y nos haces felices!','2023-08-25 13:38:49',NULL,'Mujer','Mujer',4,''),(19,'Ernesto','Paula',21,22,'Somos aficionados a las fotografías justo antes de la puesta de sol. Qué bonitos colores sacan! No hacemos ninguna otra, figúrate tu.','2023-08-25 13:38:49',NULL,'Hombre','Mujer',4,''),(20,'Isabel','Fernando',23,43,'Me gustan, es decir, nos gustan las fotos de ciudades desde miradores. Tenemos una colección. ¿Nos regalas alguna? Nos faltan bastante ciudades del mundo y es un fastidio ir solo por la foto. ','2023-08-25 13:38:49',NULL,'No binario','Hombre',4,''),(21,'Luna','María',35,54,'¿Os gustan los templos budistas? ¿Son bonitos eh? Nos han dicho que hay uno en Benalmádena y queremos ir de excursión, buscamos acompañantes!','2023-09-18 16:55:20','mmcprogramacion@gmail.com','Hombre','Mujer',3,''),(22,'Emiliano','Acisclo',34,32,'Hola. Somos amigos y nos fascinan las rocas de distinto tipo. Sus colores, texturas... ¡Vente de excursión con nosotros!','2023-09-18 16:55:20',NULL,'Hombre','Hombre',4,''),(23,'Arturo','Basilio',34,32,'Yo soy psicologo, arturo es carpintero. Somos nuevos en la ciudad y queremos hacer amigos!!!! Buen rollo ante todo!!','2023-09-18 16:55:20',NULL,'Hombre','Hombre',4,''),(24,'Estefania','Virgini',27,36,'Qué te parece este gatito a gusto en su esquina, es mono, verdad?? Ay, no puedo con él!!! Like si eres gatuno!','2023-08-25 13:38:49','joseluis@gmail.com','Mujer','Mujer',3,''),(25,'Juan','Elena',23,32,'Somos divertidos y activos. Nos gusta el deporte, la cultura, los planes al aire libre y filosofar sobre la vida. \r\nBuscamos hacer amigos abiertos de mente con los que hacer rutas, ir al cine o al teatro y hablar de la vida. ¡Contáctanos si te apetece conectar! \r\n','2023-08-25 13:38:49','medinamaria90@gmail.com','Hombre','Mujer',4,''),(26,'Andi','Lucas',43,48,'No ponemos nuestras fotos reales para que no nos reconozcas, que somos famosos, pero queremos hacer a amigos nuevos!!! Pero dejamos los nombres, guiño guiño!!','2023-08-25 13:38:49',NULL,'Hombre','Hombre',3,''),(27,'Juana','Emilia',34,36,'Treintañeras poderosas y divertidas!!!! Con ganas de salir por ahí y pasarlo requetebién.','2023-08-25 13:38:49',NULL,'Mujer','Mujer',3,''),(28,'Juan','Salvador',23,43,'Somos Juan y Salvador, y nos encantan las gaviotas =D. \r\nLectores, voladores, soñadores. Atrévete a volar, aunque caerás. Caerás. Caerás. Y te levantarás bien alto!','2023-08-25 13:38:49',NULL,'No binario','Mujer',4,''),(29,'Nicky','Jam',35,54,'Somos runners y hemos hecho carreras de 1, 5, 10, y 15 km. Vamos a por la de 20km. Vente a entrenar con nosotros!','2023-09-18 16:55:20','mmcprogramacion@gmail.com','Hombre','Hombre',3,'');
/*!40000 ALTER TABLE `couples` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `couples_prematching`
--

DROP TABLE IF EXISTS `couples_prematching`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `couples_prematching` (
  `couples_prematching_id` int NOT NULL AUTO_INCREMENT,
  `couple1_id` int DEFAULT NULL,
  `couple2_id` int DEFAULT NULL,
  `compatibility` float DEFAULT NULL,
  `showed` int NOT NULL DEFAULT '0',
  `like` tinyint DEFAULT '0',
  `match_fk_id` int DEFAULT '0',
  PRIMARY KEY (`couples_prematching_id`)
) ENGINE=InnoDB AUTO_INCREMENT=339 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `couples_prematching`
--

LOCK TABLES `couples_prematching` WRITE;
/*!40000 ALTER TABLE `couples_prematching` DISABLE KEYS */;
INSERT INTO `couples_prematching` VALUES (3,21,2,1,1,1,0),(4,22,2,1,1,1,0),(8,26,2,1,1,1,0),(120,2,9,1,1,1,0),(121,2,12,1,1,1,0),(122,2,13,1,1,1,0),(130,2,21,1,1,0,0),(131,2,22,1,1,0,0),(135,2,26,1,1,0,0),(136,2,27,1,1,1,0),(137,2,28,1,1,1,0),(138,2,29,1,9,1,0),(277,2,10,1,1,1,0),(278,2,11,1,1,0,0),(279,2,14,1,1,0,0),(280,2,15,1,1,1,0),(281,2,16,1,1,0,0),(282,2,17,1,1,0,0),(283,2,18,1,1,0,0),(284,2,19,1,1,1,0),(285,7,1,1,1,1,0),(286,7,3,1,1,1,0),(287,7,4,1,0,NULL,0),(288,7,5,1,0,NULL,0),(289,7,6,1,0,NULL,0),(290,7,8,1,0,NULL,0),(291,7,9,1,0,NULL,0),(292,7,10,1,0,NULL,0),(293,7,11,1,0,NULL,0),(294,7,12,1,0,NULL,0),(295,7,13,1,0,NULL,0),(296,7,14,1,0,NULL,0),(297,7,15,1,0,NULL,0),(298,7,16,1,0,NULL,0),(299,7,17,1,0,NULL,0),(300,7,18,1,0,NULL,0),(301,7,19,1,0,NULL,0),(302,7,20,1,0,NULL,0),(303,7,21,1,0,NULL,0),(304,7,22,1,0,NULL,0),(305,7,23,1,0,NULL,0),(306,7,24,1,0,NULL,0),(307,7,25,1,0,NULL,0),(308,7,26,1,0,NULL,0),(309,7,27,1,0,NULL,0),(310,7,28,1,0,NULL,0),(311,7,29,1,0,NULL,0),(312,1,3,1,0,NULL,0),(313,1,4,1,0,NULL,0),(314,1,5,1,0,NULL,0),(315,1,6,1,0,NULL,0),(316,1,7,1,0,NULL,0),(317,1,8,1,0,NULL,0),(318,1,9,1,0,NULL,0),(319,1,10,1,0,NULL,0),(320,1,11,1,0,NULL,0),(321,1,12,1,0,NULL,0),(322,1,13,1,0,NULL,0),(323,1,14,1,0,NULL,0),(324,1,15,1,0,NULL,0),(325,1,16,1,0,NULL,0),(326,1,17,1,0,NULL,0),(327,1,18,1,0,NULL,0),(328,1,19,1,0,NULL,0),(329,1,20,1,0,NULL,0),(330,1,21,1,0,NULL,0),(331,1,22,1,0,NULL,0),(332,1,23,1,0,NULL,0),(333,1,24,1,0,NULL,0),(334,1,25,1,0,NULL,0),(335,1,26,1,0,NULL,0),(336,1,27,1,0,NULL,0),(337,1,28,1,0,NULL,0),(338,1,29,1,0,NULL,0);
/*!40000 ALTER TABLE `couples_prematching` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `labelcouple`
--

DROP TABLE IF EXISTS `labelcouple`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `labelcouple` (
  `labelcouple_id` int NOT NULL AUTO_INCREMENT,
  `couple_id_fk` int NOT NULL,
  `label` varchar(45) NOT NULL,
  PRIMARY KEY (`labelcouple_id`),
  KEY `couple_id_idx` (`couple_id_fk`),
  CONSTRAINT `couple_id` FOREIGN KEY (`couple_id_fk`) REFERENCES `couples` (`couple_id`)
) ENGINE=InnoDB AUTO_INCREMENT=785 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `labelcouple`
--

LOCK TABLES `labelcouple` WRITE;
/*!40000 ALTER TABLE `labelcouple` DISABLE KEYS */;
INSERT INTO `labelcouple` VALUES (626,1,'Deporte'),(627,1,'Senderismo'),(628,1,'Juegos de mesa'),(629,1,'Bicicleta'),(630,1,'Emprendimiento'),(631,1,'Crecimiento personal'),(654,3,'Meditación'),(655,3,'Activismos'),(656,3,'Manualidades'),(657,3,'Espiritualidad'),(664,4,'Yoga'),(665,4,'Senderismo'),(666,4,'Libros'),(667,4,'Series'),(668,4,'Cine'),(669,4,'Debates'),(670,5,'Deporte'),(671,5,'Tardeo'),(672,5,'Debates'),(673,5,'Conciertos'),(674,5,'Escritura'),(675,5,'Escalada'),(676,6,'Series'),(677,6,'Voluntariado'),(678,6,'Mascotas'),(679,6,'Activismos'),(680,6,'Hijos'),(681,7,'Fotografía'),(682,7,'Arte'),(683,7,'Voluntariado'),(684,7,'Debates'),(685,7,'Jardinería'),(686,8,'Teatro'),(687,8,'Debates'),(688,8,'Escritura'),(689,8,'Escalada'),(690,9,'Series'),(691,9,'Conciertos'),(692,9,'Ciencia'),(693,9,'Escalada'),(694,10,'Libros'),(695,10,'Meditación'),(696,10,'Manualidades'),(697,10,'LGTBQIA+'),(698,11,'Deporte'),(699,11,'Meditación'),(700,11,'Conciertos'),(701,11,'Activismos'),(702,12,'Yoga'),(703,12,'Tardeo'),(704,12,'Activismos'),(705,13,'Series'),(706,13,'Tardeo'),(707,13,'Activismos'),(708,13,'Arquitectura'),(709,14,'Deporte'),(710,14,'Mascotas'),(711,14,'Escritura'),(712,14,'Hijos'),(713,15,'Política'),(714,15,'Escritura'),(715,15,'Manualidades'),(716,15,'Aventuras'),(717,16,'Religión'),(718,16,'Espiritualidad'),(719,16,'LGTBQIA+'),(720,17,'Series'),(721,17,'Debates'),(722,17,'Filosofía'),(723,18,'Deporte'),(724,18,'Juegos de mesa'),(725,18,'Salir de Fiesta'),(726,18,'Mascotas'),(727,19,'Arte'),(728,19,'Voluntariado'),(729,19,'Meditación'),(730,19,'Manualidades'),(731,20,'Arte'),(732,20,'Naturaleza'),(733,20,'Museos'),(734,20,'Crecimiento personal'),(735,21,'Mascotas'),(736,21,'Escalada'),(737,22,'Cocina'),(738,22,'Series'),(739,22,'Cine'),(740,22,'Teatro'),(744,23,'Cine'),(745,23,'Manualidades'),(746,23,'Psicología'),(747,24,'Mascotas'),(748,24,'Activismos'),(749,24,'Filosofía'),(750,24,'Espiritualidad'),(751,24,'LGTBQIA+'),(756,25,'Cine'),(757,25,'Camping'),(758,25,'Jardinería'),(759,25,'Escritura'),(760,26,'Senderismo'),(761,26,'Cine'),(762,26,'Camping'),(763,26,'Espiritualidad'),(764,26,'LGTBQIA+'),(765,26,'Emprendimiento'),(766,27,'Arte'),(767,27,'Voluntariado'),(768,27,'Tardeo'),(769,27,'Meditación'),(770,28,'Arte'),(771,28,'Hijos'),(772,28,'Cultura'),(773,28,'Museos'),(774,28,'Crecimiento personal'),(775,29,'Cine'),(776,29,'Jardinería'),(777,29,'Filosofía'),(778,29,'Cafeterías'),(779,2,'Teatro'),(780,2,'Hijos'),(781,2,'Cafeterías'),(782,2,'Museos'),(783,2,'Emprendimiento'),(784,2,'Crecimiento personal');
/*!40000 ALTER TABLE `labelcouple` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `labels`
--

DROP TABLE IF EXISTS `labels`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `labels` (
  `label_id` int NOT NULL AUTO_INCREMENT,
  `label` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`label_id`)
) ENGINE=InnoDB AUTO_INCREMENT=39 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `labels`
--

LOCK TABLES `labels` WRITE;
/*!40000 ALTER TABLE `labels` DISABLE KEYS */;
INSERT INTO `labels` VALUES (1,'Deportes'),(2,'Yoga'),(3,'Senderismo'),(4,'Viajes'),(5,'Cocina'),(6,'Fotografía'),(7,'Arte'),(8,'Lectura'),(9,'Música en vivo'),(10,'Cine'),(11,'Teatro'),(12,'Juegos de mesa'),(13,'Voluntariado'),(14,'Ciencia ficción'),(15,'Camping'),(16,'Bicicleta'),(17,'Artes marciales'),(18,'Jardinería'),(19,'Mascotas'),(20,'Ecología'),(21,'Moda'),(22,'Meditación'),(23,'Conciertos'),(24,'Escritura creativa'),(25,'Astronomía'),(26,'Historia'),(27,'Viajes en moto'),(28,'Escalada'),(29,'Parentalidad y crianza'),(30,'Comida gourmet'),(31,'Bailes de salón'),(32,'Artes y manualidades'),(33,'Arquitectura'),(34,'Cultura'),(35,'Debates'),(36,'Restaurantes'),(37,'Espiritualidad'),(38,'Psicología');
/*!40000 ALTER TABLE `labels` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `matches`
--

DROP TABLE IF EXISTS `matches`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `matches` (
  `matches_id` int NOT NULL AUTO_INCREMENT,
  `fk_couple1_id` int NOT NULL,
  `fk_couple2_id` int NOT NULL,
  `date_match` datetime DEFAULT NULL,
  `conversation_opened` tinyint DEFAULT '0',
  PRIMARY KEY (`matches_id`),
  KEY `fk_couple1_id_idx` (`fk_couple1_id`),
  KEY `fk_couple2_id_idx` (`fk_couple2_id`)
) ENGINE=InnoDB AUTO_INCREMENT=53 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `matches`
--

LOCK TABLES `matches` WRITE;
/*!40000 ALTER TABLE `matches` DISABLE KEYS */;
INSERT INTO `matches` VALUES (1,2,5,'2023-10-03 17:20:31',1),(2,3,2,'2023-10-03 17:20:31',1),(3,2,1,'2023-10-03 17:20:31',1),(4,4,2,'2023-10-03 17:20:31',1),(5,6,2,'2023-10-03 17:20:31',1),(6,2,7,'2023-10-03 17:20:31',1),(7,8,2,'2023-10-03 17:20:31',1),(45,1,20,'2023-10-03 17:16:10',0),(46,2,23,'2023-10-03 17:16:14',0),(47,2,24,'2023-10-03 17:16:23',1),(48,2,25,'2023-10-03 17:20:31',0),(49,1,3,'2023-10-03 17:20:31',1),(50,1,6,'2023-10-03 17:20:31',0),(51,1,8,'2023-10-03 17:20:31',0),(52,3,1,'2023-10-03 17:20:31',0);
/*!40000 ALTER TABLE `matches` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pictures`
--

DROP TABLE IF EXISTS `pictures`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pictures` (
  `pic_id` int NOT NULL,
  `file_name` varchar(45) DEFAULT NULL,
  `file_route` varchar(45) DEFAULT NULL,
  `fk_couple_id` int DEFAULT NULL,
  PRIMARY KEY (`pic_id`),
  KEY `couple_id_idx` (`fk_couple_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pictures`
--

LOCK TABLES `pictures` WRITE;
/*!40000 ALTER TABLE `pictures` DISABLE KEYS */;
/*!40000 ALTER TABLE `pictures` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `use_register`
--

DROP TABLE IF EXISTS `use_register`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `use_register` (
  `register_id` int NOT NULL,
  `fk_user_id` int DEFAULT NULL,
  `action` varchar(45) DEFAULT NULL,
  `details` varchar(45) DEFAULT NULL,
  `date` datetime DEFAULT NULL,
  PRIMARY KEY (`register_id`),
  KEY `fk_user_id_idx` (`fk_user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `use_register`
--

LOCK TABLES `use_register` WRITE;
/*!40000 ALTER TABLE `use_register` DISABLE KEYS */;
/*!40000 ALTER TABLE `use_register` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-02-07 11:52:28
