class DataEntry:
    def __init__(self, name, label_text, default_value, unit, is_float=False):
        self.name = name
        self.label_text = label_text
        self.unit = unit
        self.is_float = is_float
        self.default_value = default_value
        self.current_value = None

    def get_current_value(self):
        if self.current_value is None:
            return self.default_value
        else:
            return self.current_value

    def set_current_value(self, value):
        if self.is_float:
            self.current_value = float(value)
        else:
            self.current_value = int(value)

    def reset_value(self):
        self.current_value = self.default_value

    def __str__(self):
        return self.label_text + " " + str(self.get_current_value()) + " " + self.unit
