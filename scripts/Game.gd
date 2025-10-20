extends Node2D

var total_items: int = 0
var collected: int = 0
@onready var label: Label = $UI/HUD/Label
@onready var progress: ProgressBar = $UI/HUD/ProgressBar
@onready var overlay: ColorRect = $DarknessOverlay
@export var start_darkness: float = 0.6

func _ready() -> void:
    var items = get_tree().get_nodes_in_group("collectibles")
    total_items = items.size()
    for item in items:
        item.collected.connect(_on_item_collected)
    _update_ui()

func _on_item_collected() -> void:
    collected += 1
    _update_ui()
    if total_items > 0 and collected >= total_items:
        await get_tree().create_timer(0.5).timeout
        _on_level_complete()

func _update_ui() -> void:
    if is_instance_valid(label):
        label.text = "Itens: %d / %d" % [collected, total_items]
    if is_instance_valid(progress):
        progress.max_value = max(total_items, 1)
        progress.value = collected
    var c := overlay.color
    var t: float = 0.0
    if total_items > 0:
        t = float(collected) / float(total_items)
    c.a = lerp(start_darkness, 0.0, t)
    overlay.color = c

func _on_level_complete() -> void:
    if is_instance_valid(label):
        label.text += "  — Cidade iluminada! ✨"
