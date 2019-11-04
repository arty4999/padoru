import secrets


def coin_flip():
    coins = ["Heads", "Tails"]
    return random_select(coins)


def random_select(items):
    return secrets.choice(items)
