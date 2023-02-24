CREATE TABLE settings (
    server_id INTEGER UNIQUE NOT NULL,
    reaction VARCHAR NOT NULL,
    l_channels VARCHAR,
    s_channel INTEGER,
    r_cost INTEGER NOT NULL,
    award INTEGER NOT NULL);


CREATE TABLE data (
    server_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    score INTEGER NOT NULL)