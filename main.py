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
        response = response.json()
        some_stuff = {}
        for i in response["spans"]:
            date = datetime.fromtimestamp(i["start_time"]).date()
            if date not in some_stuff:
                some_stuff[date] = i["duration"]
            else:
                some_stuff[date] += i["duration"]
        return some_stuff
    def retrieve_data(self, year: int) -> ActivityHeatmap.ActivityData:
        # So like we setting the data ig? basically give value for every day of year(adding COLOR)
        template = ActivityHeatmap.generate_empty_activity(year)
        data: ActivityHeatmap.ActivityData = defaultdict(float)
        more_data = self.get_hackatime_year(year, "shn")
        for week in template:
            for day in week:
                if day is not None:
                    if day in more_data:
                        data[day] = float(more_data[day])
                    else:
                        data[day] = 0.0
        return data

    def set_heatmap_data(self, year: int) -> None:
        """Sets the data based on the current data."""
        self.query_one(ActivityHeatmap).values = self.retrieve_data(year)

    def _on_mount(self) -> None:
        self.set_heatmap_data(2025)

    def compose(self) -> ComposeResult:
        yield HeatmapManager(2025)

if __name__ == "__main__":
    ActivityApp().run()