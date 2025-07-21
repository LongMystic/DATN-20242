MERGE INTO {iceberg_db}.oil_fact T
USING (
    SELECT *
    FROM {iceberg_db_stg}.oil
) as S
ON T.id = S.id
WHEN MATCHED THEN
    UPDATE SET
        T.date = S.date
        , T.dcoilwtico = S.dcoilwtico
WHEN NOT MATCHED THEN
    INSERT (
        id,
        date,
        dcoilwtico
    ) VALUES (
        S.id,
        S.date,
        S.dcoilwtico
    )