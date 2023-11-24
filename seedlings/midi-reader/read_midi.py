import mido
print(mido.get_output_names())

print(mido.get_input_names())

INPUT_NAME = 'A2M virtual port'

with mido.open_input(INPUT_NAME) as inport:
    for msg in inport:
        print(msg)

# the A2M virtual port seems to not super be worknig :(