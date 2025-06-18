from flask import Flask, jsonify, request, session, redirect, url_for, send_from_directory
from flask_cors import CORS
from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime
import random
import math
import os
import re
import requests
from dotenv import load_dotenv
import json

# Load environment variables
load_dotenv()

app = Flask(__name__, static_folder='../assets', static_url_path='/assets')
app.secret_key = os.getenv('SECRET_KEY', 'your_secret_key')
CORS(app)

# Custom JSON encoder to handle ObjectId and datetime
class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)
        if isinstance(obj, datetime):
            return obj.isoformat()
        return json.JSONEncoder.default(self, obj)

app.json_encoder = CustomJSONEncoder

# MongoDB connection
mongo_uri = os.getenv('MONGO_URI', 'mongodb://')
mongo_db = os.getenv('MONGO_DB', 'reforge')

client = MongoClient(mongo_uri)
db = client[mongo_db]

# Steam API settings
STEAM_API_KEY = os.getenv('STEAM_API_KEY', '')
STEAM_OPENID_URL = 'https://steamcommunity.com/openid/login'

# Helper function to convert MongoDB document to JSON serializable
def serialize_doc(doc):
    if isinstance(doc, dict):
        result = {}
        for key, value in doc.items():
            if key == '_id' and isinstance(value, ObjectId):
                result[key] = str(value)
            elif isinstance(value, ObjectId):
                result[key] = str(value)
            elif isinstance(value, datetime):
                result[key] = value.isoformat()
            elif isinstance(value, dict):
                result[key] = serialize_doc(value)
            elif isinstance(value, list):
                result[key] = [serialize_doc(item) for item in value]
            else:
                result[key] = value
        return result
    elif isinstance(doc, list):
        return [serialize_doc(item) for item in doc]
    else:
        return doc

