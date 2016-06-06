/*
 Navicat Premium Data Transfer

 Source Server         : localhost
 Source Server Type    : MySQL
 Source Server Version : 50527
 Source Host           : localhost
 Source Database       : jtm.im

 Target Server Type    : MySQL
 Target Server Version : 50527
 File Encoding         : utf-8

 Date: 01/02/2014 18:26:36 PM
*/

SET NAMES utf8;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
--  Table structure for `post`
-- ----------------------------
DROP TABLE IF EXISTS `post`;
CREATE TABLE `post` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `pid` int(11),
  `title` text,
  `subtitle` text,
  `thumb` text,
  `link` text,
  `dlink` text,
  `post_type` text,
  `source` text,
  `price` text,
  `vendor` text,
  `author_name` text,
  `up_num` text,
  `down_num` text,
  `reply_num` text,
  `follow_num` text,
  `content` longtext,
  `processed_content` longtext,
  `author_id` text,
  `updated` datetime DEFAULT NULL,
  `created` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;