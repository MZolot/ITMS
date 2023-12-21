class DataEntry:
    def __init__(self, name, label_text, default_value, unit, is_float=False):
        self.name = name
        self.label_text = label_text
        self.default_value = default_value
        self.unit = unit
        self.__current_value = None
        self.is_float = is_float

    def get_current_value(self):
        if self.__current_value is None:
            return self.default_value
        else:
            return self.__current_value

    def set_current_value(self, value):
        if self.is_float:
            self.__current_value = float(value)
        else:
            self.__current_value = int(value)

    def __str__(self):
        return self.label_text + " " + str(self.get_current_value()) + " " + self.unit
