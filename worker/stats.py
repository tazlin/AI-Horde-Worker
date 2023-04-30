"""Bridge Stats Tracker"""
import json
import time
from collections import deque


class BridgeStats:
    """Convenience functions for the stats"""

    stats = {}  # Deliberately on class level

    def __init__(self):
        self.kudos_record = deque()

    def update_inference_stats(self, model_name, kudos):
        """Updates the stats for a model inference"""
        if "inference" not in self.stats:
            self.stats["inference"] = {}
        if model_name not in self.stats["inference"]:
            self.stats["inference"][model_name] = {"kudos": 0, "count": 0}
        self.stats["inference"][model_name]["count"] += 1
        self.stats["inference"][model_name]["kudos"] = round(self.stats["inference"][model_name]["kudos"] + kudos)
        stats_for_model = self.stats["inference"][model_name]
        self.stats["inference"][model_name]["avg_kpr"] = round(stats_for_model["kudos"] / stats_for_model["count"], 2)

        # Remember the kudos we got awarded over the last hour
        now = time.time()
        too_old = now - 3600
        self.kudos_record.append((kudos, now))
        oldest = self.kudos_record[0][1] if self.kudos_record else now
        while self.kudos_record and self.kudos_record[0][1] < too_old:
            oldest = self.kudos_record.popleft()[1]
        period = now - oldest

        # Calculate the total kudos
        total_kudos = sum(score for score, _ in self.kudos_record)
        # If period is less than an hour, extrapolate
        if period < 3600 and period > 30:
            total_kudos = total_kudos * (3600 / period)
        else:
            total_kudos = 0  # not enough measurements

        if self.kudos_record:
            self.stats["kudos_per_hour"] = round(total_kudos)

    def get_pretty_stats(self):
        """Returns a pretty string of the stats"""
        return json.dumps(self.stats, indent=4)


bridge_stats = BridgeStats()
