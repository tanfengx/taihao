/*
SQLyog Community v13.2.0 (64 bit)
MySQL - 8.0.12 : Database - db_onlinebicyclesales_sys
*********************************************************************
*/

/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
CREATE DATABASE /*!32312 IF NOT EXISTS*/`db_onlinebicyclesales_sys` /*!40100 DEFAULT CHARACTER SET utf8 */;

USE `db_onlinebicyclesales_sys`;

/*Table structure for table `address` */

DROP TABLE IF EXISTS `address`;

CREATE TABLE `address` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '收货地址编号',
  `name` varchar(100) DEFAULT NULL COMMENT '姓名',
  `phone` varchar(100) DEFAULT NULL COMMENT '手机',
  `address` varchar(200) DEFAULT NULL COMMENT '详细地址',
  `postcode` varchar(100) DEFAULT NULL COMMENT '邮编',
  `user_id` int(11) DEFAULT NULL COMMENT '用户编号',
  `default_radio` varchar(10) DEFAULT NULL COMMENT '是否默认',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=11 DEFAULT CHARSET=utf8 COMMENT='收货地址';

/*Data for the table `address` */

insert  into `address`(`id`,`name`,`phone`,`address`,`postcode`,`user_id`,`default_radio`) values 
(9,'张三','13211112222','广州天河','510000',38,'是'),
(10,'张三丰','13255556666','广州番禺','521111',38,'否');

/*Table structure for table `banner` */

DROP TABLE IF EXISTS `banner`;

CREATE TABLE `banner` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '轮播图编号',
  `img` varchar(200) DEFAULT NULL COMMENT '图片',
  `url` varchar(200) DEFAULT NULL COMMENT '链接地址',
  `index_radio` varchar(20) DEFAULT NULL COMMENT '是否首页',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=14 DEFAULT CHARSET=utf8 COMMENT='轮播图';

/*Data for the table `banner` */

insert  into `banner`(`id`,`img`,`url`,`index_radio`) values 
(11,'http://localhost:9090/media/e8017cac-fbb2-42f3-95b9-d8d5d4b0d0a0.png',NULL,'是'),
(12,'http://localhost:9090/media/46725756-396b-474d-a73c-61e162a5b1da.png',NULL,'是'),
(13,'http://localhost:9090/media/a058e09e-a4cf-49ec-a375-8b45aff08145.png',NULL,'否');

/*Table structure for table `business` */

DROP TABLE IF EXISTS `business`;

CREATE TABLE `business` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '编号',
  `username` varchar(200) DEFAULT NULL COMMENT '登录账号',
  `name` varchar(200) DEFAULT NULL COMMENT '商家名称',
  `user_id` int(11) DEFAULT NULL COMMENT '所属用户',
  `phone` varchar(200) DEFAULT NULL COMMENT '联系电话',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=9 DEFAULT CHARSET=utf8 COMMENT='商家';

/*Data for the table `business` */

insert  into `business`(`id`,`username`,`name`,`user_id`,`phone`) values 
(7,'小锋','小锋',39,NULL),
(8,'小胖','小胖',40,NULL);

/*Table structure for table `cart` */

DROP TABLE IF EXISTS `cart`;

CREATE TABLE `cart` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '购物车编号',
  `user_id` int(11) DEFAULT NULL COMMENT '购买用户',
  `name` varchar(200) DEFAULT NULL COMMENT '购买商品',
  `num` int(11) DEFAULT NULL COMMENT '数量',
  `price` double DEFAULT NULL COMMENT '单价',
  `img` varchar(200) DEFAULT NULL COMMENT '商品图片',
  `biz_user_id` int(11) DEFAULT NULL COMMENT '商家',
  `goodid` int(11) DEFAULT NULL COMMENT '产品编号',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=14 DEFAULT CHARSET=utf8 COMMENT='购物车';

/*Data for the table `cart` */

/*Table structure for table `category` */

DROP TABLE IF EXISTS `category`;

CREATE TABLE `category` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '编号',
  `name` varchar(200) DEFAULT NULL COMMENT '分类名称',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=17 DEFAULT CHARSET=utf8 COMMENT='商品分类';

/*Data for the table `category` */

insert  into `category`(`id`,`name`) values 
(13,'山地车'),
(14,'公路车'),
(15,'折叠车'),
(16,'穿戴装备');

/*Table structure for table `collect` */

DROP TABLE IF EXISTS `collect`;

CREATE TABLE `collect` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '编号',
  `user_id` int(11) DEFAULT NULL COMMENT '用户',
  `goods_id` int(11) DEFAULT NULL COMMENT '商品',
  `create_time` datetime DEFAULT NULL COMMENT '创建时间',
  `update_time` datetime DEFAULT NULL COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `unique_key` (`user_id`,`goods_id`)
) ENGINE=MyISAM AUTO_INCREMENT=4 DEFAULT CHARSET=utf8 COMMENT='商品收藏';

/*Data for the table `collect` */

insert  into `collect`(`id`,`user_id`,`goods_id`,`create_time`,`update_time`) values 
(3,38,18,'2025-01-25 15:41:45','2025-01-25 15:41:45');

/*Table structure for table `comments` */

DROP TABLE IF EXISTS `comments`;

