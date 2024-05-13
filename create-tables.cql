CREATE KEYSPACE lll_search WITH REPLICATION = {'class' : 'SimpleStrategy', 'replication_factor' : 3 };

USE lll_search;

CREATE TABLE search_tags
(
    plant_id          int,
    plant_name        text,
    plant_img         text,
    sunlight          text,
    moisture          text,
    indoor_spread_min float,
    indoor_spread_max float,
    indoor_height_min float,
    indoor_height_max float,
    toxic_dogs        text,
    toxic_cats        text,
    PRIMARY KEY ((sunlight, moisture, toxic_dogs, toxic_cats, indoor_height_min, indoor_height_max, indoor_spread_min,
                  indoor_spread_max), plant_id)
);