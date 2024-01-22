def create_liderboard(players):
    liderboard = ["Игрок    результат"]
    for player in players:
        liderboard.append(f"{player[1]}:       {player[3]}")
    return liderboard
