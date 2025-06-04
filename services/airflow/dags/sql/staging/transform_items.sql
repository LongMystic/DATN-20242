MERGE INTO {iceberg_db}.items_dim T
USING (
    SELECT *
    FROM {iceberg_db_stg}.items
) as S
ON T.id = S.id
WHEN MATCHED THEN
    UPDATE SET
        T.item_nbr = S.item_nbr
        , T.family = S.family
        , T.class = S.class
        , T.perishable = S.perishable
WHEN NOT MATCHED THEN
    INSERT (
        id,
        item_nbr,
        family,
        class,
        perishable
    ) VALUES (
        S.id,
        S.item_nbr,
        S.family,
        S.class,
        S.perishable
    )

