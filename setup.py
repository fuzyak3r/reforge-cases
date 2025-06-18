from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime
import random
import os
from dotenv import load_dotenv
import requests
import json

# Load environment variables
load_dotenv()

# MongoDB connection
mongo_uri = os.getenv('MONGO_URI', 'mongodb://')
mongo_db = os.getenv('MONGO_DB', 'reforge')

client = MongoClient(mongo_uri)
db = client[mongo_db]

# Clear existing data
db.cases.delete_many({})
db.skins.delete_many({})
db.qualities.delete_many({})
db.weapons.delete_many({})

print("Начинаем загрузку данных для кейсов CS:GO...")

# Create quality levels
qualities = [
    {
        "title": "Consumer Grade",
        "color": "#b0c3d9",
        "order": 1
    },
    {
        "title": "Industrial Grade",
        "color": "#5e98d9",
        "order": 2
    },
    {
        "title": "Mil-Spec",
        "color": "#4b69ff",
        "order": 3
    },
    {
        "title": "Restricted",
        "color": "#8847ff",
        "order": 4
    },
    {
        "title": "Classified",
        "color": "#d32ce6",
        "order": 5
    },
    {
        "title": "Covert",
        "color": "#eb4b4b",
        "order": 6
    },
    {
        "title": "Exceedingly Rare",
        "color": "#ffae39",
        "order": 7
    },
    {
        "title": "Contraband",
        "color": "#e4ae39",
        "order": 8
    }
]

# Insert quality levels
quality_ids = {}
for quality in qualities:
    result = db.qualities.insert_one(quality)
    quality_ids[quality["title"]] = result.inserted_id

# Define weapons
weapons = [
    {"title": "AK-47", "type": "rifle"},
    {"title": "M4A4", "type": "rifle"},
    {"title": "M4A1-S", "type": "rifle"},
    {"title": "AWP", "type": "sniper rifle"},
    {"title": "Desert Eagle", "type": "pistol"},
    {"title": "USP-S", "type": "pistol"},
    {"title": "Glock-18", "type": "pistol"},
    {"title": "P250", "type": "pistol"},
    {"title": "Five-SeveN", "type": "pistol"},
    {"title": "Tec-9", "type": "pistol"},
    {"title": "P90", "type": "smg"},
    {"title": "MP7", "type": "smg"},
    {"title": "UMP-45", "type": "smg"},
    {"title": "MAC-10", "type": "smg"},
    {"title": "MP9", "type": "smg"},
    {"title": "Galil AR", "type": "rifle"},
    {"title": "FAMAS", "type": "rifle"},
    {"title": "SG 553", "type": "rifle"},
    {"title": "AUG", "type": "rifle"},
    {"title": "SSG 08", "type": "sniper rifle"},
    {"title": "G3SG1", "type": "sniper rifle"},
    {"title": "SCAR-20", "type": "sniper rifle"},
    {"title": "Nova", "type": "shotgun"},
    {"title": "XM1014", "type": "shotgun"},
    {"title": "Sawed-Off", "type": "shotgun"},
    {"title": "MAG-7", "type": "shotgun"},
    {"title": "M249", "type": "machinegun"},
    {"title": "Negev", "type": "machinegun"},
    {"title": "CZ75-Auto", "type": "pistol"},
    {"title": "R8 Revolver", "type": "pistol"},
    {"title": "Dual Berettas", "type": "pistol"},
    {"title": "PP-Bizon", "type": "smg"},
    {"title": "P2000", "type": "pistol"},
    {"title": "Bayonet", "type": "knife"},
    {"title": "Flip Knife", "type": "knife"},
    {"title": "Gut Knife", "type": "knife"},
    {"title": "Karambit", "type": "knife"},
    {"title": "M9 Bayonet", "type": "knife"},
    {"title": "Huntsman Knife", "type": "knife"},
    {"title": "Butterfly Knife", "type": "knife"},
    {"title": "Falchion Knife", "type": "knife"},
    {"title": "Shadow Daggers", "type": "knife"},
    {"title": "Bowie Knife", "type": "knife"},
    {"title": "Hand Wraps", "type": "gloves"},
    {"title": "Bloodhound Gloves", "type": "gloves"},
    {"title": "Driver Gloves", "type": "gloves"},
    {"title": "Moto Gloves", "type": "gloves"},
    {"title": "Specialist Gloves", "type": "gloves"},
    {"title": "Sport Gloves", "type": "gloves"},
    {"title": "Hydra Gloves", "type": "gloves"}
]

# Insert weapons
weapon_ids = {}
for weapon in weapons:
    result = db.weapons.insert_one(weapon)
    weapon_ids[weapon["title"]] = result.inserted_id

# Define case release dates
case_info = {
    "CS:GO Weapon Case": "2013-08-14",
    "eSports 2013 Case": "2013-08-14",
    "CS:GO Weapon Case 2": "2013-11-06",
    "Winter Offensive Weapon Case": "2013-12-18",
    "eSports 2013 Winter Case": "2013-12-18",
    "CS:GO Weapon Case 3": "2014-02-12",
    "Operation Phoenix Weapon Case": "2014-02-20",
    "Huntsman Weapon Case": "2014-05-01",
    "Operation Breakout Weapon Case": "2014-07-01",
    "eSports 2014 Summer Case": "2014-07-10",
    "Operation Vanguard Weapon Case": "2014-11-11",
    "Chroma Case": "2015-01-08",
    "Chroma 2 Case": "2015-04-15",
    "Falchion Case": "2015-05-26",
    "Shadow Case": "2015-09-17",
    "Revolver Case": "2015-12-08",
    "Operation Wildfire Case": "2016-02-17",
    "Chroma 3 Case": "2016-04-27",
    "Gamma Case": "2016-06-15",
    "Gamma 2 Case": "2016-08-18",
    "Glove Case": "2016-11-28",
    "Spectrum Case": "2017-03-15",
    "Operation Hydra Case": "2017-05-23",
    "Spectrum 2 Case": "2017-09-14"
}

# Map for case image URLs
case_images = {
    "CS:GO Weapon Case": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/weapon_cases/crate_valve_1_png.png",
    "eSports 2013 Case": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/weapon_cases/crate_esports_2013_png.png",
    "CS:GO Weapon Case 2": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/weapon_cases/crate_valve_2_png.png",
    "Winter Offensive Weapon Case": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/weapon_cases/crate_community_1_png.png",
    "eSports 2013 Winter Case": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/weapon_cases/crate_esports_2013_14_png.png",
    "CS:GO Weapon Case 3": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/weapon_cases/crate_valve_3_png.png",
    "Operation Phoenix Weapon Case": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/weapon_cases/crate_community_2_png.png",
    "Huntsman Weapon Case": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/weapon_cases/crate_community_3_png.png",
    "Operation Breakout Weapon Case": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/weapon_cases/crate_community_4_png.png",
    "eSports 2014 Summer Case": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/weapon_cases/crate_esports_2014_summer_png.png",
    "Operation Vanguard Weapon Case": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/weapon_cases/crate_community_5_png.png",
    "Chroma Case": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/weapon_cases/crate_community_6_png.png",
    "Chroma 2 Case": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/weapon_cases/crate_community_7_png.png",
    "Falchion Case": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/weapon_cases/crate_community_8_png.png",
    "Shadow Case": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/weapon_cases/crate_community_9_png.png",
    "Revolver Case": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/weapon_cases/crate_community_10_png.png",
    "Operation Wildfire Case": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/weapon_cases/crate_community_11_png.png",
    "Chroma 3 Case": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/weapon_cases/crate_community_12_png.png",
    "Gamma Case": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/weapon_cases/crate_community_13_png.png",
    "Gamma 2 Case": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/weapon_cases/crate_gamma_2_png.png",
    "Glove Case": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/weapon_cases/crate_community_15_png.png",
    "Spectrum Case": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/weapon_cases/crate_community_16_png.png",
    "Operation Hydra Case": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/weapon_cases/crate_community_17_png.png",
    "Spectrum 2 Case": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/weapon_cases/crate_community_18_png.png"
}

# Helper function to get case image URL
def get_case_image(case_name):
    if case_name in case_images:
        return case_images[case_name]
    else:
        # Fallback to a generic case image
        return "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/weapon_cases/crate_community_1_png.png"

