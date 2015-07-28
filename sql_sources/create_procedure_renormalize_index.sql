USE `mediaWatch_lu`;
DROP procedure IF EXISTS `renormalize_index`;

DELIMITER $$
USE `mediaWatch_lu`$$
CREATE PROCEDURE `renormalize_index`()
BEGIN

UPDATE mediaWatch_lu.baidu_index_ch 
SET my_index_re =  
CASE
  WHEN my_index = 0 THEN 0
  WHEN my_index is null THEN 0
  WHEN 20*LOG10(my_index) + 60 <0 THEN 0
  ELSE 20*LOG10(my_index) + 60 
END;

UPDATE mediaWatch_lu.baidu_index_en
SET my_index_re =  
CASE
  WHEN my_index = 0 THEN 0
  WHEN my_index is null THEN 0
  WHEN 20*LOG10(my_index) + 60 <0 THEN 0
  ELSE 20*LOG10(my_index) + 60 
END;

UPDATE mediaWatch_lu.baidu_news_ch
SET my_index_re =  
CASE
  WHEN my_index = 0 THEN 0
  WHEN my_index is null THEN 0
  WHEN 20*LOG10(my_index) + 60 <0 THEN 0
  ELSE 20*LOG10(my_index) + 60 
END;

UPDATE mediaWatch_lu.baidu_news_en
SET my_index_re =  
CASE
  WHEN my_index = 0 THEN 0
  WHEN my_index is null THEN 0
  WHEN 20*LOG10(my_index) + 60 <0 THEN 0
  ELSE 20*LOG10(my_index) + 60 
END;

UPDATE mediaWatch_lu.baidu_site
SET my_index_re =  
CASE
  WHEN my_index = 0 THEN 0
  WHEN my_index is null THEN 0
  WHEN 20*LOG10(my_index) + 60 <0 THEN 0
  ELSE 20*LOG10(my_index) + 60 
END;

UPDATE mediaWatch_lu.composite_index
SET my_index_re =  
CASE
  WHEN my_index = 0 THEN 0
  WHEN my_index is null THEN 0
  WHEN 20*LOG10(my_index) + 60 <0 THEN 0
  ELSE 20*LOG10(my_index) + 60 
END;

UPDATE mediaWatch_lu.google_index_en
SET my_index_re =  
CASE
  WHEN my_index = 0 THEN 0
  WHEN my_index is null THEN 0
  WHEN 20*LOG10(my_index) + 60 <0 THEN 0
  ELSE 20*LOG10(my_index) + 60 
END;

UPDATE mediaWatch_lu.google_index_hk
SET my_index_re =  
CASE
  WHEN my_index = 0 THEN 0
  WHEN my_index is null THEN 0
  WHEN 20*LOG10(my_index) + 60 <0 THEN 0
  ELSE 20*LOG10(my_index) + 60 
END;

UPDATE mediaWatch_lu.google_news
SET my_index_re =  
CASE
  WHEN my_index = 0 THEN 0
  WHEN my_index is null THEN 0
  WHEN 20*LOG10(my_index) + 60 <0 THEN 0
  ELSE 20*LOG10(my_index) + 60 
END;

UPDATE mediaWatch_lu.google_site
SET my_index_re =  
CASE
  WHEN my_index = 0 THEN 0
  WHEN my_index is null THEN 0
  WHEN 20*LOG10(my_index) + 60 <0 THEN 0
  ELSE 20*LOG10(my_index) + 60 
END;

UPDATE mediaWatch_lu.yahoojap_index_en
SET my_index_re =  
CASE
  WHEN my_index = 0 THEN 0
  WHEN my_index is null THEN 0
  WHEN 20*LOG10(my_index) + 60 <0 THEN 0
  ELSE 20*LOG10(my_index) + 60 
END;

UPDATE mediaWatch_lu.yahoojap_index_jp
SET my_index_re =  
CASE
  WHEN my_index = 0 THEN 0
  WHEN my_index is null THEN 0
  WHEN 20*LOG10(my_index) + 60 <0 THEN 0
  ELSE 20*LOG10(my_index) + 60 
END;
END$$

DELIMITER ;

