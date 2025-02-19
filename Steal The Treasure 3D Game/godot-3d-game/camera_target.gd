extends Camera3D

@export var target: Camera3D  # Changed from Node3D to Camera3D
@export var follow_speed: float = 5.0
@export var camera_offset: Vector3 = Vector3(0, 2, -5)  # Decrease the negative Z offset

func _ready():
	if target == null:
		print("ERROR: Target is NOT assigned!")
		return

	print("Camera Ready! Initial Position:", global_transform.origin)

func _process(delta):
	if target == null:
		return

	var target_position = target.global_transform.origin + camera_offset
	global_transform.origin = global_transform.origin.lerp(target_position, follow_speed * delta)

	look_at(target.global_transform.origin)

	# Debugging output
	print("Camera Position:", global_transform.origin, " Target Position:", target.global_transform.origin)