# Добавляем словарь с изображениями ножей
knife_images = {
    "Bayonet": {
        "Vanilla": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/weapons/base_weapons/weapon_bayonet_png.png",
        "Blue Steel": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_bayonet_aq_blued_light_png.png",
        "Boreal Forest": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_bayonet_hy_forest_boreal_light_png.png",
        "Case Hardened": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_bayonet_aq_oiled_light_png.png",
        "Crimson Web": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_bayonet_hy_webs_light_png.png",
        "Fade": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_bayonet_aa_fade_light_png.png",
        "Forest DDPAT": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_bayonet_hy_ddpat_light_png.png",
        "Night": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_bayonet_so_night_light_png.png",
        "Safari Mesh": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_bayonet_sp_mesh_tan_light_png.png",
        "Scorched": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_bayonet_sp_dapple_light_png.png",
        "Slaughter": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_bayonet_am_zebra_light_png.png",
        "Stained": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_bayonet_aq_forced_light_png.png",
        "Urban Masked": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_bayonet_sp_tape_urban_light_png.png"
    },
    "Flip Knife": {
        "Vanilla": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/weapons/base_weapons/weapon_knife_flip_png.png",
        "Blue Steel": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_knife_flip_aq_blued_light_png.png", 
        "Boreal Forest": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_knife_flip_hy_forest_boreal_light_png.png",
        "Case Hardened": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_knife_flip_aq_oiled_light_png.png",
        "Crimson Web": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_knife_flip_hy_webs_light_png.png",
        "Fade": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_knife_flip_aa_fade_light_png.png",
        "Forest DDPAT": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_knife_flip_hy_ddpat_light_png.png",
        "Night": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_knife_flip_so_night_light_png.png",
        "Safari Mesh": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_knife_flip_sp_mesh_tan_light_png.png",
        "Scorched": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_knife_flip_sp_dapple_light_png.png",
        "Slaughter": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_knife_flip_am_zebra_light_png.png",
        "Stained": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_knife_flip_aq_forced_light_png.png",
        "Urban Masked": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_knife_flip_sp_tape_urban_light_png.png"
    },
    "Gut Knife": {
        "Vanilla": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/weapons/base_weapons/weapon_knife_gut_png.png",
        "Blue Steel": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_knife_gut_aq_blued_light_png.png",
        "Boreal Forest": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_knife_gut_hy_forest_boreal_light_png.png",
        "Case Hardened": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_knife_gut_aq_oiled_light_png.png",
        "Crimson Web": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_knife_gut_hy_webs_light_png.png",
        "Fade": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_knife_gut_aa_fade_light_png.png",
        "Forest DDPAT": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_knife_gut_hy_ddpat_light_png.png",
        "Night": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_knife_gut_so_night_light_png.png",
        "Safari Mesh": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_knife_gut_sp_mesh_tan_light_png.png",
        "Scorched": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_knife_gut_sp_dapple_light_png.png",
        "Slaughter": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_knife_gut_am_zebra_light_png.png",
        "Stained": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_knife_gut_aq_forced_light_png.png",
        "Urban Masked": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_knife_gut_sp_tape_urban_light_png.png"
    },
    "Karambit": {
        "Vanilla": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/weapons/base_weapons/weapon_knife_karambit_png.png",
        "Blue Steel": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_knife_karambit_aq_blued_light_png.png",
        "Boreal Forest": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_knife_karambit_hy_forest_boreal_light_png.png",
        "Case Hardened": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_knife_karambit_aq_oiled_light_png.png",
        "Crimson Web": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_knife_karambit_hy_webs_light_png.png",
        "Fade": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_knife_karambit_aa_fade_light_png.png",
        "Forest DDPAT": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_knife_karambit_hy_ddpat_light_png.png",
        "Night": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_knife_karambit_so_night_light_png.png",
        "Safari Mesh": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_knife_karambit_sp_mesh_tan_light_png.png",
        "Scorched": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_knife_karambit_sp_dapple_light_png.png",
        "Slaughter": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_knife_karambit_am_zebra_light_png.png",
        "Stained": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_knife_karambit_aq_forced_light_png.png",
        "Urban Masked": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_knife_karambit_sp_tape_urban_light_png.png"
    },
    "M9 Bayonet": {
        "Vanilla": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/weapons/base_weapons/weapon_knife_m9_bayonet_png.png",
        "Blue Steel": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_knife_m9_bayonet_aq_blued_light_png.png",
        "Boreal Forest": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_knife_m9_bayonet_hy_forest_boreal_light_png.png",
        "Case Hardened": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_knife_m9_bayonet_aq_oiled_light_png.png",
        "Crimson Web": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_knife_m9_bayonet_hy_webs_light_png.png",
        "Fade": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_knife_m9_bayonet_aa_fade_light_png.png",
        "Forest DDPAT": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_knife_m9_bayonet_hy_ddpat_light_png.png",
        "Night": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_knife_m9_bayonet_so_night_light_png.png",
        "Safari Mesh": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_knife_m9_bayonet_sp_mesh_tan_light_png.png",
        "Scorched": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_knife_m9_bayonet_sp_dapple_light_png.png",
        "Slaughter": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_knife_m9_bayonet_am_zebra_light_png.png",
        "Stained": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_knife_m9_bayonet_aq_forced_light_png.png",
        "Urban Masked": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_knife_m9_bayonet_sp_tape_urban_light_png.png"
    },
    "Huntsman Knife": {
        "Vanilla": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/weapons/base_weapons/weapon_knife_tactical_png.png",
        "Blue Steel": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_knife_tactical_aq_blued_light_png.png",
        "Boreal Forest": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_knife_tactical_hy_forest_boreal_light_png.png",
        "Case Hardened": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_knife_tactical_aq_oiled_light_png.png",
        "Crimson Web": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_knife_tactical_hy_webs_light_png.png",
        "Fade": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_knife_tactical_aa_fade_light_png.png",
        "Forest DDPAT": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_knife_tactical_hy_ddpat_light_png.png",
        "Night": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_knife_tactical_so_night_light_png.png",
        "Safari Mesh": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_knife_tactical_sp_mesh_tan_light_png.png",
        "Scorched": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_knife_tactical_sp_dapple_light_png.png",
        "Slaughter": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_knife_tactical_am_zebra_light_png.png",
        "Stained": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_knife_tactical_aq_forced_light_png.png",
        "Urban Masked": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_knife_tactical_sp_tape_urban_light_png.png"
    },
    "Butterfly Knife": {
        "Vanilla": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/weapons/base_weapons/weapon_knife_butterfly_png.png",
        "Blue Steel": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_knife_butterfly_aq_blued_light_png.png",
        "Boreal Forest": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_knife_butterfly_hy_forest_boreal_light_png.png",
        "Case Hardened": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_knife_butterfly_aq_oiled_light_png.png",
        "Crimson Web": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_knife_butterfly_hy_webs_light_png.png",
        "Fade": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_knife_butterfly_aa_fade_light_png.png",
        "Forest DDPAT": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_knife_butterfly_hy_ddpat_light_png.png",
        "Night": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_knife_butterfly_so_night_light_png.png",
        "Safari Mesh": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_knife_butterfly_sp_mesh_tan_light_png.png",
        "Scorched": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_knife_butterfly_sp_dapple_light_png.png",
        "Slaughter": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_knife_butterfly_am_zebra_light_png.png",
        "Stained": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_knife_butterfly_aq_forced_light_png.png",
        "Urban Masked": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_knife_butterfly_sp_tape_urban_light_png.png"
    },
    "Falchion Knife": {
        "Vanilla": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/weapons/base_weapons/weapon_knife_falchion_png.png",
        "Blue Steel": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_knife_falchion_aq_blued_light_png.png",
        "Boreal Forest": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_knife_falchion_hy_forest_boreal_light_png.png",
        "Case Hardened": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_knife_falchion_aq_oiled_light_png.png",
        "Crimson Web": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_knife_falchion_hy_webs_light_png.png",
        "Fade": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_knife_falchion_aa_fade_light_png.png",
        "Forest DDPAT": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_knife_falchion_hy_ddpat_light_png.png",
        "Night": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_knife_falchion_so_night_light_png.png",
        "Safari Mesh": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_knife_falchion_sp_mesh_tan_light_png.png",
        "Scorched": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_knife_falchion_sp_dapple_light_png.png",
        "Slaughter": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_knife_falchion_am_zebra_light_png.png",
        "Stained": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_knife_falchion_aq_forced_light_png.png",
        "Urban Masked": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_knife_falchion_sp_tape_urban_light_png.png"
    },
    "Shadow Daggers": {
        "Vanilla": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/weapons/base_weapons/weapon_knife_push_png.png",
        "Blue Steel": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_knife_push_aq_blued_light_png.png",
        "Boreal Forest": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_knife_push_hy_forest_boreal_light_png.png",
        "Case Hardened": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_knife_push_aq_oiled_light_png.png",
        "Crimson Web": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_knife_push_hy_webs_light_png.png",
        "Fade": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_knife_push_aa_fade_light_png.png",
        "Forest DDPAT": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_knife_push_hy_ddpat_light_png.png",
        "Night": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_knife_push_so_night_light_png.png",
        "Safari Mesh": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_knife_push_sp_mesh_tan_light_png.png",
        "Scorched": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_knife_push_sp_dapple_light_png.png",
        "Slaughter": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_knife_push_am_zebra_light_png.png",
        "Stained": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_knife_push_aq_forced_light_png.png",
        "Urban Masked": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_knife_push_sp_tape_urban_light_png.png"
    },
    "Bowie Knife": {
        "Vanilla": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/weapons/base_weapons/weapon_knife_survival_bowie_png.png",
        "Blue Steel": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_knife_survival_bowie_aq_blued_light_png.png",
        "Boreal Forest": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_knife_survival_bowie_hy_forest_boreal_light_png.png",
        "Case Hardened": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_knife_survival_bowie_aq_oiled_light_png.png",
        "Crimson Web": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_knife_survival_bowie_hy_webs_light_png.png",
        "Fade": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_knife_survival_bowie_aa_fade_light_png.png",
        "Forest DDPAT": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_knife_survival_bowie_hy_ddpat_light_png.png",
        "Night": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_knife_survival_bowie_so_night_light_png.png",
        "Safari Mesh": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_knife_survival_bowie_sp_mesh_tan_light_png.png",
        "Scorched": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_knife_survival_bowie_sp_dapple_light_png.png",
        "Slaughter": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_knife_survival_bowie_am_zebra_light_png.png",
        "Stained": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_knife_survival_bowie_aq_forced_light_png.png",
        "Urban Masked": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_knife_survival_bowie_sp_tape_urban_light_png.png"
    }
}

# Glove images
glove_images = {
    "Bloodhound Gloves": {
        "Snakebite": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/studded_bloodhound_gloves_bloodhound_snakeskin_brass_light_png.png",
        "Bronzed": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/studded_bloodhound_gloves_bloodhound_metallic_light_png.png",
        "Charred": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/studded_bloodhound_gloves_bloodhound_black_silver_light_png.png",
        "Guerrilla": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/studded_bloodhound_gloves_bloodhound_guerrilla_light_png.png"
    },
    "Driver Gloves": {
        "Crimson Weave": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/slick_gloves_slick_red_light_png.png",
        "Convoy": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/slick_gloves_slick_military_light_png.png",
        "Lunar Weave": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/slick_gloves_slick_black_light_png.png",
        "Diamondback": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/slick_gloves_slick_snakeskin_yellow_light_png.png"
    },
    "Hand Wraps": {
        "Badlands": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/leather_handwraps_handwrap_fabric_orange_camo_light_png.png",
        "Leather": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/leather_handwraps_handwrap_leathery_light_png.png",
        "Duct Tape": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/leather_handwraps_handwrap_leathery_ducttape_light_png.png"
    },
    "Moto Gloves": {
        "Cool Mint": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/motorcycle_gloves_motorcycle_triangle_blue_light_png.png",
        "Boom!": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/motorcycle_gloves_motorcycle_mono_boom_light_png.png",
        "Spearmint": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/motorcycle_gloves_motorcycle_mint_triangle_light_png.png",
        "Eclipse": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/motorcycle_gloves_motorcycle_basic_black_light_png.png"
    },
    "Specialist Gloves": {
        "Crimson Kimono": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/specialist_gloves_specialist_kimono_diamonds_red_light_png.png",
        "Emerald Web": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/specialist_gloves_specialist_emerald_web_light_png.png",
        "Forest DDPAT": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/specialist_gloves_specialist_ddpat_green_camo_light_png.png",
        "Foundation": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/specialist_gloves_specialist_orange_white_light_png.png"
    },
    "Sport Gloves": {
        "Superconductor": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/sporty_gloves_sporty_light_blue_light_png.png",
        "Hedge Maze": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/sporty_gloves_sporty_green_light_png.png",
        "Arid": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/sporty_gloves_sporty_military_light_png.png"
    },
    "Hydra Gloves": {
        "Case Hardened": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/studded_hydra_gloves_bloodhound_hydra_case_hardened_light_png.png",
        "Emerald": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/studded_hydra_gloves_bloodhound_hydra_black_green_light_png.png",
        "Rattler": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/studded_hydra_gloves_bloodhound_hydra_snakeskin_brass_light_png.png",
        "Mangrove": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/studded_hydra_gloves_bloodhound_hydra_green_leather_mesh_brass_light_png.png"
    }
}

