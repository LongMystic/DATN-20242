MERGE INTO {iceberg_db}.stores_dim T
USING (
    SELECT *
    FROM {iceberg_db_stg}.stores
) as S
ON T.id = S.id
WHEN MATCHED THEN
    UPDATE SET
        T.store_nbr = S.store_nbr
        , T.city = S.city
        , T.state = S.state
        , T.type = S.type
        , T.cluster = S.cluster
WHEN NOT MATCHED THEN
    INSERT (
        id,
        store_nbr,
        city,
        state,
        type,
        cluster
    ) VALUES (
        S.id,
        S.store_nbr,
        S.city,
        S.state,
        S.type,
        S.cluster
    )

