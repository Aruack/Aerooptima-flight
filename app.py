"""
Flight Route Optimization System (DAA Mini Project)
Algorithms: Dijkstra (Shortest Route) & Backtracking (Alternative Routes)
"""
import os, math, time, heapq
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# 1. Haversine Great-Circle Distance (in km)
def haversine(lat1, lon1, lat2, lon2):
    R = 6371.0
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dp, dl = math.radians(lat2 - lat1), math.radians(lon2 - lon1)
    a = math.sin(dp / 2)**2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2)**2
    return round(2 * R * math.atan2(math.sqrt(a), math.sqrt(1 - a)), 2)

# 2. Verified Airports Dataset (Real Coordinates)
AIRPORTS = {
    "DEL": {"code": "DEL", "name": "Indira Gandhi Int'l", "city": "New Delhi", "country": "India", "lat": 28.5562, "lon": 77.1000},
    "BOM": {"code": "BOM", "name": "Chhatrapati Shivaji Int'l", "city": "Mumbai", "country": "India", "lat": 19.0896, "lon": 72.8656},
    "BLR": {"code": "BLR", "name": "Kempegowda Int'l", "city": "Bengaluru", "country": "India", "lat": 13.1986, "lon": 77.7066},
    "MAA": {"code": "MAA", "name": "Chennai Int'l", "city": "Chennai", "country": "India", "lat": 12.9941, "lon": 80.1709},
    "CCU": {"code": "CCU", "name": "Netaji Subhash Chandra Bose Int'l", "city": "Kolkata", "country": "India", "lat": 22.6547, "lon": 88.4467},
    "DXB": {"code": "DXB", "name": "Dubai Int'l", "city": "Dubai", "country": "UAE", "lat": 25.2532, "lon": 55.3657},
    "DOH": {"code": "DOH", "name": "Hamad Int'l", "city": "Doha", "country": "Qatar", "lat": 25.2731, "lon": 51.6081},
    "LHR": {"code": "LHR", "name": "London Heathrow", "city": "London", "country": "UK", "lat": 51.4700, "lon": -0.4543},
    "CDG": {"code": "CDG", "name": "Charles de Gaulle", "city": "Paris", "country": "France", "lat": 49.0097, "lon": 2.5479},
    "FRA": {"code": "FRA", "name": "Frankfurt Airport", "city": "Frankfurt", "country": "Germany", "lat": 50.0379, "lon": 8.5622},
    "SIN": {"code": "SIN", "name": "Singapore Changi", "city": "Singapore", "country": "Singapore", "lat": 1.3644, "lon": 103.9915},
    "BKK": {"code": "BKK", "name": "Suvarnabhumi", "city": "Bangkok", "country": "Thailand", "lat": 13.6900, "lon": 100.7501},
    "HND": {"code": "HND", "name": "Tokyo Haneda", "city": "Tokyo", "country": "Japan", "lat": 35.5494, "lon": 139.7798},
    "HKG": {"code": "HKG", "name": "Hong Kong Int'l", "city": "Hong Kong", "country": "Hong Kong", "lat": 22.3080, "lon": 113.9185},
    "JFK": {"code": "JFK", "name": "John F. Kennedy Int'l", "city": "New York", "country": "USA", "lat": 40.6413, "lon": -73.7781},
    "SFO": {"code": "SFO", "name": "San Francisco Int'l", "city": "San Francisco", "country": "USA", "lat": 37.6213, "lon": -122.3790},
    "LAX": {"code": "LAX", "name": "Los Angeles Int'l", "city": "Los Angeles", "country": "USA", "lat": 33.9416, "lon": -118.4085},
    "ORD": {"code": "ORD", "name": "O'Hare Int'l", "city": "Chicago", "country": "USA", "lat": 41.9742, "lon": -87.9073},
    "SYD": {"code": "SYD", "name": "Sydney Kingsford Smith", "city": "Sydney", "country": "Australia", "lat": -33.9399, "lon": 151.1753}
}