cases_with_skins = [
    {
        "title": "CS:GO Weapon Case",
        "skins": [
            {"weapon": "AWP", "pattern": "Lightning Strike", "quality": "Covert", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_awp_am_lightning_awp_light_png.png"},
            {"weapon": "AK-47", "pattern": "Case Hardened", "quality": "Classified", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_ak47_aq_oiled_light_png.png"},
            {"weapon": "Desert Eagle", "pattern": "Hypnotic", "quality": "Classified", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_deagle_aa_vertigo_light_png.png"},
            {"weapon": "Glock-18", "pattern": "Dragon Tattoo", "quality": "Restricted", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_glock_am_dragon_glock_light_png.png"},
            {"weapon": "M4A1-S", "pattern": "Dark Water", "quality": "Restricted", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_m4a1_silencer_am_zebra_dark_light_png.png"},
            {"weapon": "USP-S", "pattern": "Dark Water", "quality": "Restricted", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_usp_silencer_am_zebra_dark_light_png.png"},
            {"weapon": "SG 553", "pattern": "Ultraviolet", "quality": "Mil-Spec", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_sg556_so_purple_light_png.png"},
            {"weapon": "AUG", "pattern": "Wings", "quality": "Mil-Spec", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_aug_hy_feathers_aug_light_png.png"},
            {"weapon": "MP7", "pattern": "Skulls", "quality": "Mil-Spec", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_mp7_hy_skulls_light_png.png"}
        ],
        "knives": ["Bayonet", "Flip Knife", "Gut Knife", "Karambit", "M9 Bayonet"]
    },
    {
        "title": "eSports 2013 Case",
        "skins": [
            {"weapon": "P90", "pattern": "Death by Kitty", "quality": "Covert", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_p90_cu_catskulls_p90_light_png.png"},
            {"weapon": "AK-47", "pattern": "Red Laminate", "quality": "Classified", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_ak47_hy_ak47lam_light_png.png"},
            {"weapon": "AWP", "pattern": "BOOM", "quality": "Classified", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_awp_hy_blam_simple_light_png.png"},
            {"weapon": "M4A4", "pattern": "Faded Zebra", "quality": "Restricted", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_m4a1_sp_zebracam_bw_light_png.png"},
            {"weapon": "Galil AR", "pattern": "Orange DDPAT", "quality": "Restricted", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_galilar_hy_ddpat_orange_light_png.png"},
            {"weapon": "SCAR-20", "pattern": "Crimson Web", "quality": "Restricted", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_scar20_hy_webs_darker_light_png.png"},
            {"weapon": "FAMAS", "pattern": "Doomkitty", "quality": "Mil-Spec", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_famas_hy_doomkitty_light_png.png"},
            {"weapon": "MAG-7", "pattern": "Bulldozer", "quality": "Mil-Spec", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_mag7_so_yellow_light_png.png"},
            {"weapon": "P2000", "pattern": "Scorpion", "quality": "Mil-Spec", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_hkp2000_am_scorpion_p2000_light_png.png"}
        ],
        "knives": ["Bayonet", "Flip Knife", "Gut Knife", "Karambit", "M9 Bayonet"]
    },
    {
        "title": "CS:GO Weapon Case 2",
        "skins": [
            {"weapon": "SSG 08", "pattern": "Blood in the Water", "quality": "Covert", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_ssg08_cu_shark_light_png.png"},
            {"weapon": "P90", "pattern": "Cold Blooded", "quality": "Classified", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_p90_am_slither_p90_light_png.png"},
            {"weapon": "USP-S", "pattern": "Serum", "quality": "Classified", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_usp_silencer_am_electric_red_light_png.png"},
            {"weapon": "Five-SeveN", "pattern": "Case Hardened", "quality": "Restricted", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_fiveseven_aq_oiled_light_png.png"},
            {"weapon": "MP9", "pattern": "Rose Iron", "quality": "Restricted", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_mp9_am_thorny_rose_mp9_light_png.png"},
            {"weapon": "Nova", "pattern": "Graphite", "quality": "Restricted", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_nova_am_crumple_light_png.png"},
            {"weapon": "Dual Berettas", "pattern": "Black Limba", "quality": "Mil-Spec", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_elite_cu_season_elites_bravo_light_png.png"},
            {"weapon": "M4A1-S", "pattern": "Bright Water", "quality": "Mil-Spec", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_m4a1_silencer_hy_ocean_bravo_light_png.png"},
            {"weapon": "SCAR-20", "pattern": "Crimson Web", "quality": "Mil-Spec", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_scar20_hy_webs_darker_light_png.png"},
            {"weapon": "P250", "pattern": "Splash", "quality": "Mil-Spec", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_p250_sp_splash_p250_light_png.png"},
            {"weapon": "Tec-9", "pattern": "Blue Titanium", "quality": "Mil-Spec", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_tec9_an_titanium30v_light_png.png"},
            {"weapon": "FAMAS", "pattern": "Hexane", "quality": "Mil-Spec", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_famas_hy_bluehex_light_png.png"}
        ],
        "knives": ["Bayonet", "Flip Knife", "Gut Knife", "Karambit", "M9 Bayonet"]
    },
    {
        "title": "Winter Offensive Weapon Case",
        "skins": [
            {"weapon": "M4A4", "pattern": "Asiimov", "quality": "Covert", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_m4a1_cu_m4_asimov_light_png.png"},
            {"weapon": "AWP", "pattern": "Redline", "quality": "Classified", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_awp_cu_awp_cobra_light_png.png"},
            {"weapon": "Sawed-Off", "pattern": "The Kraken", "quality": "Classified", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_sawedoff_cu_sawedoff_octopump_light_png.png"},
            {"weapon": "P250", "pattern": "Mehndi", "quality": "Restricted", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_p250_cu_p250_refined_light_png.png"},
            {"weapon": "XM1014", "pattern": "Tranquility", "quality": "Restricted", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_xm1014_cu_xm1014_caritas_light_png.png"},
            {"weapon": "PP-Bizon", "pattern": "Cobalt Halftone", "quality": "Restricted", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_bizon_am_turqoise_halftone_light_png.png"},
            {"weapon": "Galil AR", "pattern": "Sandstorm", "quality": "Mil-Spec", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_galilar_cu_sandstorm_light_png.png"},
            {"weapon": "Five-SeveN", "pattern": "Kami", "quality": "Mil-Spec", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_fiveseven_hy_kami_light_png.png"},
            {"weapon": "M249", "pattern": "Magma", "quality": "Mil-Spec", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_m249_aq_obsidian_light_png.png"},
            {"weapon": "Dual Berettas", "pattern": "Marina", "quality": "Mil-Spec", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_elite_hy_marina_sunrise_light_png.png"},
            {"weapon": "Nova", "pattern": "Rising Skull", "quality": "Mil-Spec", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_nova_cu_skull_nova_light_png.png"}
        ],
        "knives": ["Bayonet", "Flip Knife", "Gut Knife", "Karambit", "M9 Bayonet"]
    },
    {
        "title": "eSports 2013 Winter Case",
        "skins": [
            {"weapon": "AWP", "pattern": "Electric Hive", "quality": "Covert", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_awp_hy_hive_light_png.png"},
            {"weapon": "M4A4", "pattern": "X-Ray", "quality": "Covert", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_m4a1_cu_xray_m4_light_png.png"},
            {"weapon": "Desert Eagle", "pattern": "Cobalt Disruption", "quality": "Classified", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_deagle_am_ddpatdense_peacock_light_png.png"},
            {"weapon": "P90", "pattern": "Blind Spot", "quality": "Restricted", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_p90_hy_modspots_light_png.png"},
            {"weapon": "USP-S", "pattern": "Stainless", "quality": "Restricted", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_usp_silencer_aq_usp_stainless_light_png.png"},
            {"weapon": "Glock-18", "pattern": "Blue Fissure", "quality": "Restricted", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_glock_hy_craquelure_light_png.png"},
            {"weapon": "Tec-9", "pattern": "Titanium Bit", "quality": "Mil-Spec", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_tec9_am_fluted_tec9_light_png.png"},
            {"weapon": "PP-Bizon", "pattern": "Water Sigil", "quality": "Mil-Spec", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_bizon_hy_water_crest_light_png.png"},
            {"weapon": "Nova", "pattern": "Ghost Camo", "quality": "Mil-Spec", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_nova_sp_camo_wood_blue_light_png.png"},
            {"weapon": "G3SG1", "pattern": "Azure Zebra", "quality": "Mil-Spec", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_g3sg1_sp_zebracam_blue_light_png.png"},
            {"weapon": "P250", "pattern": "Steel Disruption", "quality": "Mil-Spec", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_p250_am_ddpatdense_silver_light_png.png"},
            {"weapon": "AK-47", "pattern": "Blue Laminate", "quality": "Restricted", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_ak47_hy_ak47lam_blue_light_png.png"}
        ],
        "knives": ["Bayonet", "Flip Knife", "Gut Knife", "Karambit", "M9 Bayonet"]
    },
    {
        "title": "CS:GO Weapon Case 3",
        "skins": [
            {"weapon": "CZ75-Auto", "pattern": "Victoria", "quality": "Covert", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_cz75a_aq_etched_cz75_light_png.png"},
            {"weapon": "Desert Eagle", "pattern": "Heirloom", "quality": "Classified", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_deagle_aq_engraved_deagle_light_png.png"},
            {"weapon": "USP-S", "pattern": "Stainless", "quality": "Restricted", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_usp_silencer_aq_usp_stainless_light_png.png"},
            {"weapon": "P2000", "pattern": "Red FragCam", "quality": "Restricted", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_hkp2000_hy_poly_camo_light_png.png"},
            {"weapon": "Tec-9", "pattern": "Sandstorm", "quality": "Restricted", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_tec9_cu_tec9_sandstorm_light_png.png"},
            {"weapon": "CZ75-Auto", "pattern": "The Fuschia Is Now", "quality": "Restricted", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_cz75a_am_fuschia_light_png.png"},
            {"weapon": "Five-SeveN", "pattern": "Copper Galaxy", "quality": "Restricted", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_fiveseven_am_copper_flecks_light_png.png"},
            {"weapon": "P250", "pattern": "Undertow", "quality": "Classified", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_p250_am_p250_beaded_paint_light_png.png"},
            {"weapon": "Glock-18", "pattern": "Blue Fissure", "quality": "Mil-Spec", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_glock_hy_craquelure_light_png.png"},
            {"weapon": "Dual Berettas", "pattern": "Panther", "quality": "Mil-Spec", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_elite_so_panther_light_png.png"},
            {"weapon": "CZ75-Auto", "pattern": "Crimson Web", "quality": "Mil-Spec", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_cz75a_hy_webs_light_png.png"},
            {"weapon": "P2000", "pattern": "Pulse", "quality": "Mil-Spec", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_hkp2000_cu_p2000_pulse_light_png.png"}
        ],
        "knives": ["Bayonet", "Flip Knife", "Gut Knife", "Karambit", "M9 Bayonet"]
    },
    {
        "title": "Operation Phoenix Weapon Case",
        "skins": [
            {"weapon": "AWP", "pattern": "Asiimov", "quality": "Covert", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_awp_cu_awp_asimov_light_png.png"},
            {"weapon": "AUG", "pattern": "Chameleon", "quality": "Covert", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_aug_cu_aug_chameleonaire_light_png.png"},
            {"weapon": "AK-47", "pattern": "Redline", "quality": "Classified", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_ak47_cu_ak47_cobra_light_png.png"},
            {"weapon": "Nova", "pattern": "Antique", "quality": "Classified", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_nova_cu_nova_antique_light_png.png"},
            {"weapon": "P90", "pattern": "Trigon", "quality": "Classified", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_p90_cu_p90_trigon_light_png.png"},
            {"weapon": "FAMAS", "pattern": "Sergeant", "quality": "Restricted", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_famas_an_famas_sgt_light_png.png"},
            {"weapon": "USP-S", "pattern": "Guardian", "quality": "Restricted", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_usp_silencer_cu_usp_elegant_light_png.png"},
            {"weapon": "P250", "pattern": "Mehndi", "quality": "Restricted", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_p250_cu_p250_refined_light_png.png"},
            {"weapon": "UMP-45", "pattern": "Corporal", "quality": "Mil-Spec", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_ump45_cu_ump_corporal_light_png.png"},
            {"weapon": "MAG-7", "pattern": "Heaven Guard", "quality": "Mil-Spec", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_mag7_cu_mag7_heaven_light_png.png"},
            {"weapon": "MAC-10", "pattern": "Heat", "quality": "Mil-Spec", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_mac10_cu_mac10_redhot_light_png.png"},
            {"weapon": "SG 553", "pattern": "Pulse", "quality": "Mil-Spec", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_sg556_cu_sg553_pulse_light_png.png"},
            {"weapon": "Negev", "pattern": "Terrain", "quality": "Mil-Spec", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_negev_sp_negev_turq_terrain_light_png.png"}
        ],
        "knives": ["Bayonet", "Flip Knife", "Gut Knife", "Karambit", "M9 Bayonet"]
    },
    {
        "title": "Huntsman Weapon Case",
        "skins": [
            {"weapon": "AK-47", "pattern": "Vulcan", "quality": "Covert", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_ak47_cu_ak47_rubber_light_png.png"},
            {"weapon": "M4A1-S", "pattern": "Atomic Alloy", "quality": "Covert", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_m4a1_silencer_am_m4a1-s_alloy_orange_light_png.png"},
            {"weapon": "USP-S", "pattern": "Caiman", "quality": "Classified", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_usp_silencer_cu_kaiman_light_png.png"},
            {"weapon": "SCAR-20", "pattern": "Cyrex", "quality": "Classified", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_scar20_cu_scar_cyrex_light_png.png"},
            {"weapon": "M4A4", "pattern": "Desert-Strike", "quality": "Classified", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_m4a1_cu_titanstorm_light_png.png"},
            {"weapon": "MAC-10", "pattern": "Tatter", "quality": "Restricted", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_mac10_cu_korupt_light_png.png"},
            {"weapon": "PP-Bizon", "pattern": "Antique", "quality": "Restricted", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_bizon_cu_bizon_antique_light_png.png"},
            {"weapon": "XM1014", "pattern": "Heaven Guard", "quality": "Restricted", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_xm1014_cu_xm1014_heaven_guard_light_png.png"},
            {"weapon": "P90", "pattern": "Module", "quality": "Mil-Spec", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_p90_an_royalbleed_light_png.png"},
            {"weapon": "CZ75-Auto", "pattern": "Twist", "quality": "Mil-Spec", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_cz75a_am_gyrate_light_png.png"},
            {"weapon": "AUG", "pattern": "Torque", "quality": "Mil-Spec", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_aug_cu_aug_progressiv_light_png.png"},
            {"weapon": "Tec-9", "pattern": "Isaac", "quality": "Mil-Spec", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_tec9_cu_tec9_asiimov_light_png.png"},
            {"weapon": "SSG 08", "pattern": "Slashed", "quality": "Mil-Spec", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_ssg08_cu_ssg08_immortal_light_png.png"},
            {"weapon": "Galil AR", "pattern": "Kami", "quality": "Mil-Spec", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_galilar_hy_galil_kami_light_png.png"}
        ],
        "knives": ["Huntsman Knife"]
    },
    {
        "title": "Operation Breakout Weapon Case",
        "skins": [
            {"weapon": "M4A1-S", "pattern": "Cyrex", "quality": "Covert", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_m4a1_silencer_cu_m4a1s_cyrex_light_png.png"},
            {"weapon": "P90", "pattern": "Asiimov", "quality": "Covert", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_p90_cu_p90-asiimov_light_png.png"},
            {"weapon": "Glock-18", "pattern": "Water Elemental", "quality": "Classified", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_glock_cu_glock-liquescent_light_png.png"},
            {"weapon": "Desert Eagle", "pattern": "Conspiracy", "quality": "Classified", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_deagle_cu_deagle_aureus_light_png.png"},
            {"weapon": "P250", "pattern": "Supernova", "quality": "Classified", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_p250_cu_bittersweet_light_png.png"},
            {"weapon": "Five-SeveN", "pattern": "Fowl Play", "quality": "Restricted", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_fiveseven_aq_57_feathers_light_png.png"},
            {"weapon": "Nova", "pattern": "Koi", "quality": "Restricted", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_nova_cu_nova_koi_light_png.png"},
            {"weapon": "PP-Bizon", "pattern": "Osiris", "quality": "Restricted", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_bizon_cu_bizon-osiris_light_png.png"},
            {"weapon": "SSG 08", "pattern": "Abyss", "quality": "Mil-Spec", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_ssg08_aq_leviathan_light_png.png"},
            {"weapon": "UMP-45", "pattern": "Labyrinth", "quality": "Mil-Spec", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_ump45_hy_lines_orange_light_png.png"},
            {"weapon": "MP7", "pattern": "Urban Hazard", "quality": "Mil-Spec", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_mp7_cu_mp7-commander_light_png.png"},
            {"weapon": "CZ75-Auto", "pattern": "Tigris", "quality": "Mil-Spec", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_cz75a_cu_c75a-tiger_light_png.png"},
            {"weapon": "Negev", "pattern": "Desert-Strike", "quality": "Mil-Spec", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_negev_cu_negev_titanstorm_light_png.png"}
        ],
        "knives": ["Butterfly Knife"]
    },
    {
        "title": "eSports 2014 Summer Case",
        "skins": [
            {"weapon": "Nova", "pattern": "Bloomstick", "quality": "Covert", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_nova_cu_spring_nova_light_png.png"},
            {"weapon": "AWP", "pattern": "Corticera", "quality": "Classified", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_awp_cu_favela_awp_light_png.png"},
            {"weapon": "P90", "pattern": "Virus", "quality": "Classified", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_p90_hy_zombie_light_png.png"},
            {"weapon": "M4A4", "pattern": "Bullet Rain", "quality": "Classified", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_m4a1_cu_bullet_rain_m4a1_light_png.png"},
            {"weapon": "AK-47", "pattern": "Jaguar", "quality": "Classified", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_ak47_cu_panther_ak47_light_png.png"},
            {"weapon": "Desert Eagle", "pattern": "Crimson Web", "quality": "Restricted", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_deagle_hy_webs_darker_light_png.png"},
            {"weapon": "MP7", "pattern": "Ocean Foam", "quality": "Restricted", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_mp7_am_ossify_blue_light_png.png"},
            {"weapon": "Glock-18", "pattern": "Steel Disruption", "quality": "Restricted", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_glock_am_ddpatdense_silver_light_png.png"},
            {"weapon": "AUG", "pattern": "Bengal Tiger", "quality": "Restricted", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_aug_hy_tiger_light_png.png"},
            {"weapon": "FAMAS", "pattern": "Styx", "quality": "Restricted", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_famas_am_nuclear_skulls2_famas_light_png.png"},
            {"weapon": "CZ75-Auto", "pattern": "Hexane", "quality": "Mil-Spec", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_cz75a_hy_bluehex_light_png.png"},
            {"weapon": "Negev", "pattern": "Bratatat", "quality": "Mil-Spec", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_negev_cu_bratatat_negev_light_png.png"}
        ],
        "knives": ["Butterfly Knife"]
    },
    {
        "title": "Operation Vanguard Weapon Case",
        "skins": [
            {"weapon": "AK-47", "pattern": "Wasteland Rebel", "quality": "Covert", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_ak47_cu_tribute_ak47_light_png.png"},
            {"weapon": "P2000", "pattern": "Fire Elemental", "quality": "Covert", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_hkp2000_cu_p2000_fire_elemental_light_png.png"},
            {"weapon": "M4A4", "pattern": "Griffin", "quality": "Classified", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_m4a1_cu_m4a4_griffin_light_png.png"},
            {"weapon": "M4A1-S", "pattern": "Basilisk", "quality": "Classified", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_m4a1_silencer_aq_m4a1s_basilisk_light_png.png"},
            {"weapon": "SCAR-20", "pattern": "Cardiac", "quality": "Classified", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_scar20_cu_scar20_intervention_light_png.png"},
            {"weapon": "XM1014", "pattern": "Tranquility", "quality": "Restricted", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_xm1014_cu_xm1014_caritas_light_png.png"},
            {"weapon": "Glock-18", "pattern": "Grinder", "quality": "Restricted", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_glock_aq_glock_coiled_light_png.png"},
            {"weapon": "P250", "pattern": "Cartel", "quality": "Restricted", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_p250_aq_p250_cartel_light_png.png"},
            {"weapon": "Galil AR", "pattern": "Firefight", "quality": "Mil-Spec", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_galilar_gs_galilar_incenerator_light_png.png"},
            {"weapon": "MP7", "pattern": "Skulls", "quality": "Mil-Spec", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_mp7_hy_skulls_light_png.png"},
            {"weapon": "UMP-45", "pattern": "Delusion", "quality": "Mil-Spec", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_ump45_sp_ump45_d-visions_light_png.png"},
            {"weapon": "MAG-7", "pattern": "Firestarter", "quality": "Mil-Spec", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_mag7_sp_mag7_firebitten_light_png.png"},
            {"weapon": "Sawed-Off", "pattern": "Highwayman", "quality": "Mil-Spec", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_sawedoff_aq_sawedoff_blackgold_light_png.png"}
        ],
        "knives": ["Bayonet", "Flip Knife", "Gut Knife", "Karambit", "M9 Bayonet"]
    },
    {
        "title": "Chroma Case",
        "skins": [
            {"weapon": "Galil AR", "pattern": "Chatterbox", "quality": "Covert", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_galilar_cu_galil_abrasion_light_png.png"},
            {"weapon": "AWP", "pattern": "Man-o'-war", "quality": "Covert", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_awp_am_awp_glory_light_png.png"},
            {"weapon": "M4A4", "pattern": "Dragon King", "quality": "Classified", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_m4a1_cu_m4a4_ancestral_light_png.png"},
            {"weapon": "AK-47", "pattern": "Cartel", "quality": "Classified", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_ak47_aq_ak47_cartel_light_png.png"},
            {"weapon": "Dual Berettas", "pattern": "Urban Shock", "quality": "Restricted", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_elite_cu_elites_urbanstorm_light_png.png"},
            {"weapon": "Desert Eagle", "pattern": "Naga", "quality": "Restricted", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_deagle_aq_deagle_naga_light_png.png"},
            {"weapon": "MAC-10", "pattern": "Malachite", "quality": "Restricted", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_mac10_am_mac10_malachite_light_png.png"},
            {"weapon": "Sawed-Off", "pattern": "Serenity", "quality": "Restricted", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_sawedoff_cu_sawedoff_deva_light_png.png"},
            {"weapon": "P250", "pattern": "Muertos", "quality": "Mil-Spec", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_p250_cu_p250_mandala_light_png.png"},
            {"weapon": "Glock-18", "pattern": "Catacombs", "quality": "Mil-Spec", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_glock_cu_glock_deathtoll_light_png.png"},
            {"weapon": "M249", "pattern": "System Lock", "quality": "Mil-Spec", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_m249_cu_m249_sektor_light_png.png"},
            {"weapon": "MP9", "pattern": "Deadly Poison", "quality": "Mil-Spec", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_mp9_cu_mp9_deadly_poison_light_png.png"},
            {"weapon": "SCAR-20", "pattern": "Grotto", "quality": "Mil-Spec", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_scar20_aq_scar20_leak_light_png.png"},
            {"weapon": "XM1014", "pattern": "Quicksilver", "quality": "Mil-Spec", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_xm1014_aq_xm1014_sigla_light_png.png"}
        ],
        "knives": ["Bayonet", "Flip Knife", "Gut Knife", "Karambit", "M9 Bayonet"]
    },
    {
        "title": "Chroma 2 Case",
        "skins": [
            {"weapon": "M4A1-S", "pattern": "Hyper Beast", "quality": "Covert", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_m4a1_silencer_cu_m4a1_hyper_beast_light_png.png"},
            {"weapon": "MAC-10", "pattern": "Neon Rider", "quality": "Covert", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_mac10_cu_mac10_neonrider_light_png.png"},
            {"weapon": "Galil AR", "pattern": "Eco", "quality": "Classified", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_galilar_cu_galil_eco_light_png.png"},
            {"weapon": "FAMAS", "pattern": "Djinn", "quality": "Classified", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_famas_aq_famas_jinn_light_png.png"},
            {"weapon": "Five-SeveN", "pattern": "Monkey Business", "quality": "Classified", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_fiveseven_cu_fiveseven_banana_light_png.png"},
            {"weapon": "AWP", "pattern": "Worm God", "quality": "Restricted", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_awp_aq_awp_twine_light_png.png"},
            {"weapon": "MAG-7", "pattern": "Heat", "quality": "Restricted", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_mag7_cu_mag7_redhot_light_png.png"},
            {"weapon": "CZ75-Auto", "pattern": "Pole Position", "quality": "Restricted", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_cz75a_cu_cz75_precision_light_png.png"},
            {"weapon": "UMP-45", "pattern": "Grand Prix", "quality": "Restricted", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_ump45_am_ump_racer_light_png.png"},
            {"weapon": "Desert Eagle", "pattern": "Bronze Deco", "quality": "Mil-Spec", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_deagle_am_bronze_sparkle_light_png.png"},
            {"weapon": "P250", "pattern": "Valence", "quality": "Mil-Spec", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_p250_aq_p250_contour_light_png.png"},
            {"weapon": "Negev", "pattern": "Man-o'-war", "quality": "Mil-Spec", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_negev_am_negev_glory_light_png.png"},
            {"weapon": "MP7", "pattern": "Armor Core", "quality": "Mil-Spec", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_mp7_aq_mp7_ultramodern_light_png.png"},
            {"weapon": "Sawed-Off", "pattern": "Origami", "quality": "Mil-Spec", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_sawedoff_cu_sawedoff_origami_light_png.png"},
            {"weapon": "AK-47", "pattern": "Elite Build", "quality": "Mil-Spec", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_ak47_cu_ak47_mastery_light_png.png"}
        ],
        "knives": ["Bayonet", "Flip Knife", "Gut Knife", "Karambit", "M9 Bayonet"]
    },
    {
        "title": "Falchion Case",
        "skins": [
            {"weapon": "AWP", "pattern": "Hyper Beast", "quality": "Covert", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_awp_cu_awp_hyper_beast_light_png.png"},
            {"weapon": "AK-47", "pattern": "Aquamarine Revenge", "quality": "Covert", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_ak47_cu_ak47_courage_alt_light_png.png"},
            {"weapon": "SG 553", "pattern": "Cyrex", "quality": "Classified", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_sg556_cu_sg553_cyrex_light_png.png"},
            {"weapon": "M4A4", "pattern": "Evil Daimyo", "quality": "Classified", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_m4a1_cu_m4a4_evil_daimyo_light_png.png"},
            {"weapon": "FAMAS", "pattern": "Neural Net", "quality": "Classified", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_famas_am_famas_dots_light_png.png"},
            {"weapon": "MP9", "pattern": "Ruby Poison Dart", "quality": "Restricted", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_mp9_am_mp9_nitrogen_light_png.png"},
            {"weapon": "Negev", "pattern": "Loudmouth", "quality": "Restricted", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_negev_cu_negev_annihilator_light_png.png"},
            {"weapon": "P2000", "pattern": "Handgun", "quality": "Restricted", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_hkp2000_aq_p2000_boom_light_png.png"},
            {"weapon": "CZ75-Auto", "pattern": "Yellow Jacket", "quality": "Restricted", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_cz75a_cu_cz75a_chastizer_light_png.png"},
            {"weapon": "MP7", "pattern": "Nemesis", "quality": "Restricted", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_mp7_cu_mp7_nemsis_light_png.png"},
            {"weapon": "Galil AR", "pattern": "Rocket Pop", "quality": "Mil-Spec", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_galilar_cu_galilar_particles_light_png.png"},
            {"weapon": "Glock-18", "pattern": "Bunsen Burner", "quality": "Mil-Spec", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_glock_aq_glock18_flames_blue_light_png.png"},
            {"weapon": "Nova", "pattern": "Ranger", "quality": "Mil-Spec", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_nova_cu_nova_ranger_light_png.png"},
            {"weapon": "UMP-45", "pattern": "Riot", "quality": "Mil-Spec", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_ump45_cu_ump45_uproar_light_png.png"},
            {"weapon": "USP-S", "pattern": "Torque", "quality": "Mil-Spec", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_usp_silencer_cu_usp_progressiv_light_png.png"}
        ],
        "knives": ["Falchion Knife"]
    },
    {
        "title": "Shadow Case",
        "skins": [
            {"weapon": "M4A1-S", "pattern": "Golden Coil", "quality": "Covert", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_m4a1_silencer_gs_m4a1s_snakebite_gold_light_png.png"},
            {"weapon": "USP-S", "pattern": "Kill Confirmed", "quality": "Covert", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_usp_silencer_cu_usp_kill_confirmed_light_png.png"},
            {"weapon": "AK-47", "pattern": "Frontside Misty", "quality": "Classified", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_ak47_cu_ak47_winter_sport_light_png.png"},
            {"weapon": "G3SG1", "pattern": "Flux", "quality": "Classified", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_g3sg1_gs_g3sg1_flux_purple_light_png.png"},
            {"weapon": "SSG 08", "pattern": "Big Iron", "quality": "Classified", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_ssg08_cu_ssg08_technicality_light_png.png"},
            {"weapon": "P250", "pattern": "Wingshot", "quality": "Restricted", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_p250_hy_p250_crackshot_light_png.png"},
            {"weapon": "Galil AR", "pattern": "Stone Cold", "quality": "Restricted", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_galilar_gs_galil_nightwing_light_png.png"},
            {"weapon": "M249", "pattern": "Nebula Crusader", "quality": "Restricted", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_m249_gs_m249_nebula_crusader_light_png.png"},
            {"weapon": "MP7", "pattern": "Special Delivery", "quality": "Restricted", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_mp7_cu_mp7_classified_light_png.png"},
            {"weapon": "Glock-18", "pattern": "Wraiths", "quality": "Mil-Spec", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_glock_gs_glock18_wrathys_light_png.png"},
            {"weapon": "Dual Berettas", "pattern": "Dualing Dragons", "quality": "Mil-Spec", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_elite_cu_dualberretta_dragons_light_png.png"},
            {"weapon": "XM1014", "pattern": "Scumbria", "quality": "Mil-Spec", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_xm1014_aq_xm1014_scumbria_light_png.png"},
            {"weapon": "MAG-7", "pattern": "Cobalt Core", "quality": "Mil-Spec", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_mag7_cu_mag7_myrcene_light_png.png"},
            {"weapon": "SCAR-20", "pattern": "Green Marine", "quality": "Mil-Spec", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_scar20_gs_scar20_peacemaker03_light_png.png"},
            {"weapon": "Tec-9", "pattern": "Ice Cap", "quality": "Mil-Spec", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_tec9_am_tec_9_sea_salt_light_png.png"}
        ],
        "knives": ["Shadow Daggers"]
    },
    {
        "title": "Revolver Case",
        "skins": [
            {"weapon": "M4A4", "pattern": "Royal Paladin", "quality": "Covert", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_m4a1_gs_m4a4_royal_squire_light_png.png"},
            {"weapon": "R8 Revolver", "pattern": "Fade", "quality": "Covert", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_revolver_aa_fade_revolver_light_png.png"},
            {"weapon": "AK-47", "pattern": "Point Disarray", "quality": "Classified", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_ak47_cu_ak47_point_disarray_light_png.png"},
            {"weapon": "G3SG1", "pattern": "The Executioner", "quality": "Classified", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_g3sg1_cu_g3sg1_executioner_light_png.png"},
            {"weapon": "P90", "pattern": "Shapewood", "quality": "Classified", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_p90_cu_p90_shapewood_light_png.png"},
            {"weapon": "Tec-9", "pattern": "Avalanche", "quality": "Restricted", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_tec9_cu_tec9_avalanche_light_png.png"},
            {"weapon": "SG 553", "pattern": "Tiger Moth", "quality": "Restricted", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_sg556_gs_sg553_tiger_moth_light_png.png"},
            {"weapon": "Five-SeveN", "pattern": "Retrobution", "quality": "Restricted", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_fiveseven_cu_fiveseven_retrobution_light_png.png"},
            {"weapon": "Negev", "pattern": "Power Loader", "quality": "Restricted", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_negev_cu_negev_impact_light_png.png"},
            {"weapon": "XM1014", "pattern": "Teclu Burner", "quality": "Mil-Spec", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_xm1014_aq_xm1014_hot_rod_light_png.png"},
            {"weapon": "PP-Bizon", "pattern": "Fuel Rod", "quality": "Mil-Spec", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_bizon_cu_bizon_noxious_light_png.png"},
            {"weapon": "Desert Eagle", "pattern": "Corinthian", "quality": "Mil-Spec", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_deagle_aq_deagle_corinthian_light_png.png"},
            {"weapon": "AUG", "pattern": "Ricochet", "quality": "Mil-Spec", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_aug_am_aug_jumble_light_png.png"},
            {"weapon": "P2000", "pattern": "Imperial", "quality": "Mil-Spec", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_hkp2000_am_p2000_imperial_red_light_png.png"},
            {"weapon": "Sawed-Off", "pattern": "Yorick", "quality": "Mil-Spec", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_sawedoff_gs_sawedoff_necromancer_light_png.png"}
        ],
        "knives": ["Bayonet", "Flip Knife", "Gut Knife", "Karambit", "M9 Bayonet"]
    },
    {
        "title": "Operation Wildfire Case",
        "skins": [
            {"weapon": "AWP", "pattern": "Elite Build", "quality": "Covert", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_awp_cu_awp_mastery_light_png.png"},
            {"weapon": "AK-47", "pattern": "Fuel Injector", "quality": "Covert", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_ak47_gs_ak47_supercharged_light_png.png"},
            {"weapon": "M4A4", "pattern": "The Battlestar", "quality": "Classified", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_m4a1_gs_m4a4_pioneer_light_png.png"},
            {"weapon": "Desert Eagle", "pattern": "Kumicho Dragon", "quality": "Classified", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_deagle_aq_deserteagle_kumichodragon_light_png.png"},
            {"weapon": "Nova", "pattern": "Hyper Beast", "quality": "Classified", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_nova_cu_nova_hyperbeast_light_png.png"},
            {"weapon": "Glock-18", "pattern": "Royal Legion", "quality": "Restricted", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_glock_gs_glock18_award_light_png.png"},
            {"weapon": "FAMAS", "pattern": "Valence", "quality": "Restricted", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_famas_aq_famas_contour_light_png.png"},
            {"weapon": "MAG-7", "pattern": "Praetorian", "quality": "Restricted", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_mag7_gs_mag7_praetorian_light_png.png"},
            {"weapon": "Five-SeveN", "pattern": "Triumvirate", "quality": "Restricted", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_fiveseven_cu_fiveseven_augmented_light_png.png"},
            {"weapon": "PP-Bizon", "pattern": "Photic Zone", "quality": "Mil-Spec", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_bizon_cu_bizon_citizen_light_png.png"},
            {"weapon": "Dual Berettas", "pattern": "Cartel", "quality": "Mil-Spec", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_elite_aq_dualberettas_cartel_light_png.png"},
            {"weapon": "MP7", "pattern": "Impire", "quality": "Mil-Spec", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_mp7_sp_mp7_impire_light_png.png"},
            {"weapon": "SSG 08", "pattern": "Necropos", "quality": "Mil-Spec", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_ssg08_cu_ssg08_necropos_light_png.png"},
            {"weapon": "USP-S", "pattern": "Lead Conduit", "quality": "Mil-Spec", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_usp_silencer_gs_usp_voltage_light_png.png"},
            {"weapon": "Tec-9", "pattern": "Jambiya", "quality": "Mil-Spec", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_tec9_gs_tec9_jambiya_light_png.png"}
        ],
        "knives": ["Bowie Knife"]
    },
    {
        "title": "Chroma 3 Case",
        "skins": [
            {"weapon": "M4A1-S", "pattern": "Chantico's Fire", "quality": "Covert", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_m4a1_silencer_cu_m4a1s_soultaker_light_png.png"},
            {"weapon": "PP-Bizon", "pattern": "Judgement of Anubis", "quality": "Covert", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_bizon_cu_bizon_curse_light_png.png"},
            {"weapon": "AUG", "pattern": "Fleet Flock", "quality": "Classified", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_aug_cu_aug_swallows_light_png.png"},
            {"weapon": "P250", "pattern": "Asiimov", "quality": "Classified", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_p250_cu_p250_asiimov_light_png.png"},
            {"weapon": "UMP-45", "pattern": "Primal Saber", "quality": "Classified", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_ump45_cu_ump45_primalsaber_light_png.png"},
            {"weapon": "Dual Berettas", "pattern": "Ventilators", "quality": "Restricted", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_elite_gs_dualberettas_ventilators_light_png.png"},
            {"weapon": "G3SG1", "pattern": "Orange Crash", "quality": "Restricted", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_g3sg1_sp_g3sg1_militiaorange_light_png.png"},
            {"weapon": "P2000", "pattern": "Oceanic", "quality": "Restricted", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_hkp2000_hy_p2000_oceani_light_png.png"},
            {"weapon": "Tec-9", "pattern": "Re-Entry", "quality": "Restricted", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_tec9_am_tec9_redblast_light_png.png"},
            {"weapon": "XM1014", "pattern": "Black Tie", "quality": "Restricted", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_xm1014_cu_xm1014_spectrum_light_png.png"},
            {"weapon": "CZ75-Auto", "pattern": "Red Astor", "quality": "Mil-Spec", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_cz75a_gs_cz75a_redastor_light_png.png"},
            {"weapon": "Galil AR", "pattern": "Firefight", "quality": "Mil-Spec", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_galilar_gs_galilar_incenerator_light_png.png"},
            {"weapon": "SSG 08", "pattern": "Ghost Crusader", "quality": "Mil-Spec", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_ssg08_gs_ssg08_armacore_light_png.png"},
            {"weapon": "SG 553", "pattern": "Atlas", "quality": "Mil-Spec", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_sg556_cu_sg553_atlas_light_png.png"},
            {"weapon": "M249", "pattern": "Spectre", "quality": "Mil-Spec", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_m249_cu_m249_spectre_light_png.png"},
            {"weapon": "MP9", "pattern": "Bioleak", "quality": "Mil-Spec", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_mp9_am_mp9_bioleak_light_png.png"}
        ],
        "knives": ["Bayonet", "Flip Knife", "Gut Knife", "Karambit", "M9 Bayonet"]
    },
    {
        "title": "Gamma Case",
        "skins": [
            {"weapon": "M4A1-S", "pattern": "Mecha Industries", "quality": "Covert", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_m4a1_silencer_gs_m4a1_mecha_industries_light_png.png"},
            {"weapon": "Glock-18", "pattern": "Wasteland Rebel", "quality": "Covert", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_glock_cu_glock_wasteland_rebel_light_png.png"},
            {"weapon": "M4A4", "pattern": "Desolate Space", "quality": "Classified", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_m4a1_cu_m4a4_desolate_space_light_png.png"},
            {"weapon": "SCAR-20", "pattern": "Bloodsport", "quality": "Classified", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_scar20_gs_scar20_bloodsport_light_png.png"},
            {"weapon": "P90", "pattern": "Chopper", "quality": "Classified", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_p90_gs_p90_full_throttle_light_png.png"},
            {"weapon": "R8 Revolver", "pattern": "Reboot", "quality": "Restricted", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_revolver_cu_r8_cybersport_light_png.png"},
            {"weapon": "P250", "pattern": "Iron Clad", "quality": "Restricted", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_p250_gs_p250_metal_panels_light_png.png"},
            {"weapon": "Five-SeveN", "pattern": "Violent Daimyo", "quality": "Restricted", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_fiveseven_cu_five_seven_daimyo_light_png.png"},
            {"weapon": "AUG", "pattern": "Syd Mead", "quality": "Restricted", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_aug_gs_aug_syd_mead_light_png.png"},
            {"weapon": "MP9", "pattern": "Airlock", "quality": "Restricted", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_mp9_cu_mp9_narcis_light_png.png"},
            {"weapon": "Tec-9", "pattern": "Ice Cap", "quality": "Mil-Spec", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_tec9_am_tec_9_sea_salt_light_png.png"},
            {"weapon": "SG 553", "pattern": "Aerial", "quality": "Mil-Spec", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_sg556_cu_sg553_aerial_light_png.png"},
            {"weapon": "P2000", "pattern": "Imperial Dragon", "quality": "Mil-Spec", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_hkp2000_gs_p2000_imperial_dragon_light_png.png"},
            {"weapon": "AWP", "pattern": "Phobos", "quality": "Mil-Spec", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_awp_gs_awp_phobos_light_png.png"},
            {"weapon": "Glock-18", "pattern": "Weasel", "quality": "Mil-Spec", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_glock_cu_glock18_weasel_light_png.png"},
            {"weapon": "Sawed-Off", "pattern": "Limelight", "quality": "Mil-Spec", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_sawedoff_cu_sawed_off_lime_light_png.png"}
        ],
        "knives": ["Bayonet", "Flip Knife", "Gut Knife", "Karambit", "M9 Bayonet"]
    },
    {
        "title": "Gamma 2 Case",
        "skins": [
            {"weapon": "AK-47", "pattern": "Neon Revolution", "quality": "Covert", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_ak47_cu_ak47_anarchy_light_png.png"},
            {"weapon": "FAMAS", "pattern": "Roll Cage", "quality": "Covert", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_famas_gs_famas_rally_light_png.png"},
            {"weapon": "Tec-9", "pattern": "Fuel Injector", "quality": "Classified", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_tec9_gs_tec9_supercharged_light_png.png"},
            {"weapon": "AUG", "pattern": "Triqua", "quality": "Classified", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_aug_cu_aug_orange_triangle_light_png.png"},
            {"weapon": "MP9", "pattern": "Goo", "quality": "Classified", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_mp9_cu_mp9_goo_light_png.png"},
            {"weapon": "SCAR-20", "pattern": "Powercore", "quality": "Restricted", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_scar20_gs_scar20_powercore_light_png.png"},
            {"weapon": "MAG-7", "pattern": "Petroglyph", "quality": "Restricted", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_mag7_cu_mag7_tribal_light_png.png"},
            {"weapon": "Desert Eagle", "pattern": "Directive", "quality": "Restricted", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_deagle_aq_desert_eagle_constable_light_png.png"},
            {"weapon": "Glock-18", "pattern": "Ironwork", "quality": "Restricted", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_glock_aq_glock_dark-fall_light_png.png"},
            {"weapon": "CZ75-Auto", "pattern": "Imprint", "quality": "Mil-Spec", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_cz75a_gs_cz75_tread_light_png.png"},
            {"weapon": "G3SG1", "pattern": "Ventilator", "quality": "Mil-Spec", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_g3sg1_gs_g3sg1_ventilator_light_png.png"},
            {"weapon": "M4A1-S", "pattern": "Briefing", "quality": "Mil-Spec", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_m4a1_silencer_cu_m4a1s_metritera_light_png.png"},
            {"weapon": "P90", "pattern": "Grim", "quality": "Mil-Spec", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_p90_cu_p90_grimm_light_png.png"},
            {"weapon": "XM1014", "pattern": "Slipstream", "quality": "Mil-Spec", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_xm1014_hy_xm1014_fractal_blue_light_png.png"},
            {"weapon": "UMP-45", "pattern": "Briefing", "quality": "Mil-Spec", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_ump45_cu_ump45_metritera_light_png.png"},
            {"weapon": "Five-SeveN", "pattern": "Scumbria", "quality": "Mil-Spec", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_fiveseven_aq_five_seven_scumbria_light_png.png"}
        ],
        "knives": ["Bayonet", "Flip Knife", "Gut Knife", "Karambit", "M9 Bayonet"]
    },
    {
        "title": "Glove Case",
        "skins": [
            {"weapon": "M4A4", "pattern": "Buzz Kill", "quality": "Covert", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_m4a1_gs_m4a4_sector_light_png.png"},
            {"weapon": "SSG 08", "pattern": "Dragonfire", "quality": "Covert", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_ssg08_cu_ssg08_dragonfire_scope_light_png.png"},
            {"weapon": "P90", "pattern": "Shallow Grave", "quality": "Classified", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_p90_gs_p90_shallow_grave_light_png.png"},
            {"weapon": "SCAR-20", "pattern": "Powercore", "quality": "Classified", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_scar20_gs_scar20_powercore_light_png.png"},
            {"weapon": "Sawed-Off", "pattern": "Wasteland Princess", "quality": "Classified", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_sawedoff_cu_wp_sawedoff_light_png.png"},
            {"weapon": "USP-S", "pattern": "Cyrex", "quality": "Restricted", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_usp_silencer_cu_usp_cyrex_light_png.png"},
            {"weapon": "FAMAS", "pattern": "Mecha Industries", "quality": "Restricted", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_famas_gs_famas_mecha_light_png.png"},
            {"weapon": "M4A1-S", "pattern": "Flashback", "quality": "Restricted", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_m4a1_silencer_cu_m4a1_flashback_light_png.png"},
            {"weapon": "Nova", "pattern": "Gila", "quality": "Restricted", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_nova_am_nova_sand_light_png.png"},
            {"weapon": "G3SG1", "pattern": "Stinger", "quality": "Mil-Spec", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_g3sg1_gs_g3sg1_viper_yellow_light_png.png"},
            {"weapon": "Dual Berettas", "pattern": "Royal Consorts", "quality": "Mil-Spec", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_elite_gs_dual_berettas_golden_venice_light_png.png"},
            {"weapon": "Glock-18", "pattern": "Ironwork", "quality": "Mil-Spec", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_glock_aq_glock_dark-fall_light_png.png"},
            {"weapon": "MP7", "pattern": "Cirrus", "quality": "Mil-Spec", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_mp7_gs_final_pooldeadv2_light_png.png"},
            {"weapon": "Galil AR", "pattern": "Black Sand", "quality": "Mil-Spec", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_galilar_cu_galil_ar-camo_light_png.png"},
            {"weapon": "MP9", "pattern": "Sand Scale", "quality": "Mil-Spec", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_mp9_aa_hide-mp9_light_png.png"},
            {"weapon": "MAG-7", "pattern": "Sonar", "quality": "Mil-Spec", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_mag7_am_mag7_malform_light_png.png"},
            {"weapon": "P2000", "pattern": "Turf", "quality": "Mil-Spec", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_hkp2000_gs_p2000-sport_light_png.png"}
        ],
        "gloves": ["Bloodhound Gloves", "Driver Gloves", "Hand Wraps", "Moto Gloves", "Specialist Gloves", "Sport Gloves"]
    },
    {
        "title": "Spectrum Case",
        "skins": [
            {"weapon": "AK-47", "pattern": "Bloodsport", "quality": "Covert", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_ak47_gs_ak47_bloodsport_light_png.png"},
            {"weapon": "USP-S", "pattern": "Neo-Noir", "quality": "Covert", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_usp_silencer_cu_usps_noir_light_png.png"},
            {"weapon": "M4A1-S", "pattern": "Decimator", "quality": "Classified", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_m4a1_silencer_gs_m4a1_decimator_light_png.png"},
            {"weapon": "AWP", "pattern": "Fever Dream", "quality": "Classified", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_awp_cu_awp_psychopath_light_png.png"},
            {"weapon": "CZ75-Auto", "pattern": "Xiangliu", "quality": "Classified", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_cz75a_gs_cz_snakes_purple_light_png.png"},
            {"weapon": "UMP-45", "pattern": "Scaffold", "quality": "Restricted", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_ump45_gs_ump_abyss_light_png.png"},
            {"weapon": "XM1014", "pattern": "Seasons", "quality": "Restricted", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_xm1014_aq_xm_leaf_fade_light_png.png"},
            {"weapon": "Galil AR", "pattern": "Crimson Tsunami", "quality": "Restricted", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_galilar_sp_galil_wave_light_png.png"},
            {"weapon": "M249", "pattern": "Emerald Poison Dart", "quality": "Restricted", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_m249_sp_m249_frog_original_light_png.png"},
            {"weapon": "MAC-10", "pattern": "Last Dive", "quality": "Mil-Spec", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_mac10_aa_mac10_the_last_dive_light_png.png"},
            {"weapon": "P250", "pattern": "Ripple", "quality": "Mil-Spec", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_p250_am_p250_sputnik_light_png.png"},
            {"weapon": "P2000", "pattern": "Imperial", "quality": "Mil-Spec", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_hkp2000_am_p2000_imperial_red_light_png.png"},
            {"weapon": "Five-SeveN", "pattern": "Capillary", "quality": "Mil-Spec", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_fiveseven_cu_fiveseven_vein_light_png.png"},
            {"weapon": "Desert Eagle", "pattern": "Oxide Blaze", "quality": "Mil-Spec", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_deagle_cu_desert_eagle_corroden_light_png.png"},
            {"weapon": "Sawed-Off", "pattern": "Zander", "quality": "Mil-Spec", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_sawedoff_aq_sawedoff_zander2_light_png.png"},
            {"weapon": "SCAR-20", "pattern": "Blueprint", "quality": "Mil-Spec", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_scar20_cu_blueprint_scar_light_png.png"},
            {"weapon": "PP-Bizon", "pattern": "Jungle Slipstream", "quality": "Mil-Spec", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_bizon_hy_bizon_torn_green_light_png.png"}
        ],
        "knives": ["Bayonet", "Flip Knife", "Gut Knife", "Karambit", "M9 Bayonet"]
    },
    {
        "title": "Operation Hydra Case",
        "skins": [
            {"weapon": "Five-SeveN", "pattern": "Hyper Beast", "quality": "Covert", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_fiveseven_cu_fiveseven_hyperbeast_light_png.png"},
            {"weapon": "AWP", "pattern": "Oni Taiji", "quality": "Covert", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_awp_cu_awp_hannya_light_png.png"},
            {"weapon": "M4A4", "pattern": "Hellfire", "quality": "Classified", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_m4a1_cu_m4a4_hellfire_light_png.png"},
            {"weapon": "AK-47", "pattern": "Orbit Mk01", "quality": "Classified", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_ak47_gs_ak_colony01_red_light_png.png"},
            {"weapon": "P2000", "pattern": "Woodsman", "quality": "Classified", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_hkp2000_cu_p2000_hunter_light_png.png"},
            {"weapon": "Dual Berettas", "pattern": "Cobra Strike", "quality": "Restricted", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_elite_gs_dualberettas_cobra_light_png.png"},
            {"weapon": "Galil AR", "pattern": "Sugar Rush", "quality": "Restricted", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_galilar_cu_galil_candychaos_light_png.png"},
            {"weapon": "SSG 08", "pattern": "Death's Head", "quality": "Restricted", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_ssg08_cu_ssg08_deathshead_light_png.png"},
            {"weapon": "P90", "pattern": "Death Grip", "quality": "Restricted", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_p90_hy_p90_barebones_blue_light_png.png"},
            {"weapon": "FAMAS", "pattern": "Macabre", "quality": "Mil-Spec", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_famas_sp_famas_macabre_light_png.png"},
            {"weapon": "UMP-45", "pattern": "Metal Flowers", "quality": "Mil-Spec", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_ump45_aq_ump45_flameflower_light_png.png"},
            {"weapon": "Tec-9", "pattern": "Cut Out", "quality": "Mil-Spec", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_tec9_aq_tec9_chalk_pattern_light_png.png"},
            {"weapon": "MAG-7", "pattern": "Hard Water", "quality": "Mil-Spec", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_mag7_am_mag7_caustic_light_png.png"},
            {"weapon": "Glock-18", "pattern": "Off World", "quality": "Mil-Spec", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_glock_cu_glock_indigo_light_png.png"},
            {"weapon": "USP-S", "pattern": "Blueprint", "quality": "Mil-Spec", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_usp_silencer_cu_usps_blueprint_light_png.png"}
        ],
        "gloves": ["Bloodhound Gloves", "Driver Gloves", "Hand Wraps", "Moto Gloves", "Specialist Gloves", "Sport Gloves", "Hydra Gloves"]
    },
    {
        "title": "Spectrum 2 Case",
        "skins": [
            {"weapon": "M4A1-S", "pattern": "Leaded Glass", "quality": "Covert", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_m4a1_silencer_gs_m4a1_shatter_light_png.png"},
            {"weapon": "AK-47", "pattern": "The Empress", "quality": "Covert", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_ak47_gs_ak47_empress_light_png.png"},
            {"weapon": "P250", "pattern": "See Ya Later", "quality": "Classified", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_p250_cu_p250_cybercroc_light_png.png"},
            {"weapon": "R8 Revolver", "pattern": "Llama Cannon", "quality": "Classified", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_revolver_gs_r8_llamacannon_light_png.png"},
            {"weapon": "PP-Bizon", "pattern": "High Roller", "quality": "Classified", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_bizon_cu_bizon_all_in_light_png.png"},
            {"weapon": "CZ75-Auto", "pattern": "Tacticat", "quality": "Restricted", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_cz75a_gs_cz75_tacticat_light_png.png"},
            {"weapon": "UMP-45", "pattern": "Exposure", "quality": "Restricted", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_ump45_cu_ump45_x-ray_machine_light_png.png"},
            {"weapon": "XM1014", "pattern": "Ziggy", "quality": "Restricted", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_xm1014_aq_xm1014_ziggy_anarchy_light_png.png"},
            {"weapon": "SG 553", "pattern": "Phantom", "quality": "Restricted", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_sg556_gs_sg553_phantom_light_png.png"},
            {"weapon": "G3SG1", "pattern": "Hunter", "quality": "Mil-Spec", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_g3sg1_gs_g3sg1_savage_light_png.png"},
            {"weapon": "M249", "pattern": "Deep Relief", "quality": "Mil-Spec", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_m249_cu_m249_deep_relief_light_png.png"},
            {"weapon": "MP9", "pattern": "Capillary", "quality": "Mil-Spec", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_mp9_cu_mp9_vein_light_png.png"},
            {"weapon": "SCAR-20", "pattern": "Jungle Slipstream", "quality": "Mil-Spec", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_scar20_hy_scar20_jungle_slipstream_light_png.png"},
            {"weapon": "AUG", "pattern": "Syd Mead", "quality": "Mil-Spec", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_aug_gs_aug_syd_mead_light_png.png"},
            {"weapon": "Glock-18", "pattern": "Off World", "quality": "Mil-Spec", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_glock_cu_glock_indigo_light_png.png"},
            {"weapon": "Tec-9", "pattern": "Cracked Opal", "quality": "Mil-Spec", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_tec9_cu_tec9_cracked_opal_light_png.png"},
            {"weapon": "Sawed-Off", "pattern": "Morris", "quality": "Mil-Spec", "image": "https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/default_generated/weapon_sawedoff_aq_sawed-off_flower_light_png.png"}
        ],
        "knives": ["Bayonet", "Flip Knife", "Gut Knife", "Karambit", "M9 Bayonet"]
    }
]

# Create and insert our cases
case_ids = {}
for case_data in cases_with_skins:
    # Get case title and image
    case_title = case_data["title"]
    case_image = get_case_image(case_title)
    
    # Get case release date
    release_date = case_info.get(case_title, "2013-01-01")
    
    # Calculate a default price based on release date (older cases are more expensive)
    years_old = 2025 - int(release_date.split("-")[0])
    default_price = 100 + (5 * years_old)
    
    # Create the case document
    case = {
        "title": case_title,
        "image": case_image,
        "price": default_price,
        "year": int(release_date.split("-")[0]),
        "release_date": release_date,
        "num_skins": len(case_data["skins"]) + (
            len(case_data.get("knives", [])) * 13 if "knives" in case_data else 0
        ) + (len(case_data.get("gloves", [])) * len(glove_images.get(case_data.get("gloves", [""])[0], {})) if "gloves" in case_data else 0)
    }
    
    # Insert the case and store its ID
    case_id = db.cases.insert_one(case).inserted_id
    case_ids[case_title] = case_id
    
    # Insert all the regular skins from this case
    for skin_data in case_data["skins"]:
        # Get weapon and pattern names
        weapon_name = skin_data["weapon"]
        pattern_name = skin_data["pattern"]
        image_url = skin_data["image"]
        
        # Get the weapon ID
        weapon_id = weapon_ids.get(weapon_name)
        if not weapon_id:
            print(f"Warning: Could not find weapon ID for {weapon_name}")
            continue
        
        # Get the quality info
        quality = next((q for q in qualities if q["title"] == skin_data["quality"]), qualities[2])  # Default to Mil-Spec
        quality_id = quality_ids[quality["title"]]
        
        # Calculate price based on quality (rarer = more expensive)
        quality_idx = next((i for i, q in enumerate(qualities) if q["title"] == quality["title"]), 2)
        base_price = 2 ** quality_idx
        price = round(base_price * (1 + 0.1 * years_old) * (0.8 + 0.4 * random.random()), 2)
        
        # Float range based on quality
        if quality_idx <= 2:  # Consumer, Industrial, Mil-Spec
            min_float = round(random.uniform(0.06, 0.15), 2)
            max_float = round(random.uniform(0.7, 1.0), 2)
        else:  # Restricted, Classified, Covert
            min_float = round(random.uniform(0.0, 0.1), 2)
            max_float = round(random.uniform(0.4, 0.8), 2)
        
        # Insert both regular and StatTrak versions
        for stattrak in [False, True]:
            stattrak_price = price
            if stattrak:
                stattrak_price *= 2.5  # Premium for StatTrak
            
            db.skins.insert_one({
                "pattern": {"title": pattern_name},
                "weapon": {"_id": weapon_id, "title": weapon_name, "type": next((w["type"] for w in weapons if w["title"] == weapon_name), "unknown")},
                "case_id": case_id,
                "quality": {"_id": quality_id, "title": quality["title"], "color": quality["color"], "order": quality["order"]},
                "stattrak": stattrak,
                "souvenir": False,
                "price": stattrak_price,
                "image": image_url,
                "min_float": min_float,
                "max_float": max_float,
                "created_at": datetime.now()
            })

    # Insert the knife skins if this case has knives
    if "knives" in case_data:
        # List of standard knife finishes
        standard_finishes = [
            "Vanilla", "Blue Steel", "Boreal Forest", "Case Hardened",
            "Crimson Web", "Fade", "Forest DDPAT", "Night", "Safari Mesh",
            "Scorched", "Slaughter", "Stained", "Urban Masked"
        ]
        
        # For regular knife cases, insert all knife skins
        for knife in case_data["knives"]:
            weapon_id = weapon_ids.get(knife)
            if not weapon_id:
                print(f"Warning: Could not find weapon ID for {knife}")
                continue
            
            for finish in standard_finishes:
                knife_price = round(random.uniform(50, 500) * (1 + 0.1 * years_old), 2)
                
                # Get knife image URL based on knife type and finish
                knife_image = knife_images.get(knife, {}).get(finish, None)
                
                if not knife_image:
                    # Fallback to generic knife image
                    knife_lower = knife.lower().replace(' ', '_').replace('-', '')
                    knife_image = f"https://raw.githubusercontent.com/ByMykel/counter-strike-image-tracker/main/static/panorama/images/econ/weapons/base_weapons/weapon_{knife_lower}_png.png"
                
                # Float range for knives
                min_float = round(random.uniform(0.0, 0.08), 2)
                max_float = round(random.uniform(0.4, 0.8), 2)
                
                # Insert both regular and StatTrak versions
                for stattrak in [False, True]:
                    stattrak_price = knife_price
                    if stattrak:
                        stattrak_price *= 2.5  # Premium for StatTrak
                    
                    db.skins.insert_one({
                        "pattern": {"title": finish},
                        "weapon": {"_id": weapon_id, "title": knife, "type": "knife"},
                        "case_id": case_id,
                        "quality": {"_id": quality_ids["Exceedingly Rare"], "title": "Exceedingly Rare", "color": "#ffae39", "order": 7},
                        "stattrak": stattrak,
                        "souvenir": False,
                        "price": stattrak_price,
                        "image": knife_image,
                        "min_float": min_float,
                        "max_float": max_float,
                        "created_at": datetime.now()
                    })

    # Insert the glove skins if this case has gloves
    if "gloves" in case_data:
        for glove_type in case_data["gloves"]:
            weapon_id = weapon_ids.get(glove_type)
            if not weapon_id:
                print(f"Warning: Could not find weapon ID for {glove_type}")
                continue
            
            # Get available finishes for this glove type
            finishes = glove_images.get(glove_type, {})
            
            for finish_name, finish_image in finishes.items():
                glove_price = round(random.uniform(100, 800) * (1 + 0.1 * years_old), 2)
                
                # Float range for gloves
                min_float = round(random.uniform(0.06, 0.15), 2)
                max_float = round(random.uniform(0.4, 0.9), 2)
                
                # Gloves don't have StatTrak variants, so insert only non-StatTrak
                db.skins.insert_one({
                    "pattern": {"title": finish_name},
                    "weapon": {"_id": weapon_id, "title": glove_type, "type": "gloves"},
                    "case_id": case_id,
                    "quality": {"_id": quality_ids["Exceedingly Rare"], "title": "Exceedingly Rare", "color": "#ffae39", "order": 7},
                    "stattrak": False,
                    "souvenir": False,
                    "price": glove_price,
                    "image": finish_image,
                    "min_float": min_float,
                    "max_float": max_float,
                    "created_at": datetime.now()
                })

print("\nБаза данных успешно заполнена!")
print(f"Создано {len(cases_with_skins)} кейсов")
print(f"Создано {db.skins.count_documents({})} скинов")
print("Все изображения взяты напрямую из URL")
print("Current Date and Time (UTC - YYYY-MM-DD HH:MM:SS formatted): 2025-05-17 07:53:40")
print("Current User's Login: copilotpublic_andrtro")
input("\nНажмите Enter для выхода...")