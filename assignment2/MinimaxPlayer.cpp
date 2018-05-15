/*
 * MinimaxPlayer.cpp
 *
 *  Created on: May 1, 2018
 *      Author: Garrett Haley
 */
#include <iostream>
#include <assert.h>
#include "MinimaxPlayer.h"
#include <algorithm>
#include <limits>
using std::vector;

MinimaxPlayer::MinimaxPlayer(char symb) :
	Player(symb) {

	}

MinimaxPlayer::~MinimaxPlayer() {

}

void MinimaxPlayer::get_move(OthelloBoard* b, int& col, int& row) {
	minimax(b,col,row);
}

int MinimaxPlayer::get_Utility(OthelloBoard *b) {
	int player1Score = b->count_score(b->get_p1_symbol());
	int player2Score = b->count_score(b->get_p2_symbol());
	return player1Score - player2Score;
}

vector<OthelloBoard*> MinimaxPlayer::get_Successors(char symbol, OthelloBoard *b) {
	vector<OthelloBoard*> successors;
	for (int i = 0; i < 4; i++) {
		for (int j = 0; j < 4; j++) {
			if (b->is_legal_move(i, j, symbol)) {
				OthelloBoard* temp = new OthelloBoard(*b);
				successors.push_back(temp);
				successors.back()->play_move(i, j, symbol);
				successors.back()->setCol(i);
				successors.back()->setRow(j);
			}
		}
	}

	return successors;
}
void MinimaxPlayer::minimax(OthelloBoard* b, int& col, int& row) {
        int best = 10000;
        int bestRow = 0;
        int bestCol = 0;
        for (int i = 0; i<4; i++){
                for (int j = 0; j<4; j++){
                        OthelloBoard* temp = new OthelloBoard(*b);
                        if (temp->is_legal_move(i,j,'O')){
                                temp->play_move(i,j,'O');
                                temp->setCol(i);
                                temp->setRow(j);
                                int moveEval = maximumPlayer(temp);
                                if (moveEval < best){
                                        bestCol = i;
                                        bestRow = j;
                                        best = moveEval;
                                        std::cout<<best<<std::endl;
                                }
                        }
                }
        }
        col = bestCol;
        row = bestRow;
}
int MinimaxPlayer::minimumPlayer(OthelloBoard* b){
	int v = 0;
	int bestValue = std::numeric_limits<int>::max();
	vector<OthelloBoard*> successors = get_Successors(b->get_p2_symbol(),b);
	if (successors.empty())
		return get_Utility(b);
	for (int x = 0;x<successors.size();x++){
		v = maximumPlayer(successors[x]);
		bestValue = std::min(bestValue,v);
	}
	return bestValue;
	
}
int MinimaxPlayer::maximumPlayer(OthelloBoard* b){
        int v = 0;
        int bestValue = -std::numeric_limits<int>::max();
        vector<OthelloBoard*> successors = get_Successors(b->get_p1_symbol(),b);
      	 if(successors.empty())
                return get_Utility(b);
        for (int x = 0;x<successors.size();x++){
                v = minimumPlayer(successors[x]);
                bestValue = std::max(bestValue,v);
        }
        return bestValue;

}

MinimaxPlayer* MinimaxPlayer::clone() {
	MinimaxPlayer* result = new MinimaxPlayer(symbol);
	return result;
}
