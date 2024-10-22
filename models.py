class Process:
    name: str
    arrival: int
    duration: int
    io: list[int]
    current_duration: int
    last_entry: int | None

    def __init__(self, name, arrival, duration, io):
        self.name = name
        self.arrival = arrival
        self.duration = duration
        self.io = io
        self.current_duration = 0
        self.last_entry = None