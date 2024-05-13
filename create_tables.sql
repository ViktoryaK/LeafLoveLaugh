CREATE TABLE IF NOT EXISTS Users (
    user_id UUID PRIMARY KEY,
    user_name VARCHAR(255),
    password VARCHAR(255),
    user_bio VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS Plants (
    plant_id SERIAL PRIMARY KEY,
    Scientific_Name VARCHAR(255),
    Common_Name VARCHAR(255),
    img_name VARCHAR(255),
    Sunlight VARCHAR(255),
    Moisture VARCHAR(255),
    Soil_Indicator VARCHAR(255),
    Plant_Spread VARCHAR(255),
    Plant_Height VARCHAR(255),
    Indoor_Spread VARCHAR(255),
    Indoor_Height VARCHAR(255),
    Toxic_Dogs VARCHAR(255),
    Toxic_Cats VARCHAR(255),
    Plant_Habit VARCHAR(255),
    Plant_Type VARCHAR(255),
    Indoor_Flowering VARCHAR(255),
    Hanging VARCHAR(255),
    Bloom_Period VARCHAR(255),
    Humidity VARCHAR(255),
    Air_Purifying VARCHAR(255),
    Ph_Soil VARCHAR(255),
    Bloom_Description VARCHAR(255)
);