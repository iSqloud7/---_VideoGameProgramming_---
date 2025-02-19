extends Node3D

@onready var timer = $GameTimer
@onready var timer_label = $Control/LabelTimer

var coins_collected = 0
var total_coins = 0

const WIN_SCENE = preload("res://Assets/you_won.tscn")
const LOST_SCENE = preload("res://Assets/game_over.tscn")

# Called when the node enters the scene tree for the first time.
func _ready() -> void:
	total_coins = get_tree().get_nodes_in_group("coins").size()
	print("Total coins in the scene: ", total_coins)
	timer.start()
	timer.timeout.connect(_on_game_timer_timeout)
	
	for coin in get_tree().get_nodes_in_group("coins"):
		coin.connect("coinCollected", _on_coin_coin_collected)

# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta: float) -> void:
	pass


func _on_game_timer_timeout() -> void:
	show_end_screen(false)


func _on_coin_coin_collected() -> void:
	coins_collected += 1
	print("Coins collected:", coins_collected, "/", total_coins)

	if coins_collected >= total_coins:
		show_end_screen(true)
		
func show_end_screen(won: bool):
	get_tree().paused = false  # Pause game
	var scene_to_load = WIN_SCENE if won else LOST_SCENE
	print("Loading scene:", scene_to_load.resource_path)  # Debugging
	get_tree().change_scene_to_packed(scene_to_load)
