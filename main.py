from textual.app import App, ComposeResult
from textual_timepiece.activity_heatmap import ActivityHeatmap, HeatmapManager
import requests
import random
from collections import defaultdict
import datetime as dt
from datetime import datetime
class ActivityApp(App[None]):
    def _on_heatmap_manager_year_changed(
        self,
        message: HeatmapManager.YearChanged,
    ) -> None:
        message.stop()
        self.set_heatmap_data(message.year)
    def get_hackatime_year(self, year, username):
        start_date = dt.datetime(year, 1, 1)
        end_date = dt.datetime(year, 12, 31)
        payload = {'start_date': start_date.isoformat(), 'end_date': end_date.isoformat()}
        url = f"https://hackatime.hackclub.com/api/v1/users/{username}/heartbeats/spans"
        response = requests.get(url, params=payload)
    def hackatime_day(self, data, day):
        
    def retrieve_data(self, year: int) -> ActivityHeatmap.ActivityData:
        # So like we setting the data ig? basically give value for every day of year(adding COLOR)
        template = ActivityHeatmap.generate_empty_activity(year)
        data = defaultdict(lambda: defaultdict(int))
        more_data = self.get_hackatime_year(year, "shn")
        for week in template:
            for day in week:
                

    def set_heatmap_data(self, year: int) -> None:
        """Sets the data based on the current data."""
        self.query_one(ActivityHeatmap).values = self.retrieve_data(year)

    def _on_mount(self) -> None:
        self.get_hackatime_day_heatmap("bleh")
        self.set_heatmap_data(2025)

    def compose(self) -> ComposeResult:
        yield HeatmapManager(2025)

if __name__ == "__main__":
    ActivityApp().run()