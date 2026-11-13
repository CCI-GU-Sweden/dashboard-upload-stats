-- Compatible with the existing Omero_GU PostgreSQL uploader schema.
CREATE TABLE public.imports (
    id serial PRIMARY KEY,
    time timestamp without time zone NOT NULL,
    username text NOT NULL,
    groupname text NOT NULL,
    scope text NOT NULL,
    file_count integer NOT NULL,
    total_file_size_mb real NOT NULL,
    import_time_s real NOT NULL
);