# Serve static files
@app.route('/')
def index():
    return send_from_directory('../', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('../', path)

# Прямая реализация Steam авторизации без библиотеки openid
@app.route('/api/login')
def login():
    params = {
        'openid.ns': 'http://specs.openid.net/auth/2.0',
        'openid.mode': 'checkid_setup',
        'openid.return_to': request.url_root + 'api/auth',
        'openid.realm': request.url_root,
        'openid.identity': 'http://specs.openid.net/auth/2.0/identifier_select',
        'openid.claimed_id': 'http://specs.openid.net/auth/2.0/identifier_select'
    }
    auth_url = STEAM_OPENID_URL + '?' + '&'.join([f'{key}={value}' for key, value in params.items()])
    return redirect(auth_url)

@app.route('/api/auth')
def auth():
    if 'openid.signed' not in request.args:
        return 'Authentication failed.', 400
    
    # Получаем Steam ID из ответа
    match = re.search(r'steamcommunity.com/openid/id/(.*?)$', request.args.get('openid.claimed_id', ''))
    if not match:
        return 'Could not get Steam ID.', 400
    
    steam_id = match.group(1)
    
    # Получение информации о пользователе
    user_info = get_steam_user_info(steam_id)
    
    if user_info:
        # Сохраняем информацию о пользователе в сессии
        session['steam_id'] = steam_id
        session['steam_username'] = user_info['personaname']
        session['steam_avatar'] = user_info['avatar']
        
        # Проверяем, существует ли пользователь в БД
        user = db.users.find_one({"steam_id": steam_id})
        
        if user:
            # Обновляем существующего пользователя
            db.users.update_one(
                {"steam_id": steam_id},
                {"$set": {
                    "username": user_info['personaname'],
                    "avatar": user_info['avatar'],
                    "last_login": datetime.now()
                }}
            )
        else:
            # Создаем нового пользователя
            db.users.insert_one({
                "steam_id": steam_id,
                "username": user_info['personaname'],
                "avatar": user_info['avatar'],
                "balance": 100.0,  # Начальный баланс
                "inventory": [],
                "created_at": datetime.now(),
                "last_login": datetime.now()
            })
        
        return redirect('/pages/profile.html')
    
    return 'Authentication failed. <a href="/api/login">Try again</a>', 400

def get_steam_user_info(steam_id):
    # Получение информации о пользователе через Steam API
    if not STEAM_API_KEY:
        # Если нет API ключа, возвращаем заглушку
        return {
            'personaname': f'User_{steam_id[-5:]}',
            'avatar': 'https://steamcdn-a.akamaihd.net/steamcommunity/public/images/avatars/fe/fef49e7fa7e1997310d705b2a6158ff8dc1cdfeb.jpg'
        }
        
    response = requests.get(
        f'https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/',
        params={
            'key': STEAM_API_KEY,
            'steamids': steam_id
        }
    )
    
    if response.status_code == 200:
        data = response.json()
        if data['response']['players']:
            return data['response']['players'][0]
    
    return None

@app.route('/api/logout')
def logout():
    session.pop('steam_id', None)
    session.pop('steam_username', None)
    session.pop('steam_avatar', None)
    session.pop('scanned_item', None)  # Очищаем информацию о просканированном предмете
    return redirect('/pages/profile.html')

# API routes
@app.route('/api/cases')
def get_cases():
    cases = list(db.cases.find())
    return jsonify([serialize_doc(case) for case in cases])

@app.route('/api/case/<case_id>')
def get_case(case_id):
    try:
        case = db.cases.find_one({"_id": ObjectId(case_id)})
        if not case:
            return jsonify({"error": "Case not found"}), 404
            
        skins = list(db.skins.find({"case_id": ObjectId(case_id)}))
        
        return jsonify({
            "case": serialize_doc(case),
            "skins": [serialize_doc(skin) for skin in skins]
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/inventory')
def get_inventory():
    if 'steam_id' not in session:
        return jsonify({"error": "Not logged in"}), 401
        
    try:
        user = db.users.find_one({"steam_id": session['steam_id']})
        if not user:
            return jsonify({"error": "User not found"}), 404
            
        inventory = []
        
        for item in user.get('inventory', []):
            skin = db.skins.find_one({"_id": ObjectId(item['skin_id'])})
            if skin:
                inventory_item = {
                    "_id": str(item['_id']),
                    "skin": serialize_doc(skin),
                    "float": item['float'],
                    "obtained_at": item['obtained_at']
                }
                
                # Add StatTrak™ if applicable
                if item.get('is_stattrak', False):
                    inventory_item["is_stattrak"] = True
                
                # Add special pattern if applicable
                if item.get('special_pattern'):
                    inventory_item["special_pattern"] = item['special_pattern']
                    
                inventory.append(inventory_item)
                
        return jsonify(inventory)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/scan-case/<case_id>', methods=['POST'])
def scan_case(case_id):
    """Endpoint for X-Ray scanner - determines the item without claiming it but charges a fee"""
    if 'steam_id' not in session:
        return jsonify({"error": "Not logged in"}), 401
        
    try:
        # Get user
        user = db.users.find_one({"steam_id": session['steam_id']})
        if not user:
            return jsonify({"error": "User not found"}), 404
            
        # Get case
        case = db.cases.find_one({"_id": ObjectId(case_id)})
        if not case:
            return jsonify({"error": "Case not found"}), 404
        
        # Calculate scanning fee (5% of case price, minimum 10 RC)
        scan_fee = max(case['price'] * 0.05, 10)
        scan_fee = round(scan_fee, 2)  # Round to 2 decimal places
        
        # Check if user has enough balance for scanning
        if user['balance'] < scan_fee:
            return jsonify({"error": f"Недостаточно средств для сканирования. Необходимо: {scan_fee} RC"}), 400
            
        # Deduct scan fee from user balance
        db.users.update_one(
            {"_id": user['_id']},
            {"$inc": {"balance": -scan_fee}}
        )
            
        # Get skins for this case
        skins = list(db.skins.find({"case_id": ObjectId(case_id)}))
        
        if not skins:
            return jsonify({"error": "No skins found for this case"}), 404
            
        # Adjusted rarity weights - reduced chances for Covert items
        rarities = {
            "Consumer Grade": {"weight": 2800, "float_curve": "normal"},     # Increased
            "Industrial Grade": {"weight": 2200, "float_curve": "normal"},   # Increased
            "Mil-Spec": {"weight": 1600, "float_curve": "normal"},           # Increased
            "Restricted": {"weight": 650, "float_curve": "normal"},
            "Classified": {"weight": 120, "float_curve": "normal"},
            "Covert": {"weight": 30, "float_curve": "slightly_right_skewed"}, # Reduced from 65 to 30
            "Exceedingly Rare": {"weight": 15, "float_curve": "left_skewed"} # Reduced from 25 to 15
        }
        
        # Group skins by rarity and type
        skins_by_category = {}
        
        for skin in skins:
            rarity = skin['quality']['title']
            weapon_type = skin['weapon']['type']
            
            # Create special category for knives and gloves
            if weapon_type in ["knife", "gloves"]:
                category = f"Exceedingly Rare_{weapon_type}"
            else:
                category = rarity
                
            if category not in skins_by_category:
                skins_by_category[category] = []
            
            skins_by_category[category].append(skin)
        
        # First, decide if we're dropping a special item (knife/glove)
        special_item_chance = 0.0015  # Reduced from 0.25% to 0.15% chance
        is_special_item = random.random() < special_item_chance
        
        if is_special_item and "Exceedingly Rare_knife" in skins_by_category:
            # Knife drop!
            won_skin = random.choice(skins_by_category["Exceedingly Rare_knife"])
            float_curve = "left_skewed"
        else:
            # Calculate total weight for non-special rarities
            available_rarities = [r for r in rarities.keys() if r in skins_by_category and r != "Exceedingly Rare"]
            
            if not available_rarities:
                # Fallback if no non-special rarities found
                available_categories = list(skins_by_category.keys())
                if not available_categories:
                    return jsonify({"error": "No appropriate skins found for this case"}), 404
                    
                # Pick a random category and skin
                chosen_category = random.choice(available_categories)
                won_skin = random.choice(skins_by_category[chosen_category])
                float_curve = "normal"
            else:
                # Calculate total weight
                total_weight = sum(rarities[r]["weight"] for r in available_rarities)
                
                # Roll for rarity
                roll = random.uniform(0, total_weight)
                current_weight = 0
                chosen_rarity = available_rarities[-1]  # Default to highest available rarity
                
                for rarity in available_rarities:
                    current_weight += rarities[rarity]["weight"]
                    if roll <= current_weight:
                        chosen_rarity = rarity
                        break
                
                # Select a random skin from chosen rarity
                won_skin = random.choice(skins_by_category[chosen_rarity])
                float_curve = rarities[chosen_rarity]["float_curve"]
        
        # Generate float value based on rarity
        min_float = won_skin['min_float']
        max_float = won_skin['max_float']
        float_range = max_float - min_float
        
        # Apply different distribution based on rarity
        if float_curve == "normal":
            # Normal distribution centered in the middle of the range
            mu = min_float + float_range / 2
            sigma = float_range / 6
            item_float = random.normalvariate(mu, sigma)
            # Ensure the float stays within bounds
            item_float = max(min_float, min(max_float, item_float))
        elif float_curve == "slightly_right_skewed":
            # Beta distribution for slightly right-skewed (more lower floats)
            alpha, beta = 2, 3
            raw_float = random.betavariate(alpha, beta)
            item_float = min_float + raw_float * float_range
        elif float_curve == "left_skewed":
            # Beta distribution for left-skewed (more higher floats)
            alpha, beta = 3, 2
            raw_float = random.betavariate(alpha, beta)
            item_float = min_float + raw_float * float_range
        else:
            # Uniform distribution as fallback
            item_float = random.uniform(min_float, max_float)
        
        # Round to 8 decimal places (CS:GO standard)
        item_float = round(item_float, 8)
        
        # Determine if the item is StatTrak™ - reduced chance
        stattrak_chance = 0.04  # Reduced from 10% to 4% chance
        is_stattrak = won_skin.get('stattrak', False) or (random.random() < stattrak_chance)
        
        # Store the scanned item in session for later retrieval
        session['scanned_item'] = {
            'skin_id': str(won_skin['_id']),
            'case_id': str(case_id),
            'float': item_float,
            'is_stattrak': is_stattrak
        }
        
        # Get updated user balance
        updated_user = db.users.find_one({"_id": user['_id']})
        
        response_data = {
            "wonItem": serialize_doc(won_skin),
            "float": item_float,
            "scan_fee": scan_fee,
            "new_balance": updated_user['balance']
        }
        
        # Add StatTrak™ status if applicable
        if is_stattrak:
            response_data["is_stattrak"] = True
        
        return jsonify(response_data)
        
    except Exception as e:
        print(f"Error in scan_case: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/claim-scanned-case/<case_id>', methods=['POST'])
def claim_scanned_case(case_id):
    """Endpoint to claim an X-Ray scanned item"""
    if 'steam_id' not in session:
        return jsonify({"error": "Not logged in"}), 401
        
    if 'scanned_item' not in session:
        return jsonify({"error": "No scanned item found"}), 400
        
    scanned_item = session['scanned_item']
    
    # Verify this is the correct case
    if scanned_item['case_id'] != case_id:
        return jsonify({"error": "Case mismatch"}), 400
        
    try:
        # Get user
        user = db.users.find_one({"steam_id": session['steam_id']})
        if not user:
            return jsonify({"error": "User not found"}), 404
            
        # Get case
        case = db.cases.find_one({"_id": ObjectId(case_id)})
        if not case:
            return jsonify({"error": "Case not found"}), 404
            
        # Check if user has enough balance
        if user['balance'] < case['price']:
            return jsonify({"error": "Insufficient balance"}), 400
            
        # Get the skin
        won_skin = db.skins.find_one({"_id": ObjectId(scanned_item['skin_id'])})
        if not won_skin:
            return jsonify({"error": "Item not found"}), 404
            
        # Use the saved values
        item_float = scanned_item['float']
        is_stattrak = scanned_item.get('is_stattrak', False)
        
        # Deduct case price from user balance
        db.users.update_one(
            {"_id": user['_id']},
            {"$inc": {"balance": -case['price']}}
        )
        
        # Add item to user's inventory
        inventory_item_id = ObjectId()
        
        inventory_item = {
            "_id": inventory_item_id,
            "skin_id": won_skin['_id'],
            "float": item_float,
            "obtained_at": datetime.now()
        }
        
        # Add StatTrak™ if applicable
        if is_stattrak:
            inventory_item["is_stattrak"] = True
        
        db.users.update_one(
            {"_id": user['_id']},
            {"$push": {"inventory": inventory_item}}
        )
        
        # Clear the scanned item from session
        session.pop('scanned_item', None)
        
        # Prepare response
        response_data = {
            "success": True,
            "wonItem": serialize_doc(won_skin),
            "float": item_float
        }
        
        if is_stattrak:
            response_data["is_stattrak"] = True
        
        return jsonify(response_data)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/discard-case', methods=['POST'])
def discard_case():
    """Clean up session data after discarding a case"""
    if 'steam_id' not in session:
        return jsonify({"error": "Not logged in"}), 401
    
    # Clear the scanned item
    session.pop('scanned_item', None)
    
    return jsonify({"success": True})

@app.route('/api/sell-item/<item_id>', methods=['POST'])
def sell_item(item_id):
    if 'steam_id' not in session:
        return jsonify({"error": "Not logged in"}), 401
        
    try:
        # Get user
        user = db.users.find_one({"steam_id": session['steam_id']})
        if not user:
            return jsonify({"error": "User not found"}), 404
            
        # Find the item in user's inventory
        inventory_item = None
        for item in user.get('inventory', []):
            if str(item['_id']) == item_id:
                inventory_item = item
                break
                
        if not inventory_item:
            return jsonify({"error": "Item not found in inventory"}), 404
            
        # Get the skin details
        skin = db.skins.find_one({"_id": inventory_item['skin_id']})
        if not skin:
            return jsonify({"error": "Skin not found"}), 404
            
        # Base sell price (90% of market value)
        base_price = skin['price'] * 0.9
        
        # Price modifiers based on special attributes
        price_multiplier = 1.0
        
        # Float value adjustment
        if skin.get('min_float') is not None and skin.get('max_float') is not None:
            float_range = skin['max_float'] - skin['min_float']
            if float_range > 0:
                # Calculate how good the float is (0 = worst, 1 = best)
                float_quality = 1 - ((inventory_item['float'] - skin['min_float']) / float_range)
                
                # Apply float quality multiplier (1.0 to 1.3)
                float_multiplier = 1 + (float_quality * 0.3)
                price_multiplier *= float_multiplier
        
        # StatTrak™ adjustment (2x for StatTrak™)
        if inventory_item.get('is_stattrak', False):
            price_multiplier *= 2.0
            
        # Special pattern adjustment
        if inventory_item.get('special_pattern'):
            # Special patterns can be worth a lot more
            pattern_multipliers = {
                "Fade": 1.5,
                "Marble Fade": 1.8,
                "Tiger Tooth": 1.7,
                "Doppler Ruby": 4.0,
                "Doppler Sapphire": 5.0,
                "Doppler Black Pearl": 3.5,
                "Blue Gem": 3.0,
                "Fire and Ice": 2.5
            }
            
            pattern = inventory_item['special_pattern']
            if pattern in pattern_multipliers:
                price_multiplier *= pattern_multipliers[pattern]
            else:
                price_multiplier *= 1.5  # Default multiplier for unspecified patterns
        
        # Calculate final sell price
        sell_price = base_price * price_multiplier
        sell_price = round(sell_price, 2)  # Round to 2 decimal places
        
        # Remove item from inventory and add balance
        db.users.update_one(
            {"_id": user['_id']},
            {
                "$pull": {"inventory": {"_id": ObjectId(item_id)}},
                "$inc": {"balance": sell_price}
            }
        )
        
        # Get updated user balance
        updated_user = db.users.find_one({"_id": user['_id']})
        
        return jsonify({
            "success": True,
            "sold_for": sell_price,
            "new_balance": updated_user['balance']
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/user')
def get_user():
    if 'steam_id' not in session:
        return jsonify({"error": "Not logged in"}), 401
        
    try:
        user = db.users.find_one({"steam_id": session['steam_id']})
        if not user:
            return jsonify({"error": "User not found"}), 404
            
        # Don't return inventory here to keep response small
        user_data = serialize_doc({
            "steam_id": user['steam_id'],
            "username": user['username'],
            "avatar": user['avatar'],
            "balance": user['balance'],
            "inventory_count": len(user.get('inventory', [])),
            "created_at": user['created_at'],
            "last_login": user['last_login']
        })
        
        return jsonify(user_data)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/add-funds', methods=['POST'])
def add_funds():
    if 'steam_id' not in session:
        return jsonify({"error": "Not logged in"}), 401
        
    try:
        data = request.json
        amount = float(data.get('amount', 0))
        
        if amount <= 0:
            return jsonify({"error": "Invalid amount"}), 400
            
        # In a real app, you would process payment here
        
        # Update user balance
        db.users.update_one(
            {"steam_id": session['steam_id']},
            {"$inc": {"balance": amount}}
        )
        
        return jsonify({"success": True})
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Added new endpoint for selling multiple items at once
@app.route('/api/sell-items', methods=['POST'])
def sell_items():
    if 'steam_id' not in session:
        return jsonify({"error": "Not logged in"}), 401
        
    try:
        data = request.json
        item_ids = data.get('item_ids', [])
        
        if not item_ids or not isinstance(item_ids, list):
            return jsonify({"error": "Invalid item IDs"}), 400
            
        # Get user
        user = db.users.find_one({"steam_id": session['steam_id']})
        if not user:
            return jsonify({"error": "User not found"}), 404
            
        total_price = 0
        sold_items = []
        
        # Process each item
        for item_id in item_ids:
            # Find the item in user's inventory
            inventory_item = None
            for item in user.get('inventory', []):
                if str(item['_id']) == item_id:
                    inventory_item = item
                    break
                    
            if not inventory_item:
                continue  # Skip items not found
                
            # Get the skin details
            skin = db.skins.find_one({"_id": inventory_item['skin_id']})
            if not skin:
                continue  # Skip if skin not found
                
            # Base sell price (90% of market value)
            base_price = skin['price'] * 0.9
            
            # Price modifiers based on special attributes
            price_multiplier = 1.0
            
            # Float value adjustment
            if skin.get('min_float') is not None and skin.get('max_float') is not None:
                float_range = skin['max_float'] - skin['min_float']
                if float_range > 0:
                    # Calculate how good the float is (0 = worst, 1 = best)
                    float_quality = 1 - ((inventory_item['float'] - skin['min_float']) / float_range)
                    
                    # Apply float quality multiplier (1.0 to 1.3)
                    float_multiplier = 1 + (float_quality * 0.3)
                    price_multiplier *= float_multiplier
            
            # StatTrak™ adjustment (2x for StatTrak™)
            if inventory_item.get('is_stattrak', False):
                price_multiplier *= 2.0
                
            # Special pattern adjustment
            if inventory_item.get('special_pattern'):
                # Special patterns can be worth a lot more
                pattern_multipliers = {
                    "Fade": 1.5,
                    "Marble Fade": 1.8,
                    "Tiger Tooth": 1.7,
                    "Doppler Ruby": 4.0,
                    "Doppler Sapphire": 5.0,
                    "Doppler Black Pearl": 3.5,
                    "Blue Gem": 3.0,
                    "Fire and Ice": 2.5
                }
                
                pattern = inventory_item['special_pattern']
                if pattern in pattern_multipliers:
                    price_multiplier *= pattern_multipliers[pattern]
                else:
                    price_multiplier *= 1.5  # Default multiplier for unspecified patterns
            
            # Calculate final sell price
            sell_price = base_price * price_multiplier
            sell_price = round(sell_price, 2)  # Round to 2 decimal places
            
            total_price += sell_price
            sold_items.append({"item_id": item_id, "sold_for": sell_price})
            
            # Remove item from inventory
            db.users.update_one(
                {"_id": user['_id']},
                {"$pull": {"inventory": {"_id": ObjectId(item_id)}}}
            )
        
        # Add total balance
        if total_price > 0:
            db.users.update_one(
                {"_id": user['_id']},
                {"$inc": {"balance": total_price}}
            )
        
        # Get updated user balance
        updated_user = db.users.find_one({"_id": user['_id']})
        
        return jsonify({
            "success": True,
            "sold_items": sold_items,
            "total_sold_for": total_price,
            "new_balance": updated_user['balance']
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Added new endpoint for case statistics
@app.route('/api/case-stats/<case_id>')
def get_case_stats(case_id):
    try:
        # Get case details
        case = db.cases.find_one({"_id": ObjectId(case_id)})
        if not case:
            return jsonify({"error": "Case not found"}), 404
            
        # Get all skins for this case
        skins = list(db.skins.find({"case_id": ObjectId(case_id)}))
        
        if not skins:
            return jsonify({"error": "No skins found for this case"}), 404
        
        # Group skins by rarity
        skins_by_rarity = {}
        for skin in skins:
            rarity = skin['quality']['title']
            if rarity not in skins_by_rarity:
                skins_by_rarity[rarity] = []
            skins_by_rarity[rarity].append(skin)
            
        # Calculate odds and expected value
        rarities = {
            "Consumer Grade": {"weight": 7980, "odds": 0},
            "Industrial Grade": {"weight": 1598, "odds": 0},
            "Mil-Spec": {"weight": 319.6, "odds": 0},
            "Restricted": {"weight": 63.98, "odds": 0},
            "Classified": {"weight": 12.8, "odds": 0},
            "Covert": {"weight": 2.56, "odds": 0},
            "Exceedingly Rare": {"weight": 3.2, "odds": 0}
        }
        
        # Calculate total weight for available rarities
        total_weight = sum(data["weight"] for rarity, data in rarities.items() if rarity in skins_by_rarity)
        
        # Calculate odds and expected values
        expected_value = 0
        rarity_stats = []
        
        for rarity, data in rarities.items():
            if rarity not in skins_by_rarity:
                continue
                
            odds = data["weight"] / total_weight
            rarities[rarity]["odds"] = odds
            
            # Calculate average value for this rarity
            avg_value = sum(skin['price'] for skin in skins_by_rarity[rarity]) / len(skins_by_rarity[rarity])
            
            # Contribute to expected value
            expected_value += odds * avg_value
            
            # Prepare stats for response
            rarity_stats.append({
                "rarity": rarity,
                "odds": round(odds * 100, 4),  # Convert to percentage
                "count": len(skins_by_rarity[rarity]),
                "avg_value": round(avg_value, 2)
            })
        
        # Calculate ROI
        roi = (expected_value / case['price']) - 1
        roi_percentage = round(roi * 100, 2)
        
        return jsonify({
            "case": serialize_doc(case),
            "expected_value": round(expected_value, 2),
            "case_price": case['price'],
            "roi_percentage": roi_percentage,
            "rarity_stats": rarity_stats
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)