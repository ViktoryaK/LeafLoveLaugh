CREATE KEYSPACE lll_review WITH REPLICATION = {'class' : 'SimpleStrategy', 'replication_factor' : 3 };

USE lll_review;

CREATE TABLE reviews
(
    comment_id UUID,
    plant_id   int,
    comment    text,
    date       timestamp,
    user_id    UUID,
    user_name  text,
    PRIMARY KEY ((plant_id), date, comment_id)
);
