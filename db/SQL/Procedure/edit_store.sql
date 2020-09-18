/*
Edit Store
*/

DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `edit_store`(IN `p_id` INT(11) UNSIGNED, IN `p_name` VARCHAR(255) CHARSET utf8)
    NO SQL
    COMMENT 'Edit Store'
rootFlag: BEGIN
    IF ISNULL(p_id) 
    || ISNULL(p_name) THEN
        SELECT response_format(3, NULL) JSON_VALUE;
        LEAVE rootFlag;
    END IF;

    SET @name = p_name COLLATE utf8_unicode_ci;
    UPDATE tb_store SET _name = @name WHERE _id = p_id;

    SELECT response_format(1, get_store_list()) JSON_VALUE;
END$$
DELIMITER ;