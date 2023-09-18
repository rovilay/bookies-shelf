# bookies-shelf app

## Monitoring
This app uses [Prometheus](https://prometheus.io/) to get app metrics. You can use Grafana to visualize these metrics
1. Install [Prometheus](https://prometheus.io/docs/prometheus/latest/installation/) (if you haven't)
2. Install [Grafana](https://grafana.com/docs/grafana/latest/setup-grafana/installation/) (if you haven't)
3. Start the application
4. Open a new tab and cd to project path (to use the prometheus.yml config); run `prometheus` to start prometheus server and scrape app data
5. Start the [Grafana server](https://grafana.com/docs/grafana/latest/setup-grafana/start-restart-grafana/)
6. Configure [Grafana data source](https://grafana.com/blog/2022/01/27/video-how-to-build-a-prometheus-query-in-grafana/)
7. Configure [Grafana dashboard](https://grafana.com/blog/2022/01/26/video-how-to-set-up-a-prometheus-data-source-in-grafana/)