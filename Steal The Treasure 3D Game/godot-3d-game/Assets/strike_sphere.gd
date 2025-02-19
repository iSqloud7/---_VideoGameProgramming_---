extends CharacterBody3D

const SPEED = 5.0
const JUMP_VELOCITY = 4.5
const GRAVITY = -9.8

func _physics_process(delta: float) -> void:
	# Apply gravity
	if not is_on_floor():
		velocity.y += GRAVITY * delta

	# Handle jump
	if (Input.is_action_just_pressed("ui_accept") or Input.is_action_just_pressed("jump")) and is_on_floor():
		velocity.y = JUMP_VELOCITY

	# Get input direction and handle movement
	var input_dir := Vector2.ZERO
	input_dir.x = Input.get_action_strength("ui_right") - Input.get_action_strength("ui_left")
	input_dir.y = Input.get_action_strength("ui_down") - Input.get_action_strength("ui_up")
	
	var direction := (transform.basis * Vector3(input_dir.x, 0, input_dir.y)).normalized()
	if direction:
		velocity.x = direction.x * SPEED
		velocity.z = direction.z * SPEED
	else:
		velocity.x = move_toward(velocity.x, 0, SPEED)
		velocity.z = move_toward(velocity.z, 0, SPEED)

	move_and_slide()

@export var target : Node3D  # Ова ќе биде референца на таргетот
@export var camera : Camera3D  # Ова ќе биде референца на камерата

func _ready():
	if target == null or camera == null:
		print("Target or Camera is not set!")
		return
	
	# Поставете ја позицијата на камерата
	camera.global_transform.origin = target.global_transform.origin + Vector3(0, 2, -5)

	# Насочете ја камерата кон таргетот
	camera.look_at(target.global_transform.origin, Vector3.UP)
