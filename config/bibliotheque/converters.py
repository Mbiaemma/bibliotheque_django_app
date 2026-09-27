class ISBNConverter:
    regex = "[0-9]{3}-[0-9]-[0-9]{4}-[0-9]{4}-[0-9]"

    def to_python(self, value):
        return value.replace("-", "")

    def to_url(self, value):
        return f"{value[:3]}-{value[3]}-{value[4:8]}-{value[8:12]}-{value[12]}"