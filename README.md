# bookies-shelf app

## Server

1. Ensure [python](https://www.geeksforgeeks.org/download-and-install-python-3-latest-version/) is installed on your system
2. In the project app, Navigate to api/
3. on you terminal, change directory (cd) to path/to/server
4. create `.env` from `.env.example`
5. run `pip install -r requirements.txt` to install dependencies
6. run `python -m api.app`
7. run `python -m pytest tests` to run tests

## Client

1. Ensure [node](https://nodejs.org/en) is installed on your system
2. cd to path/to/project/ui
3. run `npm install`
4. run `npm start`

## Monitoring
This app uses [Prometheus](https://prometheus.io/) to get app metrics. You can use Grafana to visualize these metrics
1. Install [Prometheus](https://prometheus.io/docs/prometheus/latest/installation/) (if you haven't)
2. Install [Grafana](https://grafana.com/docs/grafana/latest/setup-grafana/installation/) (if you haven't)
3. Start the application
4. Open a new tab and cd to project path (to use the prometheus.yml config); run `prometheus` to start prometheus server and scrape app data
5. Start the [Grafana server](https://grafana.com/docs/grafana/latest/setup-grafana/start-restart-grafana/)
6. Configure [Grafana data source](https://grafana.com/blog/2022/01/27/video-how-to-build-a-prometheus-query-in-grafana/)
7. Configure [Grafana dashboard](https://grafana.com/blog/2022/01/26/video-how-to-set-up-a-prometheus-data-source-in-grafana/)