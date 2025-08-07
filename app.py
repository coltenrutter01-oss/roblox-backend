from flask import Flask, jsonify
import requests
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return 'Roblox Backend is running!'

@app.route('/games/<int:user_id>')
def get_games(user_id):
    try:
        # Get the list of games the user has played
        url = f"https://games.roblox.com/v2/users/{user_id}/games?accessFilter=All&limit=100&sortOrder=Asc"
        r = requests.get(url)
        r.raise_for_status()
        data = r.json()

        games = []

        for index, game in enumerate(data.get("data", []), start=1):
            game_info = {
                "number": index,
                "id": game.get("id"),
                "name": game.get("name"),
                "placeId": game.get("rootPlace", {}).get("id"),
                "releaseDate": game.get("created"),
                "visits": game.get("visits"),
                "favorites": game.get("favoritedCount"),
                "playing": game.get("playing"),
                "thumbnail": f"https://www.roblox.com/asset-thumbnail/image?assetId={game.get('id')}&width=420&height=420&format=png"
            }
            games.append(game_info)

        return jsonify({"user_id": user_id, "games": games})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=10000)
