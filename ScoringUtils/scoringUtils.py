#!/usr/bin/env python

# This function takes in a list of seeds that competed
# in a round within a region, listed from top to bottom
# in the official bracket format. It also takes a list
# of results, where a 1 (0) indicates the top (bottom) 
# team won. It outputs a list of the seeds in the next
# round, i.e., the winners of the given round.
def applyRoundResults(seeds, results):
	nGames = len(results)
	return [seeds[2*i] * results[i] + seeds[2*i+1] * (1 - results[i]) for i in range(nGames)]

# This function scores a bracket vector according to the 
# ESPN Bracket Challenge scoring system. The isPickFavorite
# flag indicates whether the bracket being scored is from the
# Pick Favorite model, in which case we assume that it correctly
# guesses the Final Four and National Championship outcomes.
def scoreBracket(bracketVector, actualResultsVector, isPickFavorite = False):
	# Round score subtotals, with only indices 1-6 used
	# as actual subtotals. The 0th element is the overall total.
	roundScores = [0, 0, 0, 0, 0, 0, 0]

	regionWinners = []
	actualRegionWinners = []

	# Compute Rounds 1-4 scores
	for region in range(4):
		start = 15 * region
		end = start + 8
		regionVector = bracketVector[start:end]
		regionResultsVector = actualResultsVector[start:end]

		seeds = [1, 16, 8, 9, 5, 12, 4, 13, 6, 11, 3, 14, 7, 10, 2, 15]
		actualSeeds = [1, 16, 8, 9, 5, 12, 4, 13, 6, 11, 3, 14, 7, 10, 2, 15]

		for r in range(1, 5):
			seeds = applyRoundResults(seeds, regionVector)
			actualSeeds = applyRoundResults(actualSeeds, regionResultsVector)

			matches = [i for i, j in zip(seeds, actualSeeds) if i == j]
			roundScores[r] += 10 * (2 ** (r-1)) * len(matches)

			start = end
			end += int(len(seeds) / 2)
			regionVector = bracketVector[start:end]
			regionResultsVector = actualResultsVector[start:end]

		regionWinners.append(seeds[0])
		actualRegionWinners.append(actualSeeds[0])

	# Compute Rounds 5-6 scores
	finalFourVector = bracketVector[-3:]
	actualFinalFourVector = actualResultsVector[-3:]

	if isPickFavorite:
		finalFourVector = actualFinalFourVector

	isCorrectFirstSemifinal = (finalFourVector[0] == actualFinalFourVector[0]) and ((finalFourVector[0] == 1 and (regionWinners[0] == actualRegionWinners[0])) or (finalFourVector[0] == 0 and (regionWinners[1] == actualRegionWinners[1])))
	if isCorrectFirstSemifinal:
		roundScores[5] += 160

	isCorrectSecondSemifinal = (finalFourVector[1] == actualFinalFourVector[1]) and ((finalFourVector[1] == 1 and (regionWinners[2] == actualRegionWinners[2])) or (finalFourVector[1] == 0 and (regionWinners[3] == actualRegionWinners[3])))

	if isCorrectSecondSemifinal:
		roundScores[5] += 160

	isCorrectChampion = (finalFourVector[2] == actualFinalFourVector[2]) and ((finalFourVector[2] == 1 and isCorrectFirstSemifinal) or (finalFourVector[2] == 0 and isCorrectSecondSemifinal))
	if isCorrectChampion:
		roundScores[6] += 320

	roundScores[0] = sum(roundScores)
	return roundScores
	

	
# This Funciton changes a bracket that uses a
# representation other than TTT into a TTT bracket.
# It takes in a bracket of some form other than TTT
# and a set of scores. The scores should be an array of
# 64 ints representing the score of a given team.
# If the score changes between rounds, then the 
# rounds_are_different flag should be set, and the array that
# is passed in should be a 6x64 2-D array where "scores[i][j]"
# is the score for the ith team in the jth round.
#
# The assumption is that a 1 represents the lower score 
# winning (unless the higher_score_win flag is set). 
# In the case of a tie, we assume a 1 represents the top 
# team winning.
def change_to_TTT(bracket, scores, high_score_win=False, rounds_are_different=False):

	new_bracket = [0]*63
	current_game_indicies = [i for i in range(64)]	
	

	for round in range(0, 6):
		next_game_indicies = []
		score_index = 0
		if rounds_are_different:
			current_scores = scores[round]
		else:
			current_scores = scores
		
		#regions only apply in rounds 1-4
		end_region=1
		if round <=3:
			end_region = 4

		for region in range(0, end_region):
			offset=0
			if(round<=3):
				offset = region*15
				for j in range(0, round):
					offset += 2**(3-j)
			else:
				offset = 60 + 2*(round-4)
			end_game = 2**(3-round)
			if(round>3):
				end_game = (6-round)
			for game in range (0, end_game):
				#Top team wins
				if ((bracket[game+offset] and current_scores[current_game_indicies[score_index]] < current_scores[current_game_indicies[score_index + 1]] and not high_score_win) or
						(bracket[game+offset] and current_scores[current_game_indicies[score_index]] > current_scores[current_game_indicies[score_index + 1]] and high_score_win) or
						(not bracket[game+offset] and current_scores[current_game_indicies[score_index]] > current_scores[current_game_indicies[score_index+1]] and not high_score_win) or
						(not bracket[game+offset] and current_scores[current_game_indicies[score_index]] < current_scores[current_game_indicies[score_index + 1]] and high_score_win) or
						(bracket[game+offset] and current_scores[current_game_indicies[score_index]] == current_scores[current_game_indicies[score_index+1]])):
					new_bracket[game+offset] = 1
					next_game_indicies.append(current_game_indicies[score_index])
				#otherwise bottom team wins
				else:
					new_bracket[game+offset] = 0
					next_game_indicies.append(current_game_indicies[score_index+1])
				
				score_index+=2
		current_game_indicies = next_game_indicies
		
	return new_bracket