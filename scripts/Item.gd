extends Area2D
signal collected

func _ready() -> void:
    add_to_group("collectibles")
    body_entered.connect(_on_body_entered)

func _on_body_entered(body: Node) -> void:
    if body is CharacterBody2D:
        collected.emit()
        queue_free()