# 3. Verified Direct Flight Connections (Non-stop scheduled airline routes)
DIRECT_ROUTES = [
    ("DEL", "BOM", ["Air India", "IndiGo"]), ("DEL", "BLR", ["Air India", "IndiGo"]),
    ("DEL", "MAA", ["Air India", "IndiGo"]), ("DEL", "CCU", ["Air India", "IndiGo"]),
    ("BOM", "BLR", ["Air India", "IndiGo"]), ("BOM", "MAA", ["Air India", "IndiGo"]),
    ("BOM", "CCU", ["Air India", "IndiGo"]), ("BLR", "MAA", ["Air India", "IndiGo"]),
    ("DEL", "DXB", ["Emirates", "Air India"]), ("BOM", "DXB", ["Emirates", "Air India"]),
    ("BLR", "DXB", ["Emirates", "IndiGo"]), ("DEL", "DOH", ["Qatar Airways", "Air India"]),
    ("BOM", "DOH", ["Qatar Airways", "IndiGo"]), ("DEL", "SIN", ["Singapore Airlines", "Air India"]),
    ("BOM", "SIN", ["Singapore Airlines", "Air India"]), ("BLR", "SIN", ["Singapore Airlines"]),
    ("DEL", "BKK", ["Thai Airways", "Air India"]), ("CCU", "BKK", ["Thai Airways", "IndiGo"]),
    ("DEL", "LHR", ["British Airways", "Air India"]), ("BOM", "LHR", ["British Airways", "Air India"]),
    ("BLR", "LHR", ["British Airways"]), ("DEL", "FRA", ["Lufthansa", "Air India"]),
    ("BOM", "FRA", ["Lufthansa"]), ("DEL", "CDG", ["Air France", "Air India"]),
    ("DEL", "JFK", ["Air India", "American"]), ("DEL", "SFO", ["Air India", "United"]),
    ("DEL", "ORD", ["Air India", "United"]), ("DXB", "DOH", ["Qatar Airways", "flydubai"]),
    ("DXB", "LHR", ["Emirates", "British Airways"]), ("DXB", "CDG", ["Emirates", "Air France"]),
    ("DXB", "FRA", ["Emirates", "Lufthansa"]), ("DXB", "JFK", ["Emirates"]),
    ("DXB", "LAX", ["Emirates"]), ("DXB", "SFO", ["Emirates"]),
    ("DXB", "SIN", ["Emirates", "Singapore Airlines"]), ("DXB", "SYD", ["Emirates"]),
    ("DOH", "LHR", ["Qatar Airways", "British Airways"]), ("DOH", "CDG", ["Qatar Airways"]),
    ("DOH", "JFK", ["Qatar Airways"]), ("DOH", "SYD", ["Qatar Airways"]),
    ("LHR", "CDG", ["British Airways", "Air France"]), ("LHR", "FRA", ["British Airways", "Lufthansa"]),
    ("LHR", "JFK", ["British Airways", "Virgin", "Delta"]), ("LHR", "ORD", ["British Airways", "United"]),
    ("LHR", "SFO", ["British Airways", "United"]), ("LHR", "LAX", ["British Airways", "United"]),
    ("CDG", "FRA", ["Air France", "Lufthansa"]), ("CDG", "JFK", ["Air France", "Delta"]),
    ("FRA", "JFK", ["Lufthansa", "Delta"]), ("FRA", "SIN", ["Lufthansa", "Singapore Airlines"]),
    ("JFK", "LAX", ["Delta", "American"]), ("JFK", "SFO", ["Delta", "United"]),
    ("JFK", "ORD", ["American", "United"]), ("ORD", "SFO", ["United"]),
    ("SFO", "LAX", ["United", "Delta"]), ("SIN", "BKK", ["Singapore Airlines", "Thai Airways"]),
    ("SIN", "HKG", ["Singapore Airlines", "Cathay"]), ("SIN", "HND", ["Singapore Airlines", "ANA"]),
    ("SIN", "SYD", ["Singapore Airlines", "Qantas"]), ("HKG", "HND", ["Cathay", "ANA"]),
    ("HKG", "SFO", ["Cathay", "United"]), ("HKG", "LHR", ["Cathay", "British Airways"]),
    ("HND", "SFO", ["ANA", "United"]), ("HND", "LAX", ["ANA", "Delta"]),
    ("HND", "LHR", ["ANA", "British Airways"])
]

# Build Graph
GRAPH = {code: [] for code in AIRPORTS}
EDGES = []
for orig, dest, airlines in DIRECT_ROUTES:
    if orig in AIRPORTS and dest in AIRPORTS:
        d = haversine(AIRPORTS[orig]["lat"], AIRPORTS[orig]["lon"], AIRPORTS[dest]["lat"], AIRPORTS[dest]["lon"])
        EDGES.append({"source": orig, "target": dest, "distance_km": d, "airlines": airlines})
        GRAPH[orig].append({"to": dest, "dist": d, "airlines": airlines})
        GRAPH[dest].append({"to": orig, "dist": d, "airlines": airlines})

# 4. Dijkstra's Algorithm (from scratch using Min-Priority Queue)
def dijkstra(source, destination):
    t0 = time.perf_counter()
    if source not in GRAPH or destination not in GRAPH:
        return {"success": False, "error": "Invalid airport code."}
    
    dist = {code: float("inf") for code in GRAPH}
    prev = {code: None for code in GRAPH}
    dist[source] = 0.0
    
    pq = [(0.0, source)]  # Min-heap priority queue
    visited = set()
    steps_trace = []

    while pq:
        d, curr = heapq.heappop(pq)
        if curr in visited:
            continue
        visited.add(curr)
        steps_trace.append(f"Visited {curr} (dist: {d:.1f} km)")

        if curr == destination:
            break

        for edge in GRAPH[curr]:
            nxt, w = edge["to"], edge["dist"]
            if nxt not in visited and d + w < dist[nxt]:
                dist[nxt] = d + w
                prev[nxt] = curr
                heapq.heappush(pq, (d + w, nxt))
                steps_trace.append(f"Relaxed {curr} -> {nxt} (new dist: {d + w:.1f} km)")

    if dist[destination] == float("inf"):
        return {"success": False, "error": "No flight path found between these airports."}

    # Reconstruct path
    path, curr = [], destination
    while curr:
        path.append(curr)
        curr = prev[curr]
    path.reverse()

    runtime = round((time.perf_counter() - t0) * 1000, 3)
    return {
        "success": True,
        "algorithm": "Dijkstra (Min-Heap Priority Queue)",
        "source": source,
        "destination": destination,
        "path": path,
        "intermediate_airports": path[1:-1],
        "stops_count": len(path) - 2,
        "total_distance_km": round(dist[destination], 2),
        "execution_time_ms": runtime,
        "visited_nodes": len(visited),
        "steps_trace": steps_trace[:30]
    }

