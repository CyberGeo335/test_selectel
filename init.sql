CREATE TABLE file_uploads (
    id_number SERIAL PRIMARY KEY,
    img_name VARCHAR(255),
    tag VARCHAR(255),
    root VARCHAR(255),
    label VARCHAR(255),
    comment TEXT
);