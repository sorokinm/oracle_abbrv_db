CREATE TABLE abbreviation_names
(
    abbrv_name_id NUMBER GENERATED ALWAYS as IDENTITY(START WITH 1 INCREMENT BY 1),
    abbrv_name VARCHAR2(50),
    CONSTRAINT abbrv_name_pk PRIMARY KEY (abbrv_name_id),
    CONSTRAINT abbrv_name_unique UNIQUE (abbrv_name)
);

CREATE TABLE tags
(
    tag_id NUMBER GENERATED ALWAYS as IDENTITY(START WITH 1 INCREMENT BY 1),
    tag_name VARCHAR2(150),
    CONSTRAINT tags_pk PRIMARY KEY (tag_id),
    CONSTRAINT tag_name UNIQUE (tag_name)
);

CREATE TABLE abbrv_meanings
(
    meaning_id NUMBER GENERATED ALWAYS as IDENTITY(START WITH 1 INCREMENT BY 1),
    abbrv_name_id NUMBER,
    meaning VARCHAR(300),
    tag_id NUMBER,
    CONSTRAINT abbrv_meanining_abbrv_name_fk FOREIGN KEY (abbrv_name_id)
    REFERENCES abbreviation_names(abbrv_name_id),

    CONSTRAINT abbrv_meanining_tag_fk FOREIGN KEY (tag_id)
    REFERENCES tags(tag_id)
);