# 5. Recursive Backtracking (Alternative Routes with Pruning)
def backtracking_routes(source, destination, max_stops=2, excluded=None, max_dist=None, limit=8):
    t0 = time.perf_counter()
    if source not in GRAPH or destination not in GRAPH:
        return {"success": False, "error": "Invalid airport code."}
    
    excluded_set = set(excluded or [])
    routes, path, visited = [], [source], {source}
    stats = {"calls": 0, "pruned_cycles": 0, "pruned_stops": 0, "pruned_dist": 0}

    def search(curr, curr_dist, stops):
        stats["calls"] += 1
        if curr == destination:
            routes.append({
                "path": list(path),
                "intermediate_airports": list(path[1:-1]),
                "stops_count": len(path) - 2,
                "total_distance_km": round(curr_dist, 2)
            })
            return

        if len(routes) >= limit:
            return

        for edge in GRAPH[curr]:
            nxt, w = edge["to"], edge["dist"]
            if nxt in excluded_set:
                continue
            if nxt in visited:
                stats["pruned_cycles"] += 1
                continue
            next_stops = stops + (1 if nxt != destination else 0)
            if next_stops > max_stops:
                stats["pruned_stops"] += 1
                continue
            if max_dist and (curr_dist + w) > max_dist:
                stats["pruned_dist"] += 1
                continue

            # Forward + Recurse + Backtrack
            visited.add(nxt)
            path.append(nxt)
            search(nxt, curr_dist + w, next_stops)
            path.pop()
            visited.remove(nxt)

    search(source, 0.0, 0)
    routes.sort(key=lambda r: r["total_distance_km"])
    best_dist = routes[0]["total_distance_km"] if routes else 0

    for idx, r in enumerate(routes, 1):
        r["route_id"] = idx
        r["detour_km"] = round(r["total_distance_km"] - best_dist, 2)

    runtime = round((time.perf_counter() - t0) * 1000, 3)
    return {
        "success": bool(routes),
        "algorithm": "Recursive Backtracking with Pruning",
        "source": source,
        "destination": destination,
        "routes": routes,
        "routes_count": len(routes),
        "execution_time_ms": runtime,
        "statistics": stats
    }

# 6. REST API Endpoints
@app.route("/")
def index():
    return send_file(os.path.join(os.path.dirname(__file__), "index.html"))

@app.route("/api/flights/airports")
def get_airports():
    return jsonify({"success": True, "airports": sorted(list(AIRPORTS.values()), key=lambda x: x["city"])})

@app.route("/api/flights/connections")
def get_connections():
    return jsonify({"success": True, "connections": EDGES})

@app.route("/api/flights/shortest-route", methods=["POST"])
def api_shortest():
    data = request.get_json(silent=True) or {}
    return jsonify(dijkstra(data.get("source", "").upper(), data.get("destination", "").upper()))

@app.route("/api/flights/alternative-routes", methods=["POST"])
def api_alternatives():
    data = request.get_json(silent=True) or {}
    return jsonify(backtracking_routes(
        data.get("source", "").upper(),
        data.get("destination", "").upper(),
        max_stops=int(data.get("max_stops", 2)),
        excluded=data.get("excluded_airports", []),
        max_dist=data.get("max_distance")
    ))

@app.route("/api/flights/benchmark")
def api_benchmark():
    tests = [("DEL", "LHR"), ("BOM", "JFK"), ("DEL", "SFO"), ("BLR", "SYD"), ("FRA", "SIN")]
    results = []
    for s, d in tests:
        d_res = dijkstra(s, d)
        b_res = backtracking_routes(s, d, max_stops=2)
        results.append({
            "pair": f"{s} → {d}",
            "dijkstra_dist": d_res.get("total_distance_km"),
            "dijkstra_time_ms": d_res.get("execution_time_ms"),
            "dijkstra_nodes": d_res.get("visited_nodes"),
            "bt_routes": b_res.get("routes_count"),
            "bt_time_ms": b_res.get("execution_time_ms"),
            "bt_calls": b_res.get("statistics", {}).get("calls")
        })
    return jsonify({"success": True, "results": results})

if __name__ == "__main__":
    print("✈️  AeroOptima Server running at http://localhost:5000")
    app.run(host="0.0.0.0", port=5000, debug=True)
