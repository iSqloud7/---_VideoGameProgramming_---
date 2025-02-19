extends Label

var coins = 0

func _ready():
	text = str(coins)


func _on_coin_collected():
	coins = coins + 1
	_ready()
