INSERT INTO abbreviation_names (abbrv_name)
(
    select :abbrv_name from dual where not exists (
        select * from abbreviation_names where abbrv_name = :abbrv_name)
);

INSERT INTO tags (tag_name)
SELECT :tag_name
  FROM dual
 WHERE NOT EXISTS (SELECT NULL
                     FROM tags
                    WHERE tag_name = :tag_name
                  );

INSERT INTO abbrv_meanings (meaning, abbrv_name_id, tag_id)
    VALUES (
        :abbrv_meaning,
        (
        SELECT abbrv_name_id FROM abbreviation_names
        WHERE abbrv_name = :abbrv_name
        ),
        (
        SELECT tag_id FROM tags
        WHERE tag_name = :tag_name
        )
    );

    commit;

