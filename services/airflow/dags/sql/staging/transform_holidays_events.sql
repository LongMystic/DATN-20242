MERGE INTO {iceberg_db}.holidays_events_dim T
USING (
    SELECT *
    FROM {iceberg_db_stg}.holidays_events
) as S
ON T.id = S.id
WHEN MATCHED THEN
    UPDATE SET
        T.date = S.date
        , T.type = S.type
        , T.locale = S.locale
        , T.locale_name = S.locale_name
        , T.description = S.description
        , T.transferred = S.transferred
WHEN NOT MATCHED THEN
    INSERT (
        id,
        date,
        type,
        locale,
        locale_name,
        description,
        transferred
    ) VALUES (
        S.id,
        S.date,
        S.type,
        S.locale,
        S.locale_name,
        S.description,
        S.transferred
    )

