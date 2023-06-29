class Business:
    def __init__(self, name, number, description, website):
        self.name = name
        self.number = number
        self.description = description
        self.website = website

    def to_dict(self):
        return {
            "Name": self.name,
            "Phone Number": self.number,
            "Description": self.description,
            "Website": self.website
        }
