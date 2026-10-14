def format_price(amt):
    return "$%d.%d" % (int(amt), int(amt * 100) % 100)


def summary(cart):
    lines = ["%s x%d" % (name, item["qty"]) for name, item in sorted(cart.items.items())]
    lines.append("total " + format_price(cart.total()))
    return "\n".join(lines)
