class Player:

    def __init__(self, name, team = None, noc = None, year = None, city = None, event = None, medal = None):
        self.name = name
        self.team = team
        self.noc = noc
        self.year = year
        self.city = city
        self.event = event
        self.medal = medal

    def __str__(self):
        return (f"Name: {self.name}\n"
                f"Team: {self.team}\n"
                f"NOC: {self.noc}\n"
                f"year: {self.year}\n"
                f"city: {self.city}\n"
                f"event: {self.event}\n"
                f"medal: {self.medal}\n")
