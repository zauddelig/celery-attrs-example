import attr


@attr.s(auto_attribs=True)
class OrderLine:
    id: int
    quantity: int
    price: float
