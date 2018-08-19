-- MySQL dump 10.10
--
-- Host: localhost    Database: shiyan8
-- ------------------------------------------------------
-- Server version	5.0.22-community

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
-- Table structure for table `admin_account`
--

DROP TABLE IF EXISTS `admin_account`;
CREATE TABLE `admin_account` (
  `ACCOUNT_ID` int(4) NOT NULL auto_increment,
  `ACCOUNT_PASSWD` varchar(255) NOT NULL,
  PRIMARY KEY  (`ACCOUNT_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `admin_account`
--


/*!40000 ALTER TABLE `admin_account` DISABLE KEYS */;
LOCK TABLES `admin_account` WRITE;
INSERT INTO `admin_account` VALUES (123,'111'),(124,'222');
UNLOCK TABLES;
/*!40000 ALTER TABLE `admin_account` ENABLE KEYS */;

--
-- Table structure for table `appartus`
--

DROP TABLE IF EXISTS `appartus`;
CREATE TABLE `appartus` (
  `APPARTUS_ID` int(4) NOT NULL,
  `APPARTUS_NAME` varchar(10) default NULL,
  `APPARTUS_PRICE` int(4) default NULL,
  `APPARTUS_QUANTITTY` int(4) default NULL,
  `APPARTUS_REM` varchar(20) default NULL,
  PRIMARY KEY  (`APPARTUS_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `appartus`
--


/*!40000 ALTER TABLE `appartus` DISABLE KEYS */;
LOCK TABLES `appartus` WRITE;
INSERT INTO `appartus` VALUES (8001,'APP 1',3445,45,'REM 1'),(8002,'APP 2',32445,5,'REM 2'),(8004,'APP 4',34445,44,'REM 4');
UNLOCK TABLES;
/*!40000 ALTER TABLE `appartus` ENABLE KEYS */;

--
-- Table structure for table `beds`
--

DROP TABLE IF EXISTS `beds`;
CREATE TABLE `beds` (
  `BED_ID` int(4) NOT NULL auto_increment,
  `BED_STATE` int(1) NOT NULL,
  PRIMARY KEY  (`BED_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `beds`
--


/*!40000 ALTER TABLE `beds` DISABLE KEYS */;
LOCK TABLES `beds` WRITE;
INSERT INTO `beds` VALUES (1,0),(2,0),(3,1),(5,1);
UNLOCK TABLES;
/*!40000 ALTER TABLE `beds` ENABLE KEYS */;

--
-- Table structure for table `dept`
--

DROP TABLE IF EXISTS `dept`;
CREATE TABLE `dept` (
  `DEPT_ID` int(4) NOT NULL auto_increment,
  `DEPT_NAME` varchar(10) NOT NULL,
  `DEPT_MANAGER` int(4) NOT NULL,
  `DEPT_VICEMANAGER` int(4) NOT NULL,
  PRIMARY KEY  (`DEPT_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `dept`
--


/*!40000 ALTER TABLE `dept` DISABLE KEYS */;
LOCK TABLES `dept` WRITE;
INSERT INTO `dept` VALUES (1,'DEPT 1',1001,2001),(2,'DEPT 2',1002,2002),(4,'DEPT 4',1004,2004);
UNLOCK TABLES;
/*!40000 ALTER TABLE `dept` ENABLE KEYS */;

--
-- Table structure for table `job`
--

DROP TABLE IF EXISTS `job`;
CREATE TABLE `job` (
  `JOB_ID` int(4) NOT NULL auto_increment,
  `DEPT_ID` int(4) NOT NULL,
  `JOB_NAME` varchar(10) NOT NULL,
  PRIMARY KEY  (`JOB_ID`),
  KEY `DEPT_ID` (`DEPT_ID`),
  CONSTRAINT `job_ibfk_1` FOREIGN KEY (`DEPT_ID`) REFERENCES `dept` (`DEPT_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `job`
--


/*!40000 ALTER TABLE `job` DISABLE KEYS */;
LOCK TABLES `job` WRITE;
INSERT INTO `job` VALUES (1,1,'JOB 1'),(2,2,'JOB 2'),(3,4,'JOB 4');
UNLOCK TABLES;
/*!40000 ALTER TABLE `job` ENABLE KEYS */;

--
-- Table structure for table `menzhen`
--

DROP TABLE IF EXISTS `menzhen`;
CREATE TABLE `menzhen` (
  `MENZHEN_ID` int(4) NOT NULL auto_increment,
  `MENZHEN_NAME` varchar(20) NOT NULL,
  PRIMARY KEY  (`MENZHEN_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `menzhen`
--


/*!40000 ALTER TABLE `menzhen` DISABLE KEYS */;
LOCK TABLES `menzhen` WRITE;
INSERT INTO `menzhen` VALUES (1,'MENZHEN 1'),(3,'MENZHEN 3'),(4,'MENZHEN 4'),(6,'MENZHEN 6');
UNLOCK TABLES;
/*!40000 ALTER TABLE `menzhen` ENABLE KEYS */;

--
-- Table structure for table `patient`
--

DROP TABLE IF EXISTS `patient`;
CREATE TABLE `patient` (
  `PATIENT_NAME` varchar(10) NOT NULL,
  `PATIENT_GENDER` int(1) NOT NULL,
  `PATIENT_DATE_START` varchar(20) NOT NULL,
  `PATIENT_DEPT` int(4) NOT NULL,
  `PATIENT_STATE` varchar(10) NOT NULL,
  `PATIENT_DOC` int(4) NOT NULL,
  `PATIENT_ROOM` int(4) NOT NULL,
  `PATIENT_BED` int(4) NOT NULL,
  PRIMARY KEY  (`PATIENT_NAME`),
  KEY `PATIENT_DOC` (`PATIENT_DOC`),
  KEY `PATIENT_BED` (`PATIENT_BED`),
  CONSTRAINT `patient_ibfk_1` FOREIGN KEY (`PATIENT_DOC`) REFERENCES `personnel` (`EMP_NO`),
  CONSTRAINT `patient_ibfk_2` FOREIGN KEY (`PATIENT_BED`) REFERENCES `beds` (`BED_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `patient`
--


/*!40000 ALTER TABLE `patient` DISABLE KEYS */;
LOCK TABLES `patient` WRITE;
UNLOCK TABLES;
/*!40000 ALTER TABLE `patient` ENABLE KEYS */;

--
-- Table structure for table `personnel`
--

DROP TABLE IF EXISTS `personnel`;
CREATE TABLE `personnel` (
  `EMP_NO` int(4) NOT NULL auto_increment,
  `EMP_NAME` varchar(10) NOT NULL,
  `EMP_DEPT_ID` int(4) default NULL,
  `EMP_DUTY` varchar(10) default NULL,
  `EMP_XL` varchar(10) default NULL,
  `EMP_GENDER` int(1) default NULL,
  `EMP_BIRTHDAY` varchar(20) default NULL,
  `EMP_HOMETOWN` varchar(50) default NULL,
  `EMP_COUNTRY` varchar(50) default NULL,
  `EMP_NATION` varchar(50) default NULL,
  `EMP_ID` int(20) NOT NULL,
  `EMP_MARRIAGE` int(1) default NULL,
  `EMP_HEALTH` varchar(10) default NULL,
  `EMP_STARTWORK` varchar(20) default NULL,
  `EMP_STATE` varchar(10) default NULL,
  `EMP_HOMEADDRESS` varchar(50) default NULL,
  `EMP_TELENO` int(20) default NULL,
  `EMP_EMAIL` varchar(20) default NULL,
  `EMP_JOB_ID` int(4) default NULL,
  PRIMARY KEY  (`EMP_NO`),
  KEY `EMP_JOB_ID` (`EMP_JOB_ID`),
  CONSTRAINT `personnel_ibfk_1` FOREIGN KEY (`EMP_JOB_ID`) REFERENCES `dept` (`DEPT_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `personnel`
--


/*!40000 ALTER TABLE `personnel` DISABLE KEYS */;
LOCK TABLES `personnel` WRITE;
INSERT INTO `personnel` VALUES (4001,'EMP 1',4,'DUTY 1','XUE LI 1',1,'2018.01.10','HU NAN','CHINA','HAN',2147483647,0,'HEN HAO','2019.01.01','HAI XING','KEJI DAXUE',2147483647,'2342@QQ.COM',1),(4003,'EMP 1',5,'DUTY 13','XUE LI 1',1,'2018.01.13','HU NAN','CHINA','HAN',2147483647,0,'HEN HAO','2019.01.31','HAI XING','KEJI DAXUE',2147483647,'232442@QQ.COM',4);
UNLOCK TABLES;
/*!40000 ALTER TABLE `personnel` ENABLE KEYS */;

--
-- Table structure for table `potion`
--

DROP TABLE IF EXISTS `potion`;
CREATE TABLE `potion` (
  `POTION_ID` int(4) NOT NULL,
  `POTION_NAME` varchar(10) NOT NULL,
  `POTION_PRICE` int(4) default NULL,
  `POTION_QUANTITY` int(4) default NULL,
  `POTION_REM` varchar(20) default NULL,
  PRIMARY KEY  (`POTION_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `potion`
--


/*!40000 ALTER TABLE `potion` DISABLE KEYS */;
LOCK TABLES `potion` WRITE;
INSERT INTO `potion` VALUES (7001,'POTION 1',3455,32,'REM 1'),(7003,'POTION 3',34455,332,'REM 3'),(7004,'POTION 4',344455,3432,'REM 4');
UNLOCK TABLES;
/*!40000 ALTER TABLE `potion` ENABLE KEYS */;

--
-- Table structure for table `salary`
--

DROP TABLE IF EXISTS `salary`;
CREATE TABLE `salary` (
  `HUMAN_NO` int(4) NOT NULL auto_increment,
  `SALARY` int(4) default NULL,
  PRIMARY KEY  (`HUMAN_NO`),
  CONSTRAINT `salary_ibfk_1` FOREIGN KEY (`HUMAN_NO`) REFERENCES `personnel` (`EMP_NO`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `salary`
--


/*!40000 ALTER TABLE `salary` DISABLE KEYS */;
LOCK TABLES `salary` WRITE;
INSERT INTO `salary` VALUES (4001,9879),(4003,4533);
UNLOCK TABLES;
/*!40000 ALTER TABLE `salary` ENABLE KEYS */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

