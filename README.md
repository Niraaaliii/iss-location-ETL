# ISS Location Tracker

This project tracks the International Space Station (ISS) location and visualizes its path using free tools. It's designed to be developed in GitHub Codespaces.

## Project Structure
```
.
├── src/
│   ├── main.py           # Main application entry point
│   ├── fetch_iss_data.py # ISS location fetching functionality
│   └── store_data.py     # Database operations
├── data/                 # Directory for storing the SQLite database
├── requirements.txt      # Project dependencies
└── README.md            # Project documentation
```

## Setup Instructions

1. Clone the repository
2. Set up the virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```
3. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

Run the main script with optional parameters:

```bash
# Default: 5 minutes duration, 30 second intervals
python src/main.py

# Custom duration and interval
python src/main.py --duration 600 --interval 60
```

### Command Line Arguments

- `--duration`: Duration in seconds to collect data (default: 300)
- `--interval`: Interval in seconds between collections (default: 30)

### Error Handling

The application includes robust error handling:
- Network errors: The application will log the error and continue
- Database errors: Errors will be logged and the application will exit gracefully
- Keyboard interruption: The application can be safely stopped with Ctrl+C

### Logging

All operations are logged with timestamps and appropriate log levels:
- INFO: Normal operation messages
- ERROR: Issues with data collection or storage

Logs are stored in two locations:
1. Console output (stdout) during execution
2. Log file at `logs/iss_tracker.log`

To view logs:
```bash
# View complete log file
cat logs/iss_tracker.log

# View last 50 lines of logs
tail -n 50 logs/iss_tracker.log

# Follow logs in real-time
tail -f logs/iss_tracker.log

# Search logs for errors
grep "ERROR" logs/iss_tracker.log
```