extends Area3D

signal coin_collected

func _physics_process(delta):
	rotate_y(deg_to_rad(3))


func _on_body_entered(body: Node3D) -> void:
	if body.name == "StrikeSphere":
		$AnimationPlayer.play("bounce")
		$Timer.start()


func _on_timer_timeout():
	emit_signal("coin_collected")
	queue_free()

func _ready():
	add_to_group("player")
