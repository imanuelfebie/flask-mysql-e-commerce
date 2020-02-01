-- MySQL dump 10.16  Distrib 10.1.38-MariaDB, for Win64 (AMD64)
--
-- Host: us-cdbr-iron-east-05.cleardb.net    Database: heroku_7edc97b06ff109d
-- ------------------------------------------------------
-- Server version	5.6.42-log

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
-- Table structure for table `address`
--

DROP TABLE IF EXISTS `address`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `address` (
  `address_id` int(11) NOT NULL AUTO_INCREMENT,
  `line1` varchar(45) NOT NULL,
  `line2` varchar(45) DEFAULT NULL,
  `line3` varchar(45) DEFAULT NULL,
  `city_id` int(11) DEFAULT NULL,
  `postal_code` varchar(45) NOT NULL,
  PRIMARY KEY (`address_id`),
  KEY `city_id` (`city_id`),
  CONSTRAINT `address_ibfk_2` FOREIGN KEY (`city_id`) REFERENCES `city` (`city_id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=171 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `address`
--

LOCK TABLES `address` WRITE;
/*!40000 ALTER TABLE `address` DISABLE KEYS */;
INSERT INTO `address` VALUES (111,'Far Far Away Road 12A','Somewhere','',71,'661123'),(121,'Jl. Rawa Belong 1','Palmerah','',51,'112233'),(131,'A Galaxy','Far Far','Away',51,'112233'),(141,'Pondok Indah','Jakarta Selatan','',51,'112244'),(151,'Knight road 111','','',71,'112233'),(161,'Some road','Here','',51,'556677');
/*!40000 ALTER TABLE `address` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Temporary table structure for view `address_view`
--

DROP TABLE IF EXISTS `address_view`;
/*!50001 DROP VIEW IF EXISTS `address_view`*/;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
/*!50001 CREATE TABLE `address_view` (
  `address_id` tinyint NOT NULL,
  `line1` tinyint NOT NULL,
  `line2` tinyint NOT NULL,
  `line3` tinyint NOT NULL,
  `postal_code` tinyint NOT NULL,
  `city_name` tinyint NOT NULL,
  `country_name` tinyint NOT NULL
) ENGINE=MyISAM */;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `admin`
--

DROP TABLE IF EXISTS `admin`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `admin` (
  `admin_id` int(1) NOT NULL AUTO_INCREMENT,
  `username` varchar(45) NOT NULL,
  `email` varchar(45) NOT NULL,
  `password` varchar(45) NOT NULL,
  PRIMARY KEY (`admin_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `admin`
--

LOCK TABLES `admin` WRITE;
/*!40000 ALTER TABLE `admin` DISABLE KEYS */;
INSERT INTO `admin` VALUES (1,'admin','test@test.com','password');
/*!40000 ALTER TABLE `admin` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `category`
--

DROP TABLE IF EXISTS `category`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `category` (
  `category_id` int(11) NOT NULL AUTO_INCREMENT,
  `category_name` varchar(120) NOT NULL,
  PRIMARY KEY (`category_id`),
  UNIQUE KEY `category_name` (`category_name`),
  UNIQUE KEY `category_name_2` (`category_name`)
) ENGINE=InnoDB AUTO_INCREMENT=91 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `category`
--

LOCK TABLES `category` WRITE;
/*!40000 ALTER TABLE `category` DISABLE KEYS */;
INSERT INTO `category` VALUES (51,'Laptops'),(41,'Other'),(81,'PC\'s'),(61,'Smartphones'),(71,'Tablets');
/*!40000 ALTER TABLE `category` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `city`
--

DROP TABLE IF EXISTS `city`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `city` (
  `city_id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(120) NOT NULL,
  `country_id` int(11) NOT NULL,
  PRIMARY KEY (`city_id`),
  UNIQUE KEY `name` (`name`),
  KEY `country_id` (`country_id`),
  CONSTRAINT `city_ibfk_1` FOREIGN KEY (`country_id`) REFERENCES `country` (`country_id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=91 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `city`
--

LOCK TABLES `city` WRITE;
/*!40000 ALTER TABLE `city` DISABLE KEYS */;
INSERT INTO `city` VALUES (51,'Jakarta',61),(61,'Bandung',61),(71,'Depok',61),(81,'Tokyo',71);
/*!40000 ALTER TABLE `city` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `country`
--

DROP TABLE IF EXISTS `country`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `country` (
  `country_id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(120) NOT NULL,
  PRIMARY KEY (`country_id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=101 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `country`
--

LOCK TABLES `country` WRITE;
/*!40000 ALTER TABLE `country` DISABLE KEYS */;
INSERT INTO `country` VALUES (61,'Indonesia'),(71,'Japan'),(81,'Thailand');
/*!40000 ALTER TABLE `country` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Temporary table structure for view `customer_view`
--

DROP TABLE IF EXISTS `customer_view`;
/*!50001 DROP VIEW IF EXISTS `customer_view`*/;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
/*!50001 CREATE TABLE `customer_view` (
  `user_id` tinyint NOT NULL,
  `email` tinyint NOT NULL,
  `firstname` tinyint NOT NULL,
  `lastname` tinyint NOT NULL,
  `joined_on` tinyint NOT NULL,
  `address_line1` tinyint NOT NULL,
  `address_line2` tinyint NOT NULL,
  `address_line3` tinyint NOT NULL,
  `postal_code` tinyint NOT NULL,
  `city_id` tinyint NOT NULL,
  `city_name` tinyint NOT NULL,
  `country_name` tinyint NOT NULL
) ENGINE=MyISAM */;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `order_item`
--

DROP TABLE IF EXISTS `order_item`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `order_item` (
  `order_item_id` int(11) NOT NULL AUTO_INCREMENT,
  `product_id` int(11) NOT NULL,
  `quantity` int(11) DEFAULT NULL,
  PRIMARY KEY (`order_item_id`),
  KEY `product_id` (`product_id`),
  CONSTRAINT `order_item_ibfk_1` FOREIGN KEY (`product_id`) REFERENCES `product` (`product_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `order_item`
--

LOCK TABLES `order_item` WRITE;
/*!40000 ALTER TABLE `order_item` DISABLE KEYS */;
INSERT INTO `order_item` VALUES (1,221,2),(2,221,1);
/*!40000 ALTER TABLE `order_item` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `payment_method`
--

DROP TABLE IF EXISTS `payment_method`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `payment_method` (
  `payment_name` varchar(45) NOT NULL,
  `description` varchar(45) NOT NULL,
  `payment_method_id` int(11) NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`payment_method_id`)
) ENGINE=InnoDB AUTO_INCREMENT=31 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `payment_method`
--

LOCK TABLES `payment_method` WRITE;
/*!40000 ALTER TABLE `payment_method` DISABLE KEYS */;
INSERT INTO `payment_method` VALUES ('OVO','',1),('Creditcard cc','',11),('Debit','',21);
/*!40000 ALTER TABLE `payment_method` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `product`
--

DROP TABLE IF EXISTS `product`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `product` (
  `product_id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(45) NOT NULL,
  `description` varchar(120) NOT NULL,
  `price` decimal(10,0) NOT NULL,
  `available` tinyint(4) NOT NULL,
  `image` blob,
  `category_id` int(11) NOT NULL,
  `store_id` int(11) NOT NULL,
  `added_on` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`product_id`),
  KEY `category_id` (`category_id`),
  KEY `store_id` (`store_id`),
  CONSTRAINT `product_ibfk_1` FOREIGN KEY (`category_id`) REFERENCES `category` (`category_id`),
  CONSTRAINT `product_ibfk_2` FOREIGN KEY (`store_id`) REFERENCES `store` (`store_id`)
) ENGINE=InnoDB AUTO_INCREMENT=291 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `product`
--

LOCK TABLES `product` WRITE;
/*!40000 ALTER TABLE `product` DISABLE KEYS */;
INSERT INTO `product` VALUES (221,'Test','msalkmdalksa',13,1,NULL,51,81,'2020-01-31 16:57:38'),(231,'asus','used laptop',80,0,NULL,51,71,'2020-01-31 17:19:46'),(241,'Thinkpad X220','snajdnaskjnksa',189,1,NULL,51,81,'2020-02-01 06:59:07'),(251,'Thinkpad X1 CARBON','The best thinkpad ever',1599,0,NULL,51,81,'2020-02-01 09:07:46'),(261,'ASUS x21332','Lorem Ipsum',1299,0,NULL,81,81,'2020-02-01 09:08:53'),(271,'Vivo V11 PRO','Some description here',399,1,NULL,61,91,'2020-02-01 09:37:08'),(281,'test update','Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliq',2199,1,NULL,41,101,'2020-02-01 10:24:42');
/*!40000 ALTER TABLE `product` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Temporary table structure for view `product_view`
--

DROP TABLE IF EXISTS `product_view`;
/*!50001 DROP VIEW IF EXISTS `product_view`*/;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
/*!50001 CREATE TABLE `product_view` (
  `product_id` tinyint NOT NULL,
  `name` tinyint NOT NULL,
  `description` tinyint NOT NULL,
  `price` tinyint NOT NULL,
  `available` tinyint NOT NULL,
  `image` tinyint NOT NULL,
  `added_on` tinyint NOT NULL,
  `category_name` tinyint NOT NULL,
  `store_name` tinyint NOT NULL
) ENGINE=MyISAM */;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `store`
--

DROP TABLE IF EXISTS `store`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `store` (
  `store_id` int(11) NOT NULL AUTO_INCREMENT,
  `store_name` varchar(120) NOT NULL,
  `about` varchar(120) NOT NULL,
  `joined_on` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`store_id`),
  UNIQUE KEY `store_name` (`store_name`),
  UNIQUE KEY `store_id` (`store_id`)
) ENGINE=InnoDB AUTO_INCREMENT=151 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `store`
--

LOCK TABLES `store` WRITE;
/*!40000 ALTER TABLE `store` DISABLE KEYS */;
INSERT INTO `store` VALUES (71,'Lightsabers','BLALA','2020-01-31 15:56:13'),(81,'Used Laptops','Selling high quality used laptops','2020-01-31 15:59:28'),(91,'Vivo Store','Lorem Ipsum','2020-02-01 09:21:54'),(101,'Hobbit Relics','Selling everything hobbit related','2020-02-01 10:22:12'),(121,'A.I Cars','crime fighting cars','2020-02-01 10:26:36'),(141,'Test Store','testing things','2020-02-01 10:28:21');
/*!40000 ALTER TABLE `store` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `transaction`
--

DROP TABLE IF EXISTS `transaction`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `transaction` (
  `transaction_id` int(11) NOT NULL AUTO_INCREMENT,
  `payment_method_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `ordered_on` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`transaction_id`),
  KEY `payment_method_id` (`payment_method_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `transaction_ibfk_2` FOREIGN KEY (`payment_method_id`) REFERENCES `payment_method` (`payment_method_id`),
  CONSTRAINT `transaction_ibfk_4` FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `transaction`
--

LOCK TABLES `transaction` WRITE;
/*!40000 ALTER TABLE `transaction` DISABLE KEYS */;
INSERT INTO `transaction` VALUES (1,11,191,'2020-01-01 11:42:41'),(2,1,171,'2019-12-10 22:10:23');
/*!40000 ALTER TABLE `transaction` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `transaction_order_items`
--

DROP TABLE IF EXISTS `transaction_order_items`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `transaction_order_items` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `transaction_id` int(11) NOT NULL,
  `order_item_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `transaction_id` (`transaction_id`),
  KEY `order_item_id` (`order_item_id`),
  CONSTRAINT `transaction_order_items_ibfk_1` FOREIGN KEY (`transaction_id`) REFERENCES `transaction` (`transaction_id`) ON DELETE CASCADE,
  CONSTRAINT `transaction_order_items_ibfk_2` FOREIGN KEY (`order_item_id`) REFERENCES `order_item` (`order_item_id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `transaction_order_items`
--

LOCK TABLES `transaction_order_items` WRITE;
/*!40000 ALTER TABLE `transaction_order_items` DISABLE KEYS */;
INSERT INTO `transaction_order_items` VALUES (1,1,1),(2,2,2);
/*!40000 ALTER TABLE `transaction_order_items` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user` (
  `user_id` int(11) NOT NULL AUTO_INCREMENT,
  `email` varchar(120) NOT NULL,
  `firstname` varchar(120) NOT NULL,
  `lastname` varchar(120) DEFAULT NULL,
  `password` varchar(255) NOT NULL,
  `joined_on` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `address_id` int(11) DEFAULT NULL,
  `is_active` tinyint(1) DEFAULT NULL,
  `store_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `email` (`email`),
  UNIQUE KEY `user_id` (`user_id`),
  UNIQUE KEY `store_id` (`store_id`),
  KEY `address_id` (`address_id`),
  CONSTRAINT `user_ibfk_1` FOREIGN KEY (`address_id`) REFERENCES `address` (`address_id`),
  CONSTRAINT `user_ibfk_2` FOREIGN KEY (`store_id`) REFERENCES `store` (`store_id`)
) ENGINE=InnoDB AUTO_INCREMENT=271 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES (171,'lukeskywalker@jedi.com','Luke','Skywalker','pbkdf2:sha256:150000$QqIOzWUm$380e7b57aa5c0d857e996bfa47c1cf49dd222eed0159068aa1930a493484db05','2020-01-31 15:56:14',121,1,71),(181,'macewindu@jedi.com','Mace','Windu','pbkdf2:sha256:150000$JexIar3a$7313a98063341398a6134e1f23c18f2893ec91f8186f6c45405065d724bf6191','2020-02-01 05:47:01',131,1,81),(191,'michaeljordan@gmail.com','Michael','Jordan','pbkdf2:sha256:150000$QWzxoo5M$08f1c84b9feaa110e13856deec39dda3d4b34b8837e75b3cfc0b668796097d68','2020-01-31 16:30:24',NULL,NULL,NULL),(221,'darthvader@jointhedarkside.ds','Anakan','Skywalker','pbkdf2:sha256:150000$S6aLyHE5$f255535b8182af161e19d0df547d6e8d108ec0394589823b2e0705b643125ef1','2020-02-01 09:36:11',NULL,1,91),(231,'billgates@gmail.com','Bill ','Gates','pbkdf2:sha256:150000$YZTWgCaF$3307a1d3825edb8fe0b252fb2c2dfcd0694fb980709fdb64f28560614589a70d','2020-02-01 08:23:53',141,1,NULL),(241,'hobbit@town.com','Frodo','Baggins','pbkdf2:sha256:150000$C4rdKBrH$f59515f745670f3f7d3bd9ed962eba4bc351c2e3f61dcbaef702696110a61eae','2020-02-01 10:22:13',NULL,1,101),(251,'knighrider@kitt.com','Knight','Rider','pbkdf2:sha256:150000$UPXF2BZl$38949018ffa96fa1c6fe99f721e630783efb7223821b66299ba0fa9a2494d157','2020-02-01 10:26:37',151,1,121),(261,'test@test.com','Test','User','pbkdf2:sha256:150000$kCRekwse$70e92973e68efccfe294e733841673ad39441b2bef84f10c7df294fdb15b8806','2020-02-01 10:28:22',161,1,141);
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Final view structure for view `address_view`
--

/*!50001 DROP TABLE IF EXISTS `address_view`*/;
/*!50001 DROP VIEW IF EXISTS `address_view`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8 */;
/*!50001 SET character_set_results     = utf8 */;
/*!50001 SET collation_connection      = utf8_general_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`b5de033d9bb9f7`@`%` SQL SECURITY DEFINER */
/*!50001 VIEW `address_view` AS select `a`.`address_id` AS `address_id`,`a`.`line1` AS `line1`,`a`.`line2` AS `line2`,`a`.`line3` AS `line3`,`a`.`postal_code` AS `postal_code`,`city`.`name` AS `city_name`,`country`.`name` AS `country_name` from ((`address` `a` join `city` on((`a`.`city_id` = `city`.`city_id`))) join `country` on((`city`.`country_id` = `country`.`country_id`))) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `customer_view`
--

/*!50001 DROP TABLE IF EXISTS `customer_view`*/;
/*!50001 DROP VIEW IF EXISTS `customer_view`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8 */;
/*!50001 SET character_set_results     = utf8 */;
/*!50001 SET collation_connection      = utf8_general_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`b5de033d9bb9f7`@`%` SQL SECURITY DEFINER */
/*!50001 VIEW `customer_view` AS select `u`.`user_id` AS `user_id`,`u`.`email` AS `email`,`u`.`firstname` AS `firstname`,`u`.`lastname` AS `lastname`,`u`.`joined_on` AS `joined_on`,`a`.`line1` AS `address_line1`,`a`.`line2` AS `address_line2`,`a`.`line3` AS `address_line3`,`a`.`postal_code` AS `postal_code`,`a`.`city_id` AS `city_id`,`city`.`name` AS `city_name`,`country`.`name` AS `country_name` from (((`user` `u` left join `address` `a` on((`u`.`address_id` = `a`.`address_id`))) left join `city` on((`a`.`city_id` = `city`.`city_id`))) left join `country` on((`city`.`country_id` = `country`.`country_id`))) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `product_view`
--

/*!50001 DROP TABLE IF EXISTS `product_view`*/;
/*!50001 DROP VIEW IF EXISTS `product_view`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8 */;
/*!50001 SET character_set_results     = utf8 */;
/*!50001 SET collation_connection      = utf8_general_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`b5de033d9bb9f7`@`%` SQL SECURITY DEFINER */
/*!50001 VIEW `product_view` AS select `p`.`product_id` AS `product_id`,`p`.`name` AS `name`,`p`.`description` AS `description`,`p`.`price` AS `price`,`p`.`available` AS `available`,`p`.`image` AS `image`,`p`.`added_on` AS `added_on`,`c`.`category_name` AS `category_name`,`s`.`store_name` AS `store_name` from ((`product` `p` join `category` `c` on((`p`.`category_id` = `c`.`category_id`))) join `store` `s` on((`p`.`store_id` = `s`.`store_id`))) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2020-02-01 18:43:30
