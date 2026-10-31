# ✈️ AeroOptima -- Flight Route Optimization System

> **Optimizing flight journeys through intelligent graph algorithms.**

AeroOptima is a web-based **Design and Analysis of Algorithms (DAA) mini
project** that demonstrates flight route planning using graph
algorithms. It uses **Dijkstra's Algorithm** to calculate a
minimum-distance route and **Recursive Backtracking with Pruning** to
generate alternative routes between airports.

The application provides an interactive map for visualizing airport
locations and selected routes, along with a benchmark page for comparing
algorithm execution statistics.

------------------------------------------------------------------------

## Features

-   **Shortest Route:** Find a minimum-distance route using Dijkstra's
    Algorithm with a min-heap priority queue.
-   **Alternative Routes:** Explore alternative paths using recursive
    depth-first search and backtracking.
-   **Constraint Handling:** Set a maximum number of intermediate
    layovers and exclude selected airports from alternative-route
    searches.
-   **Geographic Distance:** Calculate great-circle distances using the
    Haversine formula.
-   **Interactive Map:** Visualize airports, predefined connections, and
    selected routes using Leaflet and OpenStreetMap.
-   **Performance Benchmarking:** Compare execution time, visited nodes,
    alternative route counts, and recursive search calls across five
    predefined airport pairs.

## Algorithms Used

### 1. Dijkstra's Shortest Path Algorithm

Dijkstra's algorithm calculates a minimum-cost path in a graph with
non-negative edge weights. AeroOptima uses geographic distance in
kilometres as the edge weight and a min-heap priority queue to select
the next airport to process.

**Time complexity:** `O((V + E) log V)` with an adjacency list and
binary min-heap.

### 2. Recursive Backtracking with Pruning

The alternative-route feature explores simple paths using recursive
depth-first search. It prunes paths that: - Revisit an airport already
in the current path. - Use an excluded airport. - Exceed the configured
maximum number of intermediate layovers. - Exceed the optional
maximum-distance constraint, when supplied to the API.

The returned routes are sorted by total distance. The current
implementation returns up to eight routes by default.

**Complexity:** Exponential in the worst case, since the number of
possible simple paths can grow exponentially.

### 3. Haversine Formula

The Haversine formula estimates the great-circle distance between two
airport coordinates using latitude and longitude. The implementation
uses an Earth radius of **6,371 km**.

------------------------------------------------------------------------

## Technology Stack

  Technology       Purpose
  ---------------- --------------------------------------
  Python           Backend and algorithm implementation
  Flask            Web server and REST API
  Flask-CORS       Cross-origin request support
  HTML5 / CSS      Frontend structure and styling
  JavaScript       Frontend logic and API communication
  Tailwind CSS     User-interface styling
  Leaflet.js       Interactive map visualization
  OpenStreetMap    Map tile source
  Python `heapq`   Min-heap priority queue
  Python `math`    Haversine distance calculations
  Python `time`    Algorithm execution-time measurement

## Project Structure

``` text
AeroOptima/
├── app.py       # Flask backend, airport data, graph and algorithms
├── index.html      # Frontend interface and interactive map
└── README.md       # Project documentation
```

## Requirements

-   Python 3
-   Flask
-   Flask-CORS
-   A modern web browser
-   Internet connection for loading CDN libraries and OpenStreetMap
    tiles

## Installation and Setup

### 1. Clone the repository

``` bash
git clone https://github.com/Aruack/Aerooptima-flight
cd Aerooptima-flight
```

Replace the placeholders with your actual GitHub repository URL and
folder name.

### 2. Install dependencies

``` bash
pip install flask flask-cors
```

### 3. Run the application

``` bash
python "app.py"
```

### 4. Open in your browser

Visit:

``` text
http://localhost:5000
```

Keep the terminal running while using the application.

## How to Use

1.  Start the Flask server.
2.  Open the application in your browser.
3.  Select a source airport and destination airport.
4.  Choose **Dijkstra (Shortest)** to calculate the minimum-distance
    route.
5.  Choose **Backtracking (Alternatives)** to explore other possible
    paths.
6.  Adjust the maximum layover count or toggle excluded hubs.
7.  Select an alternative route to display it on the map.
8.  Open **DAA Benchmarks** to run the predefined performance
    comparison.

## REST API Endpoints

  -----------------------------------------------------------------------------------
  Method                  Endpoint                            Description
  ----------------------- ----------------------------------- -----------------------
  `GET`                   `/`                                 Serves the application
                                                              frontend

  `GET`                   `/api/flights/airports`             Returns the airport
                                                              dataset

  `GET`                   `/api/flights/connections`          Returns predefined
                                                              airport connections

  `POST`                  `/api/flights/shortest-route`       Calculates the shortest
                                                              route using Dijkstra

  `POST`                  `/api/flights/alternative-routes`   Generates alternative
                                                              routes using
                                                              backtracking

  `GET`                   `/api/flights/benchmark`            Runs the predefined
                                                              algorithm benchmark
                                                              suite
  -----------------------------------------------------------------------------------

### Example API request

**POST** `/api/flights/shortest-route`

``` json
{
  "source": "DEL",
  "destination": "LHR"
}
```

**POST** `/api/flights/alternative-routes`

``` json
{
  "source": "DEL",
  "destination": "LHR",
  "max_stops": 2,
  "excluded_airports": ["DXB"]
}
```

## Dataset and Important Notes

-   The submitted source code contains **19 airport records** with
    airport codes, names, cities, countries, and coordinates.
-   Direct flight connections and associated airline names are defined
    in a predefined dataset in the backend.
-   The graph builder adds each listed connection in both directions, so
    the current graph treats connections as undirected.
-   Route weights represent Haversine geographic distances, not actual
    flown distances.
-   Airline names are connection metadata; the current algorithms
    optimize distance rather than airline preference.

> **Disclaimer:** AeroOptima is an educational DAA project that
> calculates routes over a predefined airport and connection dataset. It
> does not provide live flight schedules, real-time flight status,
> ticket prices, seat availability, booking services, or certified
> operational flight guidance. The dataset may not reflect current
> airline operations.

## Benchmarking

The benchmark endpoint runs tests for these airport pairs:

-   DEL → LHR
-   BOM → JFK
-   DEL → SFO
-   BLR → SYD
-   FRA → SIN

The benchmark reports Dijkstra distance, execution time and visited
nodes, along with backtracking route count, execution time and recursive
call count. Execution times depend on the machine and current system
load.

## Future Enhancements

-   Integrate an authorized and regularly updated flight-route data
    source.
-   Model directional routes and service availability.
-   Add route optimization based on travel time, fare, number of stops,
    or emissions.
-   Add repeated benchmark runs and statistical summaries.
-   Add automated unit tests and stronger input validation.
-   Add deployment configuration for a hosted demonstration.

## Academic Information

  Field          Details
  -------------- -----------------------------------------------------
  Project        AeroOptima -- Flight Route Optimization System
  Subject        Design and Analysis of Algorithms (DAA)
  Programme      MCA -- Artificial Intelligence and Machine Learning
  Institution    Chandigarh University
  Project Type   DAA Mini Project

## Acknowledgements

This project uses open-source technologies including Python, Flask,
Leaflet, Tailwind CSS, and OpenStreetMap. Refer to their official
documentation for usage and licensing information.

## License

No license is specified in the submitted project files. Add a `LICENSE`
file and select an appropriate license before permitting reuse or
redistribution.