CREATE TABLE `comments` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '评论编号',
  `content` text CHARACTER SET utf8 COLLATE utf8_general_ci COMMENT '评论内容',
  `create_time` datetime DEFAULT NULL COMMENT '添加时间',
  `update_time` datetime DEFAULT NULL COMMENT '修改时间',
  `user_id` int(11) DEFAULT NULL COMMENT '用户',
  `goods_id` int(11) DEFAULT NULL COMMENT '商品编号',
  `pid` int(11) DEFAULT NULL COMMENT '父评论ID',
  `puser_id` int(11) DEFAULT NULL COMMENT '父级用户ID',
  `score` int(11) DEFAULT NULL COMMENT '评论星级',
  `orders_id` int(11) DEFAULT NULL COMMENT '订单编号',
  `biz_user_id` int(11) DEFAULT NULL COMMENT '商家编号',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=19 DEFAULT CHARSET=utf8 COMMENT='商品评论';

/*Data for the table `comments` */

insert  into `comments`(`id`,`content`,`create_time`,`update_time`,`user_id`,`goods_id`,`pid`,`puser_id`,`score`,`orders_id`,`biz_user_id`) values 
(16,'6666','2024-12-10 11:57:33','2024-12-10 11:57:33',38,18,NULL,NULL,5,9,39),
(17,'非常不错的自行车！','2025-01-25 15:41:27','2025-01-25 15:41:27',38,18,NULL,NULL,5,10,39),
(18,'谢谢您的支持！','2025-01-25 15:49:54','2025-01-25 15:49:54',39,18,17,38,NULL,NULL,NULL);

/*Table structure for table `dict` */

DROP TABLE IF EXISTS `dict`;

