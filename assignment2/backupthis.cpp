/*
 * MinimaxPlayer.cpp
 *
 *  Created on: Apr 17, 2015
 *      Author: wong
 */
#include <iostream>
#include <assert.h>
#include "MinimaxPlayer.h"
#include <algorithm>
using std::vector;

MinimaxPlayer::MinimaxPlayer(char symb) :
		Player(symb) {

}

MinimaxPlayer::~MinimaxPlayer() {

}

void MinimaxPlayer::get_move(OthelloBoard* b, int& col, int& row) {
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
				int moveEval = minimax(temp,false);
				std::cout<<i;
				std::cout<<j;
				std::cout<<moveEval;
				if (moveEval < best){
					bestCol = i;
					bestRow = j;
					best = moveEval;
	//				temp->display();
			//		std::cout<<i;
			//		std::cout<<j;
			//		std::cout<<best
				}
 			}
        	}
    	}
	col = bestCol;
	row = bestRow;
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
				successors.push_back(new OthelloBoard(*b));
				successors.back()->play_move(i, j, symbol);
				successors.back()->setCol(i);
				successors.back()->setRow(j);
			}
		}
	}

	return successors;
}
int MinimaxPlayer::minimax(OthelloBoard* b, bool maximizingPlayer){
	int bestValue;
	int v;
	vector<OthelloBoard*> successors;
	switch(maximizingPlayer){
	case true: successors = get_Successors('X',b);
	case false: successors = get_Successors('O',b);
	}
	if(successors.empty()){
		b->display();
		return get_Utility(b);
	}
	if(maximizingPlayer){
		bestValue = -10000;
		for (int x=0;x<successors.size();x++){
			v = minimax(successors[x],false);
			bestValue = std::max(bestValue,v);
		return bestValue;		
		}
	}
	else{
		bestValue = 10000;
		for (int x=0;x<successors.size();x++){
			v = minimax(successors[x], true);
			bestValue = std::min(bestValue,v);
		}
		return bestValue; 
	}
}		

MinimaxPlayer* MinimaxPlayer::clone() {
	MinimaxPlayer* result = new MinimaxPlayer(symbol);
	return result;
}
