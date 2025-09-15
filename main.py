from src.weather_mockup_nomcp import WeatherMonitorMockup


def main():
    scheduler = WeatherMonitorMockup()
    scheduler.run_monitoring()


if __name__ == "__main__":
    main()
