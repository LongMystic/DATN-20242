MERGE INTO longvk_test.category_dim T
USING (
    SELECT *
    FROM longvk_test.category
) as S
ON T.id = S.id
WHEN MATCHED THEN
    UPDATE SET
        T.category_id = S.category_id
        , T.category_name = S.category_name
        , T.level = S.level
        , T.parent_category = S.parent_category
        , T.parent_id = S.parent_id
        , T.industry_id = S.industry_id
        , T.is_selected = S.is_selected
WHEN NOT MATCHED THEN
    INSERT *