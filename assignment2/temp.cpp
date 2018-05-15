/*
 * MinimaxPlayer.cpp
 *
 *  Created on: Apr 17, 2015
 *      Author: wong
 */
#include <iostream>
#include <assert.h>
#include "MinimaxPlayer.h"

using std::vector;

MinimaxPlayer::MinimaxPlayer(char symb) :
		Player(symb) {

}

MinimaxPlayer::~MinimaxPlayer() {

}

void MinimaxPlayer::get_move(OthelloBoard* b, int& col, int& row) {
	switch(b->get_p1_symbol()){
		case 'X': get_Max(b, col, row,'X');
		case 'O': get_Max(b, col, row, 'O'); 
	}
}

int MinimaxPlayer::get_Utility(OthelloBoard *b) {
	return b->count_score(b->get_p1_symbol()) - b->count_score(b->get_p2_symbol());
}

vector<OthelloBoard*> MinimaxPlayer::get_Successors(char symbol, OthelloBoard *b) {
	vector<OthelloBoard*> successors;
	for (int i = 0; i < 4; i++) {
		for (int j = 0; j < 4; j++) {
			if (b->is_legal_move(i, j, playerSymbol)) {
				successors.push_back(new OthelloBoard(*b));
				successors.back()->play_move(i, j, symbol);
				successors.back()->setColumn(i);
				boardVector.back()->setRow(j);
			}
		}
	}

	return successors;
}

int MinimaxPlayer::get_Max(OthelloBoard* b, int& col, int& row, char symbol){
	vector<OthelloBoard*> successors;
	int max = -100000;
	int rowMax = 0;
	int colMax = 0;
	switch(symbol){
		case 'X': successors = get_Successors('X',b);
		case 'O': successors = get_Successors('O',b);
	}
	if (successors.size() == 0)
		return get_Utility(b);
	for (int x = 0; x < successors.size(); x++) {
		if (get_Min(successors[x],col,row,symbol) > max) {
			rowMax = successors[x]->getRow();
			colMax = successors[x]->getColumn();
			max = get_Min(successors[x], col, row, symbol);
		}
	}

	row = rowMax;
	col = colMax;
	return max;
}
int MinimaxPlayer::get_Min(OthelloBoard* b, int& col, int& row, char symbol){
        vector<OthelloBoard*> successors;
        int min = 100000;
        int rowMin = 0;
	int colMin = 0;
        switch(symbol){
                case 'X': successors = get_Successors('X',b);
                case 'O': successors = get_Successors('O',b);
        }
	if (successors.size() == 0)
		return get_Utility(b);
        for (int x = 0; x < successors.size(); x++) {
                if (get_Max(successors[x],col,row,symbol) > min) {
                        rowMin = successors[x]->getRow();
                        colMin = successors[x]->getColumn();
                        min = get_Max(successors[x], col, row, symbol);
                }
        }

        row = rowMin;
        col = colMin;
        return min;
}


MinimaxPlayer* MinimaxPlayer::clone() {
	MinimaxPlayer* result = new MinimaxPlayer(symbol);
	return result;
}
