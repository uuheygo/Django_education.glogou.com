/* delete some test data from database */


DELETE FROM `mediawatch_lu`.`baidu_index_ch` WHERE `my_date`='2015-07-23';
DELETE FROM `mediawatch_lu`.`baidu_index_ch` WHERE `my_date`='2015-07-24';

DELETE FROM `mediawatch_lu`.`baidu_index_en` WHERE `my_date`='2015-07-23';
DELETE FROM `mediawatch_lu`.`baidu_index_en` WHERE `my_date`='2015-07-24';

DELETE FROM `mediawatch_lu`.`baidu_news_ch` WHERE `my_date`='2015-07-23';
DELETE FROM `mediawatch_lu`.`baidu_news_ch` WHERE `my_date`='2015-07-24';

DELETE FROM `mediawatch_lu`.`baidu_news_en` WHERE `my_date`='2015-07-23';
DELETE FROM `mediawatch_lu`.`baidu_news_en` WHERE `my_date`='2015-07-24';

DELETE FROM `mediawatch_lu`.`baidu_site` WHERE `my_date`='2015-07-23';
DELETE FROM `mediawatch_lu`.`baidu_site` WHERE `my_date`='2015-07-24';

DELETE FROM `mediawatch_lu`.`google_index_en` WHERE `my_date`='2015-07-23';
DELETE FROM `mediawatch_lu`.`google_index_en` WHERE `my_date`='2015-07-24';

DELETE FROM `mediawatch_lu`.`google_index_hk` WHERE `my_date`='2015-07-23';
DELETE FROM `mediawatch_lu`.`google_index_hk` WHERE `my_date`='2015-07-24';

DELETE FROM `mediawatch_lu`.`google_news` WHERE `my_date`='2015-07-23';
DELETE FROM `mediawatch_lu`.`google_news` WHERE `my_date`='2015-07-24';

DELETE FROM `mediawatch_lu`.`google_site` WHERE `my_date`='2015-07-23';
DELETE FROM `mediawatch_lu`.`google_site` WHERE `my_date`='2015-07-24';