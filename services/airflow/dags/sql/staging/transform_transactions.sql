MERGE INTO {iceberg_db}.transactions_fact T
USING (
    SELECT *
    FROM {iceberg_db_stg}.transactions
) as S
ON T.id = S.id

WHEN MATCHED THEN
    UPDATE SET
        T.date = S.date
        , T.store_nbr = S.store_nbr
        , T.transactions = S.transactions
WHEN NOT MATCHED THEN
    INSERT (
        id,
        date,
        store_nbr,
        transactions
    ) VALUES (
        S.id,
        S.date,
        S.store_nbr,
        S.transactions
    )