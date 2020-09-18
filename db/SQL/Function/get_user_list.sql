/*
Get User List
*/

DELIMITER $$
CREATE DEFINER=`root`@`localhost` FUNCTION `get_user_list`() RETURNS mediumtext CHARSET utf8
    NO SQL
    COMMENT 'Get User List'
BEGIN
    SET @json = CONCAT(
        '[',
        (
            SELECT GROUP_CONCAT(
                DISTINCT
                '{',
                '"_id":', _id, ',',
                '"_name":"', _name, '",',
                '"_cash_balance":', _cash_balance,
                '}'
                ORDER BY _name ASC
            ) FROM (
                SELECT * FROM tb_user
            ) tb
        ),
        ']'
    );

    RETURN CASE WHEN ISNULL(@json) THEN '[]' ELSE @json END;
END$$
DELIMITER ;