-- MySQL dump 10.13  Distrib 5.6.37, for Win32 (AMD64)
--
-- Host: localhost    Database: mooresfarmmarket
-- ------------------------------------------------------
-- Server version	5.6.37

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `CUSTOMERS`
--

DROP TABLE IF EXISTS `CUSTOMERS`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `CUSTOMERS` (
  `CustomerID` int(11) NOT NULL AUTO_INCREMENT,
  `FirstName` varchar(50) NOT NULL,
  `LastName` varchar(50) NOT NULL,
  `Email` varchar(100) NOT NULL,
  `Password` varchar(30) NOT NULL,
  PRIMARY KEY (`CustomerID`),
  UNIQUE KEY `Email` (`Email`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `CUSTOMERS`
--

LOCK TABLES `CUSTOMERS` WRITE;
/*!40000 ALTER TABLE `CUSTOMERS` DISABLE KEYS */;
INSERT INTO `CUSTOMERS` VALUES (1,'Dominic','Holly','hollyd1@go.stockton.edu','hollyd1'),(2,'Alan','Ceron','cerona1@go.stockton.edu','cerona1'),(3,'Jack','Stewart','stewa149@go.stockton.edu','stewa149'),(4,'Joshua','Williams','willi687@go.stockton.edu','willi687');
/*!40000 ALTER TABLE `CUSTOMERS` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `EMPLOYEES`
--

DROP TABLE IF EXISTS `EMPLOYEES`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `EMPLOYEES` (
  `EmployeeID` int(11) NOT NULL AUTO_INCREMENT,
  `FirstName` varchar(100) NOT NULL,
  `LastName` varchar(100) NOT NULL,
  `Email` varchar(255) DEFAULT NULL,
  `Phone` varchar(15) DEFAULT NULL,
  `HireDate` date DEFAULT NULL,
  `Wage` varchar(6) DEFAULT NULL,
  PRIMARY KEY (`EmployeeID`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `EMPLOYEES`
--

LOCK TABLES `EMPLOYEES` WRITE;
/*!40000 ALTER TABLE `EMPLOYEES` DISABLE KEYS */;
/*!40000 ALTER TABLE `EMPLOYEES` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `FAVORITES`
--

DROP TABLE IF EXISTS `FAVORITES`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `FAVORITES` (
  `CustomerID` int(11) NOT NULL,
  `ProductID` int(11) NOT NULL,
  PRIMARY KEY (`CustomerID`,`ProductID`),
  KEY `ProductID` (`ProductID`),
  CONSTRAINT `favorites_ibfk_1` FOREIGN KEY (`CustomerID`) REFERENCES `CUSTOMERS` (`CustomerID`) ON DELETE CASCADE,
  CONSTRAINT `favorites_ibfk_2` FOREIGN KEY (`ProductID`) REFERENCES `PRODUCTS` (`ProductID`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `FAVORITES`
--

LOCK TABLES `FAVORITES` WRITE;
/*!40000 ALTER TABLE `FAVORITES` DISABLE KEYS */;
/*!40000 ALTER TABLE `FAVORITES` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `FLOWERS`
--

DROP TABLE IF EXISTS `FLOWERS`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `FLOWERS` (
  `ProductID` int(11) NOT NULL DEFAULT '0',
  `Annual` varchar(50) DEFAULT NULL,
  `SunOrShade` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`ProductID`),
  CONSTRAINT `flowers_ibfk_1` FOREIGN KEY (`ProductID`) REFERENCES `PRODUCTS` (`ProductID`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `FLOWERS`
--

LOCK TABLES `FLOWERS` WRITE;
/*!40000 ALTER TABLE `FLOWERS` DISABLE KEYS */;
/*!40000 ALTER TABLE `FLOWERS` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `HONEY`
--

DROP TABLE IF EXISTS `HONEY`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `HONEY` (
  `ProductID` int(11) NOT NULL DEFAULT '0',
  `Source` varchar(50) DEFAULT NULL,
  `Raw` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`ProductID`),
  CONSTRAINT `honey_ibfk_1` FOREIGN KEY (`ProductID`) REFERENCES `PRODUCTS` (`ProductID`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `HONEY`
--

LOCK TABLES `HONEY` WRITE;
/*!40000 ALTER TABLE `HONEY` DISABLE KEYS */;
INSERT INTO `HONEY` VALUES (10,' Clover',0),(11,'Wildfolwer',0),(12,'South Jersey Pine Barren',0),(13,'Buckwheat',0);
/*!40000 ALTER TABLE `HONEY` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `PRODUCE`
--

DROP TABLE IF EXISTS `PRODUCE`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `PRODUCE` (
  `ProductID` int(11) NOT NULL DEFAULT '0',
  `StorageInstructions` varchar(255) DEFAULT NULL,
  `Type` enum('Fruit','Vegetable') NOT NULL,
  `Location` varchar(16) DEFAULT NULL,
  PRIMARY KEY (`ProductID`),
  CONSTRAINT `produce_ibfk_1` FOREIGN KEY (`ProductID`) REFERENCES `PRODUCTS` (`ProductID`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `PRODUCE`
--

LOCK TABLES `PRODUCE` WRITE;
/*!40000 ALTER TABLE `PRODUCE` DISABLE KEYS */;
INSERT INTO `PRODUCE` VALUES (1,NULL,'Vegetable',NULL),(2,NULL,'Fruit',NULL),(3,NULL,'Fruit',NULL),(4,NULL,'Fruit',NULL),(5,NULL,'Fruit',NULL);
/*!40000 ALTER TABLE `PRODUCE` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `PRODUCTS`
--

DROP TABLE IF EXISTS `PRODUCTS`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `PRODUCTS` (
  `ProductID` int(11) NOT NULL AUTO_INCREMENT,
  `Name` varchar(255) NOT NULL,
  `Price` varchar(50) DEFAULT NULL,
  `CurrentlyAvailable` tinyint(1) NOT NULL DEFAULT '1',
  `Imagelink` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`ProductID`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `PRODUCTS`
--

LOCK TABLES `PRODUCTS` WRITE;
/*!40000 ALTER TABLE `PRODUCTS` DISABLE KEYS */;
INSERT INTO `PRODUCTS` VALUES (1,'corn',NULL,1,NULL),(2,'tomatoes',NULL,1,NULL),(3,'blueberries',NULL,1,NULL),(4,'raspberries',NULL,0,NULL),(5,'Red delicious apples',NULL,1,NULL),(10,'2lb. Clover Honey',NULL,1,NULL),(11,'2lb. Wildflower Honey',NULL,1,NULL),(12,'2lb. South Jersey Pine Barren Honey',NULL,1,NULL),(13,'2lb. Buckwheat Honey',NULL,1,NULL),(14,'Christmas Tree',NULL,0,NULL),(15,'Straw Bale',NULL,0,NULL);
/*!40000 ALTER TABLE `PRODUCTS` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `REVIEWS`
--

DROP TABLE IF EXISTS `REVIEWS`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `REVIEWS` (
  `ReviewID` int(11) NOT NULL AUTO_INCREMENT,
  `CustomerID` int(11) DEFAULT NULL,
  `Rating` int(11) DEFAULT NULL,
  `ReviewText` varchar(300) DEFAULT NULL,
  `ReviewDate` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`ReviewID`),
  KEY `CustomerID` (`CustomerID`),
  CONSTRAINT `reviews_ibfk_1` FOREIGN KEY (`CustomerID`) REFERENCES `CUSTOMERS` (`CustomerID`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `REVIEWS`
--

LOCK TABLES `REVIEWS` WRITE;
/*!40000 ALTER TABLE `REVIEWS` DISABLE KEYS */;
/*!40000 ALTER TABLE `REVIEWS` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Seasonal`
--

DROP TABLE IF EXISTS `Seasonal`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Seasonal` (
  `ProductID` int(11) NOT NULL DEFAULT '0',
  `Season` varchar(40) DEFAULT NULL,
  PRIMARY KEY (`ProductID`),
  CONSTRAINT `seasonal_ibfk_1` FOREIGN KEY (`ProductID`) REFERENCES `PRODUCTS` (`ProductID`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Seasonal`
--

LOCK TABLES `Seasonal` WRITE;
/*!40000 ALTER TABLE `Seasonal` DISABLE KEYS */;
INSERT INTO `Seasonal` VALUES (14,'Christmas'),(15,'Fall');
/*!40000 ALTER TABLE `Seasonal` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `VegetablePlant`
--

DROP TABLE IF EXISTS `VegetablePlant`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `VegetablePlant` (
  `ProductID` int(11) NOT NULL DEFAULT '0',
  `Season` varchar(40) DEFAULT NULL,
  `PlantType` enum('Vine','Stalk','Squash','Lettuce') DEFAULT NULL,
  PRIMARY KEY (`ProductID`),
  CONSTRAINT `vegetableplant_ibfk_1` FOREIGN KEY (`ProductID`) REFERENCES `PRODUCTS` (`ProductID`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `VegetablePlant`
--

LOCK TABLES `VegetablePlant` WRITE;
/*!40000 ALTER TABLE `VegetablePlant` DISABLE KEYS */;
/*!40000 ALTER TABLE `VegetablePlant` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-02-28 14:59:51