CREATE TABLE `dict` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '编号',
  `code` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '编码',
  `value` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '内容',
  `type` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '类型',
  `deleted` int(11) DEFAULT '0' COMMENT '删除',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE KEY `c_d` (`code`,`deleted`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=20 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci ROW_FORMAT=DYNAMIC COMMENT='数据字典';

/*Data for the table `dict` */

insert  into `dict`(`id`,`code`,`value`,`type`,`deleted`) values 
(2,'message','message','icon',0),
(3,'menu','menu','icon',0),
(4,'grid','grid','icon',0),
(5,'house','house','icon',0),
(6,'user','user','icon',0),
(7,'file','files','icon',0),
(8,'money','money','icon',0),
(9,'school','school','icon',0),
(10,'notebook','notebook','icon',0),
(11,'coin','coin','icon',0),
(12,'set-up','set-up','icon',0),
(13,'postcard','postcard','icon',0),
(14,'food','food','icon',0),
(15,'position','position','icon',0),
(16,'chat-line-round','chat-line-round','icon',0),
(17,'chat-dot-round','chat-dot-round','icon',0),
(18,'setting','setting','icon',0),
(19,'comment','comment','icon',0);

/*Table structure for table `goods` */

DROP TABLE IF EXISTS `goods`;

CREATE TABLE `goods` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '编号',
  `category_id` int(11) DEFAULT NULL COMMENT '商品分类',
  `name` varchar(200) DEFAULT NULL COMMENT '商品名称',
  `img` varchar(200) DEFAULT NULL COMMENT '图片',
  `content` text COMMENT '详情',
  `price` double DEFAULT NULL COMMENT '价格',
  `create_time` datetime DEFAULT NULL COMMENT '发布时间',
  `user_id` int(11) DEFAULT NULL COMMENT '发布商家',
  `views` int(11) DEFAULT '0' COMMENT '浏览量',
  `state_radio` varchar(200) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT '审核中' COMMENT '状态,审核中|审核成功|审核失败',
  `remarks` varchar(200) DEFAULT NULL COMMENT '审核说明',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=19 DEFAULT CHARSET=utf8 COMMENT='商品';

/*Data for the table `goods` */

insert  into `goods`(`id`,`category_id`,`name`,`img`,`content`,`price`,`create_time`,`user_id`,`views`,`state_radio`,`remarks`) values 
(14,16,'匹克骑行头盔自行车头盔','http://localhost:9090/media/8b63142f-9d0d-44ff-8056-f35858aaaba8.png','<p style=\"text-align: center;\"><img src=\"http://localhost:9090/media/e2e7d0a6-d84f-4e4c-9439-a2b36b1a0054.png\" alt=\"\" data-href=\"\" style=\"width: 50%;\"></p>',58.9,'2024-12-10 10:24:02',39,2,'审核成功',NULL),
(15,14,'百士盾死飞自行车','http://localhost:9090/media/e681904d-4e41-4a79-9784-31560bc57dac.png','<p style=\"text-align: center;\"><img src=\"http://localhost:9090/media/2d0924d8-5af5-441e-b260-92ff78c72c6a.png\" alt=\"\" data-href=\"\" style=\"width: 50%;\"></p>',299,'2024-12-10 10:25:10',39,6,'审核成功',NULL),
(16,14,'永久MT210破风型弯把公路自行车','http://localhost:9090/media/49ddc178-4961-43e9-9baf-f7010d2ccd4d.png','<p style=\"text-align: center;\"><img src=\"http://localhost:9090/media/c1401f1b-403d-4342-aaae-370a28c66857.png\" alt=\"\" data-href=\"\" style=\"width: 50%;\"></p>',388,'2024-12-10 10:49:04',39,12,'审核成功',NULL),
(17,13,'百士盾儿童自行车山地单车','http://localhost:9090/media/2bada69d-d13d-4ac4-a28b-34086ffcc197.png','<p style=\"text-align: center;\"><img src=\"http://localhost:9090/media/d03493a7-8061-4736-9d5e-d1e36acb166a.png\" alt=\"\" data-href=\"\" style=\"width: 50%;\"></p>',208,'2024-12-10 10:52:40',39,5,'审核成功',NULL),
(18,13,'山地自行车越客MX1成人学生山地车','http://localhost:9090/media/54186977-d11c-4b12-b20f-dd93d9dbb410.png','<p style=\"text-align: center;\"><img src=\"http://localhost:9090/media/dc985b17-794a-4b3f-b542-ad40d6b1e55a.png\" alt=\"\" data-href=\"\" style=\"width: 50%;\"><img src=\"http://localhost:9090/media/bd69fd9e-1340-4c4a-b1eb-686648cdbaf9.png\" alt=\"\" data-href=\"\" style=\"\"></p>',999,'2024-12-10 10:53:38',39,37,'审核成功',NULL);

/*Table structure for table `member` */

DROP TABLE IF EXISTS `member`;

CREATE TABLE `member` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '编号',
  `username` varchar(200) DEFAULT NULL COMMENT '用户名',
  `name` varchar(200) DEFAULT NULL COMMENT '姓名',
  `user_id` int(11) DEFAULT NULL COMMENT '所属用户',
  `isvip` varchar(200) DEFAULT NULL COMMENT '是否会员',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=5 DEFAULT CHARSET=utf8 COMMENT='用户';

/*Data for the table `member` */

insert  into `member`(`id`,`username`,`name`,`user_id`,`isvip`) values 
(4,'zhangsan','张三',38,'否');

/*Table structure for table `notice` */

DROP TABLE IF EXISTS `notice`;

CREATE TABLE `notice` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '编号',
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '名称',
  `content` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci COMMENT '内容',
  `create_time` datetime DEFAULT NULL COMMENT '创建时间',
  `user_id` int(11) DEFAULT NULL COMMENT '创建人id',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci ROW_FORMAT=DYNAMIC COMMENT='系统公告';

/*Data for the table `notice` */

insert  into `notice`(`id`,`name`,`content`,`create_time`,`user_id`) values 
(19,'春季大促，自行车全场8折优惠！','<p style=\"text-align: start;\">亲爱的顾客朋友们，</p><p style=\"text-align: start;\">随着春季的到来，为了让大家更好地享受户外骑行的乐趣，我们网站决定在本周五至下周日（日期范围）举办春季大促活动。活动期间，全场自行车享受8折优惠！无论您是寻找城市通勤车、山地车还是公路车，我们都有丰富款式供您选择。</p><p style=\"text-align: start;\">此外，购买任意自行车还将赠送价值100元的骑行配件礼包一份，数量有限，先到先得。快来选购心仪的自行车，一起迎接充满活力的春天吧！</p><p style=\"text-align: start;\">如有任何疑问，欢迎随时联系我们的客服团队，我们将竭诚为您服务。</p><p style=\"text-align: start;\">祝您骑行愉快！</p>','2025-01-25 14:56:08',1),
(20,'新品上市！探索系列山地车正式发布！','<p style=\"text-align: start;\">各位骑行爱好者们，</p><p style=\"text-align: start;\">我们很高兴地宣布，经过长时间的研发与测试，探索系列山地车现已正式上线！该系列山地车采用全新轻量化材料，搭载先进的悬挂系统和变速系统，能够轻松应对各种复杂地形，带给您极致的骑行体验。</p><p style=\"text-align: start;\">探索系列山地车不仅性能卓越，外观设计也非常时尚，是户外探险和城市骑行的理想选择。现在下单购买，还将享受限时9折优惠，并有机会获得限量版骑行背包一个。</p><p style=\"text-align: start;\">立即访问我们的网站，了解更多关于探索系列山地车的详细信息，开启您的全新骑行之旅！</p>','2025-01-25 14:56:22',1),
(21,'网站维护通知，短暂暂停服务','<p style=\"text-align: start;\">尊敬的顾客们，</p><p style=\"text-align: start;\">为了提升网站性能和购物体验，我们计划于（具体日期）的（具体时间范围）进行系统维护和升级。在此期间，网站将暂时无法访问。</p><p style=\"text-align: start;\">我们深知此次维护可能会给您带来不便，对此我们深表歉意。请您放心，我们会尽快完成维护工作，确保网站恢复正常运行。</p><p style=\"text-align: start;\">在维护期间，如有任何紧急需求或疑问，您可以通过我们的客服热线（电话号码）或电子邮件（邮箱地址）与我们联系，我们将尽力为您提供帮助。</p><p style=\"text-align: start;\">感谢您对我们网站的理解与支持，期待在维护完成后继续为您提供优质的自行车销售服务。</p><p style=\"text-align: start;\">祝您生活愉快！</p>','2025-01-25 14:56:35',1);

/*Table structure for table `orders` */

DROP TABLE IF EXISTS `orders`;

CREATE TABLE `orders` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '订单编号',
  `name` varchar(100) DEFAULT NULL COMMENT '订单号',
  `content` text COMMENT '订单明细',
  `state_radio` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL COMMENT '订单状态,已下单|已发货|已收货|已评价|已取消',
  `user_id` int(11) DEFAULT NULL COMMENT '下单用户',
  `amount` double DEFAULT NULL COMMENT '总金额',
  `create_time` datetime DEFAULT NULL COMMENT '下单时间',
  `update_time` datetime DEFAULT NULL COMMENT '更新时间',
  `biz_user_id` int(11) DEFAULT NULL COMMENT '商户',
  `goodids` varchar(100) DEFAULT NULL COMMENT '产品编号',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=14 DEFAULT CHARSET=utf8 COMMENT='订单';

/*Data for the table `orders` */

insert  into `orders`(`id`,`name`,`content`,`state_radio`,`user_id`,`amount`,`create_time`,`update_time`,`biz_user_id`,`goodids`) values 
(10,'20250125154019','收货地址：张三，13211112222，广州天河<br/>支付方式：微信支付<br/>商品明细：<br/><ul><li>商品：山地自行车越客MX1成人学生山地车，数量：1，单价：999</li></ul>','已评价',38,999,'2025-01-25 15:40:20','2025-01-25 15:41:27',39,'18'),
(11,'20250125161342','收货地址：张三，13211112222，广州天河<br/>支付方式：微信支付<br/>商品明细：<br/><ul><li>商品：山地自行车越客MX1成人学生山地车，数量：1，单价：999</li></ul>','已下单',38,899.1,'2025-01-25 16:13:43','2025-01-25 16:13:43',39,'18'),
(12,'20250125161622','收货地址：张三，13211112222，广州天河<br/>支付方式：微信支付<br/>商品明细：<br/><ul><li>商品：永久MT210破风型弯把公路自行车，数量：1，单价：388</li></ul>','已下单',38,349.2,'2025-01-25 16:16:22','2025-01-25 16:16:22',39,'16'),
(13,'20250125161703','收货地址：张三，13211112222，广州天河<br/>支付方式：微信支付<br/>商品明细：<br/><ul><li>商品：百士盾死飞自行车，数量：1，单价：299</li></ul>','已下单',38,299,'2025-01-25 16:17:04','2025-01-25 16:17:04',39,'15');

/*Table structure for table `paytype` */

DROP TABLE IF EXISTS `paytype`;

CREATE TABLE `paytype` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '方式编号',
  `name` varchar(50) DEFAULT NULL COMMENT '支付名称',
  `img` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL COMMENT '二维码',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=3 DEFAULT CHARSET=utf8 COMMENT='支付方式';

/*Data for the table `paytype` */

insert  into `paytype`(`id`,`name`,`img`) values 
(1,'微信支付','http://localhost:9090/media/cb97f1b9-dead-41a1-bdbe-033136c9f379.png'),
(2,'支付宝','http://localhost:9090/media/3c2af067-7e70-4f6a-a426-c4a5abea85af.png');

/*Table structure for table `permission` */

DROP TABLE IF EXISTS `permission`;

CREATE TABLE `permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '编号',
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '名称',
  `path` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '路径',
  `orders` int(11) DEFAULT '1' COMMENT '顺序',
  `icon` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT 'grid' COMMENT '图标',
  `page` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '页面路径',
  `auth` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '权限',
  `p_id` int(11) DEFAULT NULL COMMENT '父级id',
  `deleted` int(11) DEFAULT '0' COMMENT '逻辑删除',
  `create_time` datetime DEFAULT NULL COMMENT '创建时间',
  `update_time` datetime DEFAULT NULL COMMENT '更新时间',
  `type` int(11) DEFAULT NULL COMMENT '类型',
  `hide` tinyint(1) DEFAULT '0' COMMENT '是否隐藏',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE KEY `a_d_index` (`auth`,`deleted`) USING BTREE,
  UNIQUE KEY `p_p_d_index` (`path`,`page`,`deleted`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=785 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci ROW_FORMAT=DYNAMIC COMMENT='权限';

/*Data for the table `permission` */

insert  into `permission`(`id`,`name`,`path`,`orders`,`icon`,`page`,`auth`,`p_id`,`deleted`,`create_time`,`update_time`,`type`,`hide`) values 
(1,'系统管理','',2,'menu',NULL,NULL,NULL,0,'2023-01-16 20:45:51','2023-01-16 20:45:51',1,0),
(3,'用户管理','user',1,'user','User','user.list',1,0,'2023-01-16 20:45:51','2023-08-16 23:06:21',2,0),
(4,'用户新增','',1,NULL,'','user.add',3,0,'2023-01-16 20:45:51','2023-01-16 20:45:51',3,0),
(8,'用户编辑','',1,NULL,NULL,'user.edit',3,0,NULL,'2023-01-28 11:45:21',3,0),
(9,'用户删除',NULL,1,NULL,NULL,'user.delete',3,0,'2023-01-29 11:04:15','2023-01-29 11:04:15',3,0),
(10,'角色管理','role',1,'grid','Role','role.list',1,0,'2023-01-31 20:32:59','2023-01-31 20:32:59',2,0),
(11,'权限管理','permission',1,'position','Permission','permission.list',1,0,'2023-01-31 20:33:25','2023-08-16 23:05:29',2,0),
(12,'首页','home',1,'house','Home',NULL,NULL,0,'2023-01-31 21:03:00','2023-01-31 21:03:00',2,0),
(13,'数据字典管理','dict',1,'set-up','Dict','dict.list',1,0,'2023-02-02 20:41:32','2023-08-16 23:32:18',2,0),
(14,'批量删除',NULL,1,'',NULL,'user.deleteBatch',3,0,'2023-02-02 22:32:22','2023-02-02 22:32:22',3,0),
(16,'用户导出',NULL,1,NULL,NULL,'user.export',3,0,'2023-02-02 22:33:08','2023-02-02 22:33:08',3,0),
(21,'角色新增',NULL,1,NULL,'','role.add',10,0,'2023-01-16 20:45:51','2023-01-16 20:45:51',3,0),
(22,'角色编辑',NULL,1,NULL,NULL,'role.edit',10,0,NULL,'2023-01-28 11:45:21',3,0),
(23,'角色删除',NULL,1,NULL,NULL,'role.delete',10,0,'2023-01-29 11:04:15','2023-01-29 11:04:15',3,0),
(25,'批量删除',NULL,1,NULL,NULL,'role.deleteBatch',10,0,'2023-02-02 22:32:22','2023-02-02 22:32:22',3,0),
(27,'角色导出',NULL,1,NULL,NULL,'role.export',10,0,'2023-02-02 22:33:08','2023-02-02 22:33:08',3,0),
(30,'权限新增',NULL,1,NULL,'','permission.add',11,0,'2023-01-16 20:45:51','2023-01-16 20:45:51',3,0),
(31,'权限编辑',NULL,1,NULL,NULL,'permission.edit',11,0,NULL,'2023-01-28 11:45:21',3,0),
(32,'权限删除',NULL,1,NULL,NULL,'permission.delete',11,0,'2023-01-29 11:04:15','2023-01-29 11:04:15',3,0),
(35,'权限导出',NULL,1,NULL,NULL,'permission.export',11,0,'2023-02-02 22:33:08','2023-02-02 22:33:08',3,0),
(37,'数据字典新增',NULL,1,NULL,'','dict.add',13,0,'2023-01-16 20:45:51','2023-01-16 20:45:51',3,0),
(38,'数据字典编辑',NULL,1,NULL,NULL,'dict.edit',13,0,NULL,'2023-01-28 11:45:21',3,0),
(39,'数据字典删除',NULL,1,NULL,NULL,'dict.delete',13,0,'2023-01-29 11:04:15','2023-01-29 11:04:15',3,0),
(40,'批量删除',NULL,1,NULL,NULL,'dict.deleteBatch',13,0,'2023-02-02 22:32:22','2023-02-02 22:32:22',3,0),
(42,'数据字典导出',NULL,1,NULL,NULL,'dict.export',13,0,'2023-02-02 22:33:08','2023-02-02 22:33:08',3,0),
(505,'平台公告','notice',1,'comment','Notice',NULL,NULL,0,NULL,'2024-12-10 10:19:59',2,0),
(506,'公告查询',NULL,1,'grid',NULL,'notice.list',505,0,NULL,'2023-08-14 16:28:13',3,0),
(507,'公告新增',NULL,1,'grid',NULL,'notice.add',505,0,NULL,'2023-08-14 16:28:16',3,0),
(509,'公告导出',NULL,1,'grid',NULL,'notice.export',505,0,NULL,NULL,3,0),
(510,'批量删除',NULL,1,'grid',NULL,'notice.deleteBatch',505,0,NULL,NULL,3,0),
(511,'公告编辑',NULL,1,'grid',NULL,'notice.edit',505,0,NULL,NULL,3,0),
(512,'公告删除',NULL,1,'grid',NULL,'notice.delete',505,0,NULL,NULL,3,0),
(700,'用户管理','member',1,'grid','Member',NULL,NULL,0,NULL,NULL,2,0),
(701,'用户查询',NULL,1,'grid',NULL,'member.list',700,0,NULL,NULL,3,0),
(702,'用户新增',NULL,1,'grid',NULL,'member.add',700,0,NULL,NULL,3,0),
(703,'用户导出',NULL,1,'grid',NULL,'member.export',700,0,NULL,NULL,3,0),
(704,'批量删除',NULL,1,'grid',NULL,'member.deleteBatch',700,0,NULL,NULL,3,0),
(705,'用户编辑',NULL,1,'grid',NULL,'member.edit',700,0,NULL,NULL,3,0),
(706,'用户删除',NULL,1,'grid',NULL,'member.delete',700,0,NULL,NULL,3,0),
(707,'商家管理','business',1,'grid','Business',NULL,NULL,0,NULL,NULL,2,0),
(708,'商家查询',NULL,1,'grid',NULL,'business.list',707,0,NULL,NULL,3,0),
(709,'商家新增',NULL,1,'grid',NULL,'business.add',707,0,NULL,NULL,3,0),
(710,'商家导出',NULL,1,'grid',NULL,'business.export',707,0,NULL,NULL,3,0),
(711,'批量删除',NULL,1,'grid',NULL,'business.deleteBatch',707,0,NULL,NULL,3,0),
(712,'商家编辑',NULL,1,'grid',NULL,'business.edit',707,0,NULL,NULL,3,0),
(713,'商家删除',NULL,1,'grid',NULL,'business.delete',707,0,NULL,NULL,3,0),
(714,'商品分类管理','category',1,'grid','Category',NULL,NULL,0,NULL,NULL,2,0),
(715,'商品分类查询',NULL,1,'grid',NULL,'category.list',714,0,NULL,NULL,3,0),
(716,'商品分类新增',NULL,1,'grid',NULL,'category.add',714,0,NULL,NULL,3,0),
(717,'商品分类导出',NULL,1,'grid',NULL,'category.export',714,0,NULL,NULL,3,0),
(718,'批量删除',NULL,1,'grid',NULL,'category.deleteBatch',714,0,NULL,NULL,3,0),
(719,'商品分类编辑',NULL,1,'grid',NULL,'category.edit',714,0,NULL,NULL,3,0),
(720,'商品分类删除',NULL,1,'grid',NULL,'category.delete',714,0,NULL,NULL,3,0),
(721,'自行车商品管理','goods',1,'grid','Goods',NULL,NULL,0,NULL,'2025-01-25 15:07:06',2,0),
(722,'商品查询',NULL,1,'grid',NULL,'goods.list',721,0,NULL,NULL,3,0),
(723,'商品新增',NULL,1,'grid',NULL,'goods.add',721,0,NULL,NULL,3,0),
(724,'商品导出',NULL,1,'grid',NULL,'goods.export',721,0,NULL,NULL,3,0),
(725,'批量删除',NULL,1,'grid',NULL,'goods.deleteBatch',721,0,NULL,NULL,3,0),
(726,'商品编辑',NULL,1,'grid',NULL,'goods.edit',721,0,NULL,NULL,3,0),
(727,'商品删除',NULL,1,'grid',NULL,'goods.delete',721,0,NULL,NULL,3,0),
(728,'购物车管理','cart',1,'grid','Cart',NULL,NULL,0,NULL,'2025-01-25 15:13:56',2,1),
(729,'购物车查询',NULL,1,'grid',NULL,'cart.list',728,0,NULL,NULL,3,0),
(730,'购物车新增',NULL,1,'grid',NULL,'cart.add',728,0,NULL,NULL,3,0),
(731,'购物车导出',NULL,1,'grid',NULL,'cart.export',728,0,NULL,NULL,3,0),
(732,'批量删除',NULL,1,'grid',NULL,'cart.deleteBatch',728,0,NULL,NULL,3,0),
(733,'购物车编辑',NULL,1,'grid',NULL,'cart.edit',728,0,NULL,NULL,3,0),
(734,'购物车删除',NULL,1,'grid',NULL,'cart.delete',728,0,NULL,NULL,3,0),
(735,'订单评论管理','comments',1,'grid','Comments',NULL,NULL,0,NULL,NULL,2,0),
(736,'订单评论查询',NULL,1,'grid',NULL,'comments.list',735,0,NULL,NULL,3,0),
(737,'订单评论新增',NULL,1,'grid',NULL,'comments.add',735,0,NULL,NULL,3,0),
(738,'订单评论导出',NULL,1,'grid',NULL,'comments.export',735,0,NULL,NULL,3,0),
(739,'批量删除',NULL,1,'grid',NULL,'comments.deleteBatch',735,0,NULL,NULL,3,0),
(740,'订单评论编辑',NULL,1,'grid',NULL,'comments.edit',735,0,NULL,NULL,3,0),
(741,'订单评论删除',NULL,1,'grid',NULL,'comments.delete',735,0,NULL,NULL,3,0),
(742,'自行车订单管理','orders',1,'grid','Orders',NULL,NULL,0,NULL,'2025-01-25 15:07:13',2,0),
(743,'农产品订单查询',NULL,1,'grid',NULL,'orders.list',742,0,NULL,NULL,3,0),
(744,'农产品订单新增',NULL,1,'grid',NULL,'orders.add',742,0,NULL,NULL,3,0),
(745,'农产品订单导出',NULL,1,'grid',NULL,'orders.export',742,0,NULL,NULL,3,0),
(746,'批量删除',NULL,1,'grid',NULL,'orders.deleteBatch',742,0,NULL,NULL,3,0),
(747,'农产品订单编辑',NULL,1,'grid',NULL,'orders.edit',742,0,NULL,NULL,3,0),
(748,'农产品订单删除',NULL,1,'grid',NULL,'orders.delete',742,0,NULL,NULL,3,0),
(749,'支付方式管理','paytype',1,'grid','Paytype',NULL,NULL,0,NULL,NULL,2,0),
(750,'支付方式查询',NULL,1,'grid',NULL,'paytype.list',749,0,NULL,NULL,3,0),
(751,'支付方式新增',NULL,1,'grid',NULL,'paytype.add',749,0,NULL,NULL,3,0),
(752,'支付方式导出',NULL,1,'grid',NULL,'paytype.export',749,0,NULL,NULL,3,0),
(753,'批量删除',NULL,1,'grid',NULL,'paytype.deleteBatch',749,0,NULL,NULL,3,0),
(754,'支付方式编辑',NULL,1,'grid',NULL,'paytype.edit',749,0,NULL,NULL,3,0),
(755,'支付方式删除',NULL,1,'grid',NULL,'paytype.delete',749,0,NULL,NULL,3,0),
(756,'收货地址管理','address',1,'grid','Address',NULL,NULL,0,NULL,NULL,2,0),
(757,'收货地址查询',NULL,1,'grid',NULL,'address.list',756,0,NULL,NULL,3,0),
(758,'收货地址新增',NULL,1,'grid',NULL,'address.add',756,0,NULL,NULL,3,0),
(759,'收货地址导出',NULL,1,'grid',NULL,'address.export',756,0,NULL,NULL,3,0),
(760,'批量删除',NULL,1,'grid',NULL,'address.deleteBatch',756,0,NULL,NULL,3,0),
(761,'收货地址编辑',NULL,1,'grid',NULL,'address.edit',756,0,NULL,NULL,3,0),
(762,'收货地址删除',NULL,1,'grid',NULL,'address.delete',756,0,NULL,NULL,3,0),
(763,'自行车收藏管理','collect',1,'grid','Collect',NULL,NULL,0,NULL,'2025-01-25 15:07:22',2,0),
(764,'农产品收藏查询',NULL,1,'grid',NULL,'collect.list',763,0,NULL,NULL,3,0),
(765,'农产品收藏新增',NULL,1,'grid',NULL,'collect.add',763,0,NULL,NULL,3,0),
(766,'农产品收藏导出',NULL,1,'grid',NULL,'collect.export',763,0,NULL,NULL,3,0),
(767,'批量删除',NULL,1,'grid',NULL,'collect.deleteBatch',763,0,NULL,NULL,3,0),
(768,'农产品收藏编辑',NULL,1,'grid',NULL,'collect.edit',763,0,NULL,NULL,3,0),
(769,'农产品收藏删除',NULL,1,'grid',NULL,'collect.delete',763,0,NULL,NULL,3,0),
(770,'售后服务管理','services',1,'grid','Services',NULL,NULL,0,NULL,NULL,2,0),
(771,'售后服务查询',NULL,1,'grid',NULL,'services.list',770,0,NULL,NULL,3,0),
(772,'售后服务新增',NULL,1,'grid',NULL,'services.add',770,0,NULL,NULL,3,0),
(773,'售后服务导出',NULL,1,'grid',NULL,'services.export',770,0,NULL,NULL,3,0),
(774,'批量删除',NULL,1,'grid',NULL,'services.deleteBatch',770,0,NULL,NULL,3,0),
(775,'售后服务编辑',NULL,1,'grid',NULL,'services.edit',770,0,NULL,NULL,3,0),
(776,'售后服务删除',NULL,1,'grid',NULL,'services.delete',770,0,NULL,NULL,3,0),
(777,'轮播图管理','banner',1,'grid','Banner',NULL,NULL,0,NULL,NULL,2,0),
(778,'轮播图查询',NULL,1,'grid',NULL,'banner.list',777,0,NULL,NULL,3,0),
(779,'轮播图新增',NULL,1,'grid',NULL,'banner.add',777,0,NULL,NULL,3,0),
(780,'轮播图导出',NULL,1,'grid',NULL,'banner.export',777,0,NULL,NULL,3,0),
(781,'批量删除',NULL,1,'grid',NULL,'banner.deleteBatch',777,0,NULL,NULL,3,0),
(782,'轮播图编辑',NULL,1,'grid',NULL,'banner.edit',777,0,NULL,NULL,3,0),
(783,'轮播图删除',NULL,1,'grid',NULL,'banner.delete',777,0,NULL,NULL,3,0),
(784,'数据统计分析','statistics',1,'grid','Statistics',NULL,NULL,0,NULL,'2024-12-10 10:20:23',2,0);

/*Table structure for table `role` */

DROP TABLE IF EXISTS `role`;

CREATE TABLE `role` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '编号',
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '名称',
  `flag` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '唯一标识',
  `deleted` int(11) DEFAULT '0' COMMENT '逻辑删除',
  `create_time` datetime DEFAULT NULL COMMENT '创建时间',
  `update_time` datetime DEFAULT NULL COMMENT '更新时间',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE KEY `flag_deleted_idnex` (`flag`,`deleted`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci ROW_FORMAT=DYNAMIC COMMENT='角色';

/*Data for the table `role` */

insert  into `role`(`id`,`name`,`flag`,`deleted`,`create_time`,`update_time`) values 
(1,'管理员','ADMIN',0,'2023-01-16 19:49:44','2023-08-16 05:17:54'),
(13,'用户','member',0,'2024-12-10 10:11:31','2024-12-10 10:11:31'),
(14,'商家','business',0,'2024-12-10 10:11:31','2025-01-25 15:43:59');

/*Table structure for table `role_permission` */

DROP TABLE IF EXISTS `role_permission`;

CREATE TABLE `role_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '编号',
  `role_id` int(11) NOT NULL COMMENT '角色编号',
  `permission_id` int(11) NOT NULL COMMENT '权限编号',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE KEY `role_id` (`role_id`,`permission_id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=8986 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci ROW_FORMAT=DYNAMIC COMMENT='角色权限';

/*Data for the table `role_permission` */

insert  into `role_permission`(`id`,`role_id`,`permission_id`) values 
(8849,1,1),
(8850,1,3),
(8851,1,4),
(8852,1,8),
(8853,1,9),
(8854,1,10),
(8855,1,11),
(8856,1,12),
(8857,1,13),
(8858,1,14),
(8859,1,16),
(8860,1,21),
(8861,1,22),
(8862,1,23),
(8863,1,25),
(8864,1,27),
(8865,1,30),
(8866,1,31),
(8867,1,32),
(8868,1,35),
(8869,1,37),
(8870,1,38),
(8871,1,39),
(8872,1,40),
(8873,1,42),
(8874,1,505),
(8875,1,506),
(8876,1,507),
(8877,1,509),
(8878,1,510),
(8879,1,511),
(8880,1,512),
(8881,1,699),
(8882,1,700),
(8883,1,701),
(8884,1,702),
(8885,1,703),
(8886,1,704),
(8887,1,705),
(8888,1,706),
(8889,1,707),
(8890,1,708),
(8891,1,709),
(8892,1,710),
(8893,1,711),
(8894,1,712),
(8895,1,713),
(8896,1,714),
(8897,1,715),
(8898,1,716),
(8899,1,717),
(8900,1,718),
(8901,1,719),
(8902,1,720),
(8903,1,721),
(8904,1,722),
(8905,1,723),
(8906,1,724),
(8907,1,725),
(8908,1,726),
(8909,1,727),
(8910,1,728),
(8911,1,729),
(8912,1,730),
(8913,1,731),
(8914,1,732),
(8915,1,733),
(8916,1,734),
(8917,1,735),
(8918,1,736),
(8919,1,737),
(8920,1,738),
(8921,1,739),
(8922,1,740),
(8923,1,741),
(8924,1,742),
(8925,1,743),
(8926,1,744),
(8927,1,745),
(8928,1,746),
(8929,1,747),
(8930,1,748),
(8931,1,749),
(8932,1,750),
(8933,1,751),
(8934,1,752),
(8935,1,753),
(8936,1,754),
(8937,1,755),
(8938,1,756),
(8939,1,757),
(8940,1,758),
(8941,1,759),
(8942,1,760),
(8943,1,761),
(8944,1,762),
(8945,1,763),
(8946,1,764),
(8947,1,765),
(8948,1,766),
(8949,1,767),
(8950,1,768),
(8951,1,769),
(8952,1,770),
(8953,1,771),
(8954,1,772),
(8955,1,773),
(8956,1,774),
(8957,1,775),
(8958,1,776),
(8959,1,777),
(8960,1,778),
(8961,1,779),
(8962,1,780),
(8963,1,781),
(8964,1,782),
(8965,1,783),
(6014,9,12),
(6015,9,505),
(6016,9,506),
(6017,10,12),
(6018,10,505),
(6019,10,506),
(7490,11,12),
(7491,11,505),
(7492,11,506),
(7493,12,12),
(7494,12,505),
(7495,12,506),
(8966,13,12),
(8967,13,505),
(8968,13,506),
(8969,14,12),
(8970,14,505),
(8971,14,506),
(8979,14,721),
(8980,14,722),
(8981,14,723),
(8982,14,726),
(8983,14,727),
(8985,14,735),
(8984,14,736),
(8974,14,742),
(8975,14,743),
(8977,14,747),
(8972,14,770),
(8973,14,771),
(8976,14,775),
(8978,14,784);

/*Table structure for table `services` */

DROP TABLE IF EXISTS `services`;

CREATE TABLE `services` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '编号',
  `orders_id` int(11) DEFAULT NULL COMMENT '售后订单',
  `user_id` int(11) DEFAULT NULL COMMENT '用户',
  `type_radio` varchar(200) DEFAULT NULL COMMENT '类型,退货|换货|退款',
  `content` text COMMENT '具体原因',
  `state_radio` varchar(200) DEFAULT '审核中' COMMENT '状态,审核中|审核通过|审核失败|处理完成',
  `remarks` varchar(200) DEFAULT NULL COMMENT '处理说明',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=2 DEFAULT CHARSET=utf8 COMMENT='售后服务';

/*Data for the table `services` */

/*Table structure for table `user` */

DROP TABLE IF EXISTS `user`;

CREATE TABLE `user` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '编号',
  `username` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '用户名',
  `password` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '密码',
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '昵称',
  `email` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '邮箱',
  `address` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '地址',
  `uid` varchar(40) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '用户唯一id',
  `deleted` int(11) NOT NULL DEFAULT '0' COMMENT '逻辑删除',
  `create_time` datetime DEFAULT NULL COMMENT '添加时间',
  `update_time` datetime DEFAULT NULL COMMENT '更新时间',
  `avatar` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '头像',
  `role` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '角色',
  `score` int(11) DEFAULT '0' COMMENT '积分',
  `isvip` varchar(200) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '是否会员',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE KEY `uid_index` (`uid`) USING BTREE,
  UNIQUE KEY `username_index` (`username`,`deleted`) USING BTREE,
  UNIQUE KEY `email_index` (`email`,`deleted`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=41 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci ROW_FORMAT=DYNAMIC COMMENT='用户';

/*Data for the table `user` */

insert  into `user`(`id`,`username`,`password`,`name`,`email`,`address`,`uid`,`deleted`,`create_time`,`update_time`,`avatar`,`role`,`score`,`isvip`) values 
(1,'admin','21232f297a57a5a743894a0e4a801fc3','管理员','admin@126.com','广州南沙区','4918ea50c06a458f94878abe741b4f51',0,'2022-12-09 20:08:17','2023-08-16 15:46:27','http://localhost:9090/media/c1c271a8-1f2a-4fbe-b9dd-584fe04e0c08.jpeg','ADMIN',0,NULL),
(38,'zhangsan','e10adc3949ba59abbe56e057f20f883e','张三','zhangsan@qq.com',NULL,'de68359f-b69c-11ef-9bf3-000ec65d51bc',0,'2024-12-10 10:17:13','2025-01-25 16:16:47','http://localhost:9090/media/c8c6ff9f-d7c2-4b02-ba79-1a2062095504.jpg','member',0,'否'),
(39,'小锋','e10adc3949ba59abbe56e057f20f883e','小锋','xiaofeng@qq.coom',NULL,'ef77de36-b69c-11ef-870b-000ec65d51bc',0,'2024-12-10 10:17:42','2024-12-10 10:18:11','http://localhost:9090/media/f53f6981-3ade-4f95-bcee-dbec3db510a7.jpg','business',0,NULL),
(40,'小胖','e10adc3949ba59abbe56e057f20f883e','小胖','xiaopang@qq.com',NULL,'7c598510-b6a2-11ef-9f49-000ec65d51bc',0,'2024-12-10 10:57:26','2024-12-10 10:57:26',NULL,'business',0,NULL);

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
