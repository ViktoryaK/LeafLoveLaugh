CREATE KEYSPACE lll_latest_reviews WITH REPLICATION = {'class' : 'SimpleStrategy', 'replication_factor' : 3 };

USE lll_latest_reviews;

CREATE TABLE latest_reviews
(
    review_id  UUID,
    plant_id    int,
    review     text,
    date        timestamp,
    user_id     UUID,
    user_name   text,
    PRIMARY KEY ((review_id), date)
) WITH CLUSTERING ORDER BY (date DESC);