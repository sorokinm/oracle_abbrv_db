INSERT INTO abbreviation_names VALUES (abbrv_name)
SELECT :abbrv_name
  FROM dual
 WHERE NOT EXISTS (SELECT NULL
                     FROM abbreviation_names
                    WHERE name = :abbrv_name
                  );

INSERT INTO tags VALUES (tag_name)
SELECT :tag_name
  FROM dual
 WHERE NOT EXISTS (SELECT NULL
                     FROM tags
                    WHERE name = :tag_name
                  );

INSERT INTO abbrv_meanings (meaning, abbrv_name_id, tag_id)
    VALUES (
        :abbrv_meaning,
        (
        SELECT abbrv_name_id FROM abbreviation_names
        ),
        (
        SELECT tag_id FROM tags
        )
    );

