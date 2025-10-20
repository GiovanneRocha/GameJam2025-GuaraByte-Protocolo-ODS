extends CharacterBody2D

@export var speed: float = 220.0
@export var jump_velocity: float = -420.0
var gravity: float = ProjectSettings.get_setting("physics/2d/default_gravity")

func _physics_process(delta: float) -> void:
    if not is_on_floor():
        velocity.y += gravity * delta
    var dir := Input.get_axis("ui_left", "ui_right")
    velocity.x = dir * speed
    if is_on_floor() and Input.is_action_just_pressed("ui_accept"):
        velocity.y = jump_velocity
    move_and_slide()
