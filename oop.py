class Devs:
    def __init__(self, name, partner):
        self.name = name
        self._partner = partner

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not isinstance(value, str) or value.strip() == "":
            raise ValueError("Name must be a non-empty string")
        self._name = value

    @property
    def partner(self):
        return self._partner

    @partner.setter
    def partner(self, value):
        if value not in ["Abhishek", "Shaurya"]:
            raise ValueError(" must be Abhishek or Shaurya")
        self._partner = value

    def __str__(self):
        return f"Dev {self.name} is paired with {self.partner}"


d1 = Devs("Abhishek", "Nobody")
print(d1)
d1.partner = "RandomGuy"
print(d1)
d2 = Devs("Shaurya", "Abhishek")
print(d2)
