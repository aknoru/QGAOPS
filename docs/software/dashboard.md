# Software-only dashboard

The dependency-free dashboard reads actual generated benchmark and gesture
fixture JSON files. Generate them first:

```powershell
.\.venv\Scripts\python.exe scripts\run_benchmark.py
.\.venv\Scripts\python.exe scripts\run_gesture_fixture.py
.\.venv\Scripts\python.exe -m software.dashboard.app
```

Open `http://127.0.0.1:8000/`. The `/api/status` endpoint exposes the stored
software results and explicitly reports that hardware is not integrated.
