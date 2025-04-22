-- MySQL dump 10.13  Distrib 8.0.41, for Win64 (x86_64)
--
-- Host: localhost    Database: mooresfarmmarket
-- ------------------------------------------------------
-- Server version	8.0.41

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `customers`
--

DROP TABLE IF EXISTS `customers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `customers` (
  `CustomerID` int NOT NULL AUTO_INCREMENT,
  `FirstName` varchar(50) NOT NULL,
  `LastName` varchar(50) NOT NULL,
  `Email` varchar(100) NOT NULL,
  `Password` varchar(30) NOT NULL,
  PRIMARY KEY (`CustomerID`),
  UNIQUE KEY `Email` (`Email`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `customers`
--

LOCK TABLES `customers` WRITE;
/*!40000 ALTER TABLE `customers` DISABLE KEYS */;
INSERT INTO `customers` VALUES (1,'Dominic','Holly','hollyd1@go.stockton.edu','hollyd1'),(2,'Alan','Ceron','cerona1@go.stockton.edu','cerona1'),(3,'Jack','Stewart','stewa149@go.stockton.edu','stewa149'),(4,'Joshua','Williams','willi687@go.stockton.edu','willi687');
/*!40000 ALTER TABLE `customers` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `employees`
--

DROP TABLE IF EXISTS `employees`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `employees` (
  `EmployeeID` int NOT NULL AUTO_INCREMENT,
  `FirstName` varchar(100) NOT NULL,
  `LastName` varchar(100) NOT NULL,
  `Email` varchar(255) DEFAULT NULL,
  `Phone` varchar(15) DEFAULT NULL,
  `HireDate` date DEFAULT NULL,
  `Wage` varchar(6) DEFAULT NULL,
  `password` varchar(255) NOT NULL,
  `position` enum('admin','employee') NOT NULL,
  PRIMARY KEY (`EmployeeID`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `employees`
--

LOCK TABLES `employees` WRITE;
/*!40000 ALTER TABLE `employees` DISABLE KEYS */;
INSERT INTO `employees` VALUES (1,'Scott','Moore','smoore388@yahoo.com','7323492876',NULL,NULL,'1234','admin'),(2,'Tyler','DelPrete','tydel579@gmail.com','7325691655',NULL,NULL,'1234','employee'),(3,'Tony','Del Prete','tony@gmail.com','123456789',NULL,NULL,'1234','employee'),(4,'Emily','Similarion','emily@gmail.com','123456789',NULL,NULL,'1234','employee');
/*!40000 ALTER TABLE `employees` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `employeeschedule`
--

DROP TABLE IF EXISTS `employeeschedule`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `employeeschedule` (
  `ShiftID` int NOT NULL AUTO_INCREMENT,
  `EmployeeID` int NOT NULL,
  `Year` int NOT NULL,
  `Month` int NOT NULL,
  `Day` int NOT NULL,
  `TimeIn` time NOT NULL,
  `TimeOut` time NOT NULL,
  PRIMARY KEY (`ShiftID`),
  KEY `EmployeeID` (`EmployeeID`),
  CONSTRAINT `employeeschedule_ibfk_1` FOREIGN KEY (`EmployeeID`) REFERENCES `employees` (`EmployeeID`) ON DELETE CASCADE,
  CONSTRAINT `employeeschedule_chk_1` CHECK ((`Year` >= 2000)),
  CONSTRAINT `employeeschedule_chk_2` CHECK ((`Month` between 1 and 12)),
  CONSTRAINT `employeeschedule_chk_3` CHECK ((`Day` between 1 and 31))
) ENGINE=InnoDB AUTO_INCREMENT=25 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `employeeschedule`
--

LOCK TABLES `employeeschedule` WRITE;
/*!40000 ALTER TABLE `employeeschedule` DISABLE KEYS */;
INSERT INTO `employeeschedule` VALUES (14,4,2025,4,19,'02:09:00','16:05:00'),(17,3,2025,4,19,'09:00:00','14:00:00'),(18,3,2025,4,27,'05:00:00','19:00:00'),(19,2,2025,4,25,'13:00:00','18:00:00'),(20,2,2025,4,29,'09:00:00','14:00:00'),(23,1,2025,5,1,'08:00:00','15:00:00'),(24,1,2025,5,3,'10:00:00','14:00:00');
/*!40000 ALTER TABLE `employeeschedule` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `favorites`
--

DROP TABLE IF EXISTS `favorites`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `favorites` (
  `CustomerID` int NOT NULL,
  `ProductID` int NOT NULL,
  PRIMARY KEY (`CustomerID`,`ProductID`),
  KEY `ProductID` (`ProductID`),
  CONSTRAINT `favorites_ibfk_1` FOREIGN KEY (`CustomerID`) REFERENCES `customers` (`CustomerID`) ON DELETE CASCADE,
  CONSTRAINT `favorites_ibfk_2` FOREIGN KEY (`ProductID`) REFERENCES `products` (`ProductID`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `favorites`
--

LOCK TABLES `favorites` WRITE;
/*!40000 ALTER TABLE `favorites` DISABLE KEYS */;
INSERT INTO `favorites` VALUES (3,4),(1,5),(1,36);
/*!40000 ALTER TABLE `favorites` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `flowers`
--

DROP TABLE IF EXISTS `flowers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `flowers` (
  `ProductID` int NOT NULL DEFAULT '0',
  `Annual` varchar(50) DEFAULT NULL,
  `SunOrShade` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`ProductID`),
  CONSTRAINT `flowers_ibfk_1` FOREIGN KEY (`ProductID`) REFERENCES `products` (`ProductID`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `flowers`
--

LOCK TABLES `flowers` WRITE;
/*!40000 ALTER TABLE `flowers` DISABLE KEYS */;
INSERT INTO `flowers` VALUES (35,'Annual','Sun or Shade'),(36,'Annual','Sun'),(37,'Perrenial','Sun'),(53,'Annual','Sun');
/*!40000 ALTER TABLE `flowers` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `honey`
--

DROP TABLE IF EXISTS `honey`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `honey` (
  `ProductID` int NOT NULL DEFAULT '0',
  `Source` varchar(50) DEFAULT NULL,
  `Raw` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`ProductID`),
  CONSTRAINT `honey_ibfk_1` FOREIGN KEY (`ProductID`) REFERENCES `products` (`ProductID`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `honey`
--

LOCK TABLES `honey` WRITE;
/*!40000 ALTER TABLE `honey` DISABLE KEYS */;
INSERT INTO `honey` VALUES (49,'Buckwheat',0),(50,'Buckwheat',0),(51,'Cranberry',0);
/*!40000 ALTER TABLE `honey` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `produce`
--

DROP TABLE IF EXISTS `produce`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `produce` (
  `ProductID` int NOT NULL DEFAULT '0',
  `StorageInstructions` varchar(255) DEFAULT NULL,
  `Type` enum('Fruit','Vegetable') NOT NULL,
  `Location` varchar(16) DEFAULT NULL,
  PRIMARY KEY (`ProductID`),
  CONSTRAINT `produce_ibfk_1` FOREIGN KEY (`ProductID`) REFERENCES `products` (`ProductID`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `produce`
--

LOCK TABLES `produce` WRITE;
/*!40000 ALTER TABLE `produce` DISABLE KEYS */;
INSERT INTO `produce` VALUES (1,'fridge','Vegetable','sdjngjnmskjdn'),(2,'counter','Fruit','Georgia'),(3,'fridge','Fruit','California'),(4,'fridge','Fruit','California'),(5,'fridge','Fruit','California');
/*!40000 ALTER TABLE `produce` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `products`
--

DROP TABLE IF EXISTS `products`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `products` (
  `ProductID` int NOT NULL AUTO_INCREMENT,
  `Name` varchar(255) NOT NULL,
  `Price` varchar(50) DEFAULT NULL,
  `CurrentlyAvailable` tinyint(1) NOT NULL DEFAULT '1',
  `Imagelink` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`ProductID`)
) ENGINE=InnoDB AUTO_INCREMENT=56 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `products`
--

LOCK TABLES `products` WRITE;
/*!40000 ALTER TABLE `products` DISABLE KEYS */;
INSERT INTO `products` VALUES (1,'corn','5',1,'corn.jpg'),(2,'tomatoes','',1,'tomatoes.jpg'),(3,'blueberries','3.49',1,'blueberries.jpg'),(4,'raspberries','3.99',0,'raspberries.jpg'),(5,'red delicious apples','',0,'reddelicious.jpg'),(15,'Straw Bale','15',1,'strawbale.jpg'),(18,'wreath','24.95',0,'wreath.jpg'),(35,'mum','5.95',0,'mum.jpg'),(36,'sunflower','8.95',1,'sunflower.jpg'),(37,'Hydrangea','34.95',1,'hydregana.jpg'),(49,'2lb Buckwheat Honey','14.95',1,'IMG_2441.jpg'),(50,'5lb Buckwheat Honey','32.95',1,'IMG_2439.jpg'),(51,'5lb Cranberry Honey','34.95',1,'IMG_2440.jpg'),(52,'Sun decoration','34.95',1,'IMG_2442.jpg'),(53,'Assorted Hanging Plants','24.95',1,'IMG_2443.jpg'),(54,'Tomato plant','2.79',1,'IMG_2445.jpg'),(55,'Lettuce plant','2.79',1,'IMG_2444.jpg');
/*!40000 ALTER TABLE `products` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `reviews`
--

DROP TABLE IF EXISTS `reviews`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `reviews` (
  `ReviewID` int NOT NULL AUTO_INCREMENT,
  `CustomerID` int DEFAULT NULL,
  `Rating` int DEFAULT NULL,
  `ReviewText` varchar(300) DEFAULT NULL,
  `ReviewDate` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`ReviewID`),
  KEY `CustomerID` (`CustomerID`),
  CONSTRAINT `reviews_ibfk_1` FOREIGN KEY (`CustomerID`) REFERENCES `customers` (`CustomerID`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `reviews`
--

LOCK TABLES `reviews` WRITE;
/*!40000 ALTER TABLE `reviews` DISABLE KEYS */;
INSERT INTO `reviews` VALUES (2,3,3,'this place rocks','2025-04-03 22:29:01'),(4,3,4,'this place is cool','2025-04-10 17:28:25'),(5,2,5,'this place is chill','2025-04-10 18:15:03');
/*!40000 ALTER TABLE `reviews` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `seasonal`
--

DROP TABLE IF EXISTS `seasonal`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `seasonal` (
  `ProductID` int NOT NULL DEFAULT '0',
  `Season` varchar(40) DEFAULT NULL,
  PRIMARY KEY (`ProductID`),
  CONSTRAINT `seasonal_ibfk_1` FOREIGN KEY (`ProductID`) REFERENCES `products` (`ProductID`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `seasonal`
--

LOCK TABLES `seasonal` WRITE;
/*!40000 ALTER TABLE `seasonal` DISABLE KEYS */;
INSERT INTO `seasonal` VALUES (15,'Fall'),(52,'');
/*!40000 ALTER TABLE `seasonal` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `time_off_requests`
--

DROP TABLE IF EXISTS `time_off_requests`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `time_off_requests` (
  `id` int NOT NULL AUTO_INCREMENT,
  `employeeid` int NOT NULL,
  `start_date` date NOT NULL,
  `end_date` date NOT NULL,
  `reason` text,
  `status` varchar(20) DEFAULT 'Pending',
  `request_date` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `employeeid` (`employeeid`),
  CONSTRAINT `time_off_requests_ibfk_1` FOREIGN KEY (`employeeid`) REFERENCES `employees` (`EmployeeID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `time_off_requests`
--

LOCK TABLES `time_off_requests` WRITE;
/*!40000 ALTER TABLE `time_off_requests` DISABLE KEYS */;
/*!40000 ALTER TABLE `time_off_requests` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `vegetableplant`
--

DROP TABLE IF EXISTS `vegetableplant`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `vegetableplant` (
  `ProductID` int NOT NULL DEFAULT '0',
  `Season` varchar(40) DEFAULT NULL,
  `PlantType` enum('Vine','Stalk','Squash','Lettuce') DEFAULT NULL,
  PRIMARY KEY (`ProductID`),
  CONSTRAINT `vegetableplant_ibfk_1` FOREIGN KEY (`ProductID`) REFERENCES `products` (`ProductID`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `vegetableplant`
--

LOCK TABLES `vegetableplant` WRITE;
/*!40000 ALTER TABLE `vegetableplant` DISABLE KEYS */;
INSERT INTO `vegetableplant` VALUES (54,'Summer','Vine'),(55,'Summer','Lettuce');
/*!40000 ALTER TABLE `vegetableplant` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-04-22 13:49:20
