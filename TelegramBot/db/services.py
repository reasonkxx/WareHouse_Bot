from db.database import take_item  


def take_item_from_db(name: str, quantity: int, size: str, color: str):
    take_item(name, quantity, size, color)

