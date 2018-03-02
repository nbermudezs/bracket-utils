import scoringUtils as score
import json

#read FFF brackets
in_file = open("allBracketsFFF.json")
json_brackets = json.load(in_file)
all_FFF_brackets = []
for b in json_brackets['brackets']:
	bracket_vector = []
	for c in b['bracket']['fullvector']:
		bracket_vector.append(int(c))
	all_FFF_brackets.append(bracket_vector)	
in_file.close()

#read FFF brackets
in_file = open("allBracketsTTT.json")
json_brackets = json.load(in_file)
all_TTT_brackets = []
for b in json_brackets['brackets']:
	bracket_vector = []
	for c in b['bracket']['fullvector']:
		bracket_vector.append(int(c))
	all_TTT_brackets.append(bracket_vector)	
in_file.close()

seed_vector = [[1,16,8,9,5,12,4,13,6,11,3,14,7,10,2,15,1,16,8,9,5,12,4,13,6,11,3,14,7,10,2,15,1,16,8,9,5,12,4,13,6,11,3,14,7,10,2,15,1,16,8,9,5,12,4,13,6,11,3,14,7,10,2,15],
				[1,16,8,9,5,12,4,13,6,11,3,14,7,10,2,15,1,16,8,9,5,12,4,13,6,11,3,14,7,10,2,15,1,16,8,9,5,12,4,13,6,11,3,14,7,10,2,15,1,16,8,9,5,12,4,13,6,11,3,14,7,10,2,15],
				[1,16,8,9,5,12,4,13,6,11,3,14,7,10,2,15,1,16,8,9,5,12,4,13,6,11,3,14,7,10,2,15,1,16,8,9,5,12,4,13,6,11,3,14,7,10,2,15,1,16,8,9,5,12,4,13,6,11,3,14,7,10,2,15],
				[1,16,8,9,5,12,4,13,6,11,3,14,7,10,2,15,1,16,8,9,5,12,4,13,6,11,3,14,7,10,2,15,1,16,8,9,5,12,4,13,6,11,3,14,7,10,2,15,1,16,8,9,5,12,4,13,6,11,3,14,7,10,2,15],
				[1]*64, [1]*64]
				

for i in range(0, len(all_TTT_brackets)):
	new_TTT = score.change_to_TTT(all_FFF_brackets[i], seed_vector, rounds_are_different=True)
	if(new_TTT != all_TTT_brackets[i]):
		print("Failure", 1985+i)
	else:
		print("Success!", 1985+i)
