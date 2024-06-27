from dataclasses import dataclass


@dataclass
class Product:
    number : int
    name : str



    def __hash__(self):
        return hash(self.number)

    def __str__(self):
        return f"{self.number} - {self.name}"