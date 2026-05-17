import requests
import json
import os

def fetch_status():
    # Using BattleMetrics API to get Arma Reforger servers
    url = "https://api.battlemetrics.com/servers?filter[game]=reforger&page[size]=50"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        servers = []
        for item in data.get('data', []):
            attrs = item.get('attributes', {})
            servers.append({
                "name": attrs.get('name'),
                "players": attrs.get('players'),
                "maxPlayers": attrs.get('maxPlayers'),
                "status": attrs.get('status'),
                "map": attrs.get('details', {}).get('map', 'Unknown')
            })
        
        # Sort by player count descending
        servers.sort(key=lambda x: x['players'], reverse=True)
        
        with open('status.json', 'w') as f:
            json.dump(servers, f, indent=4)
        print(f"Successfully updated status.json with {len(servers)} servers.")
            
    except Exception as e:
        print(f"Error fetching status: {e}")
        # Ensure the file exists even if the fetch fails
        if not os.path.exists('status.json'):
            with open('status.json', 'w') as f:
                json.dump([], f)

if __name__ == "__main__":
    fetch_status()
