from textual.app import App, ComposeResult
from textual_timepiece.activity_heatmap import ActivityHeatmap, HeatmapManager
import random
random.seed(2012)
ActivityHeatmap.generate_empty_activity(2012)
print(ActivityHeatmap.generate_empty_activity(2012))