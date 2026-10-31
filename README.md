# AeroOptima: Flight Route Optimization System
### MCA DAA (Design and Analysis of Algorithms) Mini Project

AeroOptima is packaged into **one Python file** and **one HTML file**:

- **[`app.py`](file:///c:/Users/Aryan%20Kumar/Desktop/CU/Sem%201/mini%20project/Smart%20Logistics%20&%20Delivery%20Optimization%20System/app.py)** (~220 lines):
  - Verified IATA coordinates for international & domestic hubs.
  - Verified non-stop commercial flight connections.
  - Haversine great-circle geodesic formula.
  - **Dijkstra's Algorithm** from scratch using a Min-Priority Queue (`heapq`).
  - **Recursive Backtracking** from scratch with cycle avoidance, max layovers, and hub exclusion.
  - Clean Flask REST API endpoints & static web server.
- **[`index.html`](file:///c:/Users/Aryan%20Kumar/Desktop/CU/Sem%201/mini%20project/Smart%20Logistics%20&%20Delivery%20Optimization%20System/index.html)** (~250 lines):
  - Standalone single-page frontend using React 18, Leaflet, and Tailwind CSS via CDN.
  - Interactive Leaflet dark radar map with pulsing origin & destination markers.
  - Source/Destination selectors, layover slider, and bypass hub toggles.
  - Route comparison list & live DAA benchmark comparison table.

---

## 🚀 How to Run

```bash
python app.py
```
Open **`http://localhost:5000`** in your browser.
