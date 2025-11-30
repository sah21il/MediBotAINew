# utils/health_chart_memory.py

class HealthChartMemory:
    def __init__(self):
        self.history = []

    def store(self, graph_points: dict):
        self.history.append(graph_points)
        if len(self.history) > 50:  # limit memory
            self.history.pop(0)

    def get_all(self):
        return self.history
