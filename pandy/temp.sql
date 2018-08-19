-- MySQL dump 10.13  Distrib 5.7.23, for Linux (x86_64)
--
-- Host: localhost    Database: wechatmovie
-- ------------------------------------------------------
-- Server version	5.7.23-0ubuntu0.16.04.1

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
-- Table structure for table `adarticles`
--

DROP TABLE IF EXISTS `adarticles`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `adarticles` (
  `id` int(8) NOT NULL AUTO_INCREMENT,
  `title` varchar(255) DEFAULT NULL,
  `picurl` varchar(255) DEFAULT NULL,
  `url` varchar(255) DEFAULT NULL,
  `canbeuse` int(1) DEFAULT NULL,
  `tab` int(4) DEFAULT '1',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=141 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `adarticles`
--

LOCK TABLES `adarticles` WRITE;
/*!40000 ALTER TABLE `adarticles` DISABLE KEYS */;
INSERT INTO `adarticles` VALUES (130,'【推荐】他是宇宙杀神渡劫陨落，重生为地球上的废材少爷，这一世注定不平凡…','https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1533933609411&di=f895e906f989f2992f7fe4acf5b93397&imgtype=0&src=http%3A%2F%2Ffile1.3737k.com%2Fnews%2Fday_150121%2F201501211050599655.jpg','https://mp.weixin.qq.com/s/hy4PY_DwfmuXx5S8m0vOxg',1,2),(131,'病人已宣布无救！医学院刚毕业的学生几针下去！竟起死回生了！\n','http://img.ugirls.tv/uploads/mobile/magazine/content/2017/08/25/db81ef5ceee4663ae84007d8437d8254.jpg','https://mp.weixin.qq.com/s/Mk2IScNqIHxAEo6JinhC2g',1,1),(132,'【推荐】为救妹妹神秘部队兵王退伍当保镖，没想到保护的竟然是千金大小姐...\n','http://img.ugirls.tv/uploads/mobile/magazine/content/2017/08/25/c109894671257556d9d073a2384624ce.jpg','https://mp.weixin.qq.com/s/UA0YCAxSRIHjQV8Ezrq8nA',1,2),(133,'【火爆】病人已宣布无救！医学院刚毕业的学生几针下去！竟起死回生了！\n','http://img.ugirls.tv/uploads/mobile/magazine/content/2017/08/25/db81ef5ceee4663ae84007d8437d8254.jpg','https://mp.weixin.qq.com/s/Mk2IScNqIHxAEo6JinhC2g',1,1),(134,'【推荐】他身具两个超强丹田，却被世人称为修仙史上第一废柴……\n','https://mmbiz.qpic.cn/mmbiz_jpg/dZJzfxRLDZiblcWh743uvlP3TA0hEdiahbEmEHU1KpZGG3boPGR6U006kWSnqATO4QBjV2AJ9kNXxJpric55k5YvA/640?wx_fmt=jpeg&tp=webp&wxfrom=5&wx_lazy=1','https://mp.weixin.qq.com/s/WK7c9W7QqkqWmERmmaG7-g',1,1),(135,'【推荐】特种兵回家看见父亲被黑社会殴打、妹妹被欺辱，他一个电话竟......','http://a2.att.hudong.com/37/69/01300000876508134992697520456.jpg','https://mp.weixin.qq.com/s/vpvTNsPmP1cITb2vaK-Myg',1,2),(136,'【推荐】小伙车祸生命垂危，医院不敢医，却被一个实习医生救活了，神了！','https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1534587848927&di=2ce958c55a8033b93339d38d5dc0eade&imgtype=0&src=http%3A%2F%2Fs15.sinaimg.cn%2Fmw690%2F001JxHu5gy6R8eEcvFQ7e%26690','https://mp.weixin.qq.com/s/b9bXt3KEizr6luGe3C73Eg',1,2),(137,'title2','https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1534673543899&di=a750e5917cceda73dce050c9f18102e5&imgtype=0&src=http%3A%2F%2Fimg1qn.moko.cc%2F2016-07-26%2F79726bdb-2247-4db6-ac16-6d170dc48982.jpg%3FimageView2%2F2%2Fw%2F915%2Fh%2F915','http://baddy.com',1,1),(138,'title3','https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1534673543899&di=a750e5917cceda73dce050c9f18102e5&imgtype=0&src=http%3A%2F%2Fimg1qn.moko.cc%2F2016-07-26%2F79726bdb-2247-4db6-ac16-6d170dc48982.jpg%3FimageView2%2F2%2Fw%2F915%2Fh%2F915','http://baiducom',1,2),(139,'title2','https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1534673543899&di=a750e5917cceda73dce050c9f18102e5&imgtype=0&src=http%3A%2F%2Fimg1qn.moko.cc%2F2016-07-26%2F79726bdb-2247-4db6-ac16-6d170dc48982.jpg%3FimageView2%2F2%2Fw%2F915%2Fh%2F915','http://baidu.com',1,1),(140,'title2','https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1534673543899&di=a750e5917cceda73dce050c9f18102e5&imgtype=0&src=http%3A%2F%2Fimg1qn.moko.cc%2F2016-07-26%2F79726bdb-2247-4db6-ac16-6d170dc48982.jpg%3FimageView2%2F2%2Fw%2F915%2Fh%2F915','http://baidu.com',1,1);
/*!40000 ALTER TABLE `adarticles` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2018-08-19 15:58:26
