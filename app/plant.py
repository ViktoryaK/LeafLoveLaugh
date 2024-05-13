from dataclasses import dataclass


@dataclass
class Plant:
    id: int
    scientific_name: str
    common_name: str
    img_name: str
    sunlight: str
    moisture: str
    soil_indicator: str
    spread: str
    height: str
    indoor_spread: str
    indoor_height: str
    toxic_dogs: str
    toxic_cats: str
    habit: str
    type: str
    indoor_flowering: str
    hanging: str
    bloom_period: str
    humidity: str
    air_purifying: str
    ph_soil: str
    bloom_description: str
