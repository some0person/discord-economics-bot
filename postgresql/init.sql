CREATE TABLE settings (
    server_id BIGINT UNIQUE NOT NULL,
    reaction VARCHAR NOT NULL,
    l_channels VARCHAR,
    s_channel BIGINT,
    r_cost INTEGER NOT NULL,
    award INTEGER NOT NULL);


CREATE TABLE data (
    server_id BIGINT NOT NULL,
    member_id BIGINT NOT NULL,
    score INTEGER NOT NULL);


CREATE TABLE pricelist (
    item_id INTEGER NOT NULL,
    server_id BIGINT NOT NULL,
    title VARCHAR NOT NULL,
    price INTEGER NOT NULL,
    description VARCHAR);
