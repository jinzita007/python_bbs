-- ----------------------------
-- Table structure for bbs_theme
-- ----------------------------
DROP TABLE IF EXISTS `bbs_theme`;
CREATE TABLE `bbs_theme` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `titleId` int(11) DEFAULT NULL COMMENT '主题_标题id',
  `url` varchar(255) NOT NULL COMMENT '主题_URL',
  `title` varchar(255) DEFAULT NULL COMMENT '主题_标题名',
  `reply_number` int(11) DEFAULT NULL COMMENT '主题_回复数',
  `view_number` int(11) DEFAULT NULL COMMENT '主题_浏览数',
  `public_date` varchar(255) DEFAULT NULL COMMENT '主题_时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for bbs_post
-- ----------------------------
DROP TABLE IF EXISTS `bbs_post`;
CREATE TABLE `bbs_post` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '自动递增',
  `authorId` int(11) NOT NULL COMMENT '帖子_作者ID',
  `titleId` int(11) NOT NULL COMMENT '主题_标题ID',
  `url` varchar(255) NOT NULL COMMENT '帖子_URL',
  `authorUrl` varchar(255) NOT NULL COMMENT '帖子_作者URL',
  `author` varchar(255) NOT NULL COMMENT '帖子_作者名',
  `content` text NOT NULL COMMENT '帖子_正文内容',
  `dates` varchar(200) NOT NULL COMMENT '帖子_发表时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;