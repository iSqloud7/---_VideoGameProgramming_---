extends Label

var time_elapsed: float = 70.0
var counting: bool = false  

func _ready() -> void:
	text = "TIME: 0"
	counting = true  

func _process(delta: float) -> void:
	if counting:
		time_elapsed -= delta
		text = "TIME: " + str(int(time_elapsed)) 
