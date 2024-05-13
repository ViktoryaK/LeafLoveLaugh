CREATE KEYSPACE lll_comments WITH REPLICATION = {'class' : 'SimpleStrategy', 'replication_factor' : 3 };

USE lll_comments;

CREATE TABLE search_comments
(
    comment_id  UUID,
    plant_id    int,
    comment     text,
    date        timestamp,
    user_id     UUID,
    user_name   text,
    PRIMARY KEY ((comment_id), date)
) WITH CLUSTERING ORDER BY (date DESC);