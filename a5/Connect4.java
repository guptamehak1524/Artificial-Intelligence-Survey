import java.util.*;

class Board{
    byte[][] board = new byte[6][7];

    public Board(){
        board = new byte[][]{
                {0,0,0,0,0,0,0,},
                {0,0,0,0,0,0,0,},
                {0,0,0,0,0,0,0,},
                {0,0,0,0,0,0,0,},
                {0,0,0,0,0,0,0,},
                {0,0,0,0,0,0,0,},
        };
    }

    public boolean isLegalMove(int column){
        return board[0][column]==0;
    }

    public ArrayList<Integer> legalMoves(){
        ArrayList<Integer> legal_moves = new ArrayList<>();
        for (int i =0; i < 7; i++) {
            if (board[0][i]== 0){
                legal_moves.add(i);
            }
        }
        return legal_moves;
    }

    //Placing a Move on the board
    public boolean placeMove(int column, int player){
        if(!isLegalMove(column)) {System.out.println("Illegal move!"); return false;}
        for(int i=5;i>=0;--i){
            if(board[i][column] == 0) {
                board[i][column] = (byte)player;
                return true;
            }
        }
        return false;
    }

    public void undoMove(int column){
        for(int i=0;i<=5;++i){
            if(board[i][column] != 0) {
                board[i][column] = 0;
                break;
            }
        }
    }
    //Printing the board
    public void displayBoard(){
        System.out.println();
        for(int i=0;i<=5;++i){
            for(int j=0;j<=6;++j){
                System.out.print(" | " + board[i][j]);
                if (j == 6) {
                    System.out.print(" | ");
                }
            }
            System.out.println();
        }
        System.out.println();
    }
}

public class Connect4 {
    private Board b;
    private Scanner scan;
    private int nextMoveLocation=-1;
    private int maxDepth = 9;

    public Connect4(Board b){
        this.b = b;
    }

    //CHECK IF THERE IS A WINNER
    public int gameResult(Board b){
        int aiScore = 0, pmcScore = 0;
        for(int i=5;i>=0;--i){
            for(int j=0;j<=6;++j){
                if(b.board[i][j]==0) continue;

                //Checking cells to the right
                if(j<=3){
                    for(int k=0;k<4;++k){
                        if(b.board[i][j+k]==1) aiScore++;
                        else if(b.board[i][j+k]==2) pmcScore++;
                        else break;
                    }
                    if(aiScore==4)return 1; else if (pmcScore==4)return 2;
                    aiScore = 0; pmcScore = 0;
                }

                //Checking cells up
                if(i>=3){
                    for(int k=0;k<4;++k){
                        if(b.board[i-k][j]==1) aiScore++;
                        else if(b.board[i-k][j]==2) pmcScore++;
                        else break;
                    }
                    if(aiScore==4)return 1; else if (pmcScore==4)return 2;
                    aiScore = 0; pmcScore = 0;
                }

                //Checking diagonal up-right
                if(j<=3 && i>= 3){
                    for(int k=0;k<4;++k){
                        if(b.board[i-k][j+k]==1) aiScore++;
                        else if(b.board[i-k][j+k]==2) pmcScore++;
                        else break;
                    }
                    if(aiScore==4)return 1; else if (pmcScore==4)return 2;
                    aiScore = 0; pmcScore = 0;
                }

                //Checking diagonal up-left
                if(j>=3 && i>=3){
                    for(int k=0;k<4;++k){
                        if(b.board[i-k][j-k]==1) aiScore++;
                        else if(b.board[i-k][j-k]==2) pmcScore++;
                        else break;
                    }
                    if(aiScore==4)return 1; else if (pmcScore==4)return 2;
                    aiScore = 0; pmcScore = 0;
                }
            }
        }

        for(int j=0;j<7;++j){
            //Game has not ended yet
            if(b.board[0][j]==0)return -1;
        }
        //Game draw!
        return 0;
    }

    int calculateScore(int aiScore, int moreMoves){
        int moveScore = 4 - moreMoves;
        if(aiScore==0)return 0;
        else if(aiScore==1)return 1*moveScore;
        else if(aiScore==2)return 10*moveScore;
        else if(aiScore==3)return 100*moveScore;
        else return 1000;
    }

    //Evaluate board favorableness for AI
    public int evaluateBoard(Board b){

        int aiScore=1;
        int score=0;
        int blanks = 0;
        int k=0, moreMoves=0;
        for(int i=5;i>=0;--i){
            for(int j=0;j<=6;++j){

                if(b.board[i][j]==0 || b.board[i][j]==2) continue;

                if(j<=3){
                    for(k=1;k<4;++k){
                        if(b.board[i][j+k]==1)aiScore++;
                        else if(b.board[i][j+k]==2){aiScore=0;blanks = 0;break;}
                        else blanks++;
                    }

                    moreMoves = 0;
                    if(blanks>0)
                        for(int c=1;c<4;++c){
                            int column = j+c;
                            for(int m=i; m<= 5;m++){
                                if(b.board[m][column]==0)moreMoves++;
                                else break;
                            }
                        }

                    if(moreMoves!=0) score += calculateScore(aiScore, moreMoves);
                    aiScore=1;
                    blanks = 0;
                }

                if(i>=3){
                    for(k=1;k<4;++k){
                        if(b.board[i-k][j]==1)aiScore++;
                        else if(b.board[i-k][j]==2){aiScore=0;break;}
                    }
                    moreMoves = 0;

                    if(aiScore>0){
                        int column = j;
                        for(int m=i-k+1; m<=i-1;m++){
                            if(b.board[m][column]==0)moreMoves++;
                            else break;
                        }
                    }
                    if(moreMoves!=0) score += calculateScore(aiScore, moreMoves);
                    aiScore=1;
                    blanks = 0;
                }

                if(j>=3){
                    for(k=1;k<4;++k){
                        if(b.board[i][j-k]==1)aiScore++;
                        else if(b.board[i][j-k]==2){aiScore=0; blanks=0;break;}
                        else blanks++;
                    }
                    moreMoves=0;
                    if(blanks>0)
                        for(int c=1;c<4;++c){
                            int column = j- c;
                            for(int m=i; m<= 5;m++){
                                if(b.board[m][column]==0)moreMoves++;
                                else break;
                            }
                        }

                    if(moreMoves!=0) score += calculateScore(aiScore, moreMoves);
                    aiScore=1;
                    blanks = 0;
                }

                if(j<=3 && i>=3){
                    for(k=1;k<4;++k){
                        if(b.board[i-k][j+k]==1)aiScore++;
                        else if(b.board[i-k][j+k]==2){aiScore=0;blanks=0;break;}
                        else blanks++;
                    }
                    moreMoves=0;
                    if(blanks>0){
                        for(int c=1;c<4;++c){
                            int column = j+c, row = i-c;
                            for(int m=row;m<=5;++m){
                                if(b.board[m][column]==0)moreMoves++;
                                else if(b.board[m][column]==1);
                                else break;
                            }
                        }
                        if(moreMoves!=0) score += calculateScore(aiScore, moreMoves);
                        aiScore=1;
                        blanks = 0;
                    }
                }

                if(i>=3 && j>=3){
                    for(k=1;k<4;++k){
                        if(b.board[i-k][j-k]==1)aiScore++;
                        else if(b.board[i-k][j-k]==2){aiScore=0;blanks=0;break;}
                        else blanks++;
                    }
                    moreMoves=0;
                    if(blanks>0){
                        for(int c=1;c<4;++c){
                            int column = j-c, row = i-c;
                            for(int m=row;m<=5;++m){
                                if(b.board[m][column]==0)moreMoves++;
                                else if(b.board[m][column]==1);
                                else break;
                            }
                        }
                        if(moreMoves!=0) score += calculateScore(aiScore, moreMoves);
                        aiScore=1;
                        blanks = 0;
                    }
                }
            }
        }
        return score;
    }

    public int minimax(int depth, int turn, int alpha, int beta){

        if(beta<=alpha){if(turn == 1) return Integer.MAX_VALUE; else return Integer.MIN_VALUE; }
        int gameResult = gameResult(b);

        if(gameResult==1)return Integer.MAX_VALUE/2;
        else if(gameResult==2)return Integer.MIN_VALUE/2;
        else if(gameResult==0)return 0;

        if(depth==maxDepth)return evaluateBoard(b);

        int maxScore=Integer.MIN_VALUE, minScore = Integer.MAX_VALUE;

        for(int j=0;j<=6;++j){

            int currentScore = 0;

            if(!b.isLegalMove(j)) continue;

            if(turn==1){
                b.placeMove(j, 1);
                currentScore = minimax(depth+1, 2, alpha, beta);

                if(depth==0){
                    System.out.println("Score for location "+j+" = "+currentScore);
                    if(currentScore > maxScore)nextMoveLocation = j;
                    if(currentScore == Integer.MAX_VALUE/2){b.undoMove(j);break;}
                }

                maxScore = Math.max(currentScore, maxScore);

                alpha = Math.max(currentScore, alpha);
            }
            else if(turn==2){
                b.placeMove(j, 2);
                currentScore = minimax(depth+1, 1, alpha, beta);
                minScore = Math.min(currentScore, minScore);

                beta = Math.min(currentScore, beta);
            }
            b.undoMove(j);
            if(currentScore == Integer.MAX_VALUE || currentScore == Integer.MIN_VALUE) break;
        }
        return turn==1?maxScore:minScore;
    }

    public int hMCTS(){
        nextMoveLocation = -1;
        minimax(0, 1, Integer.MIN_VALUE, Integer.MAX_VALUE);
        return nextMoveLocation;
    }

    public int firstTurn(){
        if(Math.random() < 0.5){
            return 0;
        }
        return 1;
    }

    public void pMCTS() {
        System.out.println("PURE MONTE CARLO TURN : Pick a spot -- ");
        int number = 1;
        int max_score = Integer.MIN_VALUE;
        long startTime = System.currentTimeMillis();
        for (int i = 0; i < 7; i++) {
            if(b.isLegalMove(i)){
                int score  = 0;
                for (int j = 1; j < 1000; j++) {
                    int random_play_result  = random_playout(i);
                    score += random_play_result;
                }
                if (score > max_score) {
                    max_score = score;
                    number = i;
                }

                System.out.println("Score for location " + i + " = " + "\t" + score );
            }
        }
        b.placeMove(number, (byte)2);
        long endTime = System.currentTimeMillis();
        long timeElapsed = endTime - startTime;
        System.out.println("Execution time in milliseconds: " + timeElapsed);
    }

    public int random_playout(int move) {
        Board copy = new Board();
        for(int i=0; i<b.board.length; i++)
            for(int j=0; j<b.board[i].length; j++)
                copy.board[i][j]=b.board[i][j];

        copy.placeMove(move, (byte)2);
        if (gameResult(copy) == 2){
            return 2;
        }

        while (!copy.legalMoves().isEmpty()) {
            if (copy.legalMoves().size() == 0) {
                return 1;
            }
            int move_index2 = new Random().nextInt(copy.legalMoves().size());
            int computer2_move = copy.legalMoves().get(move_index2);
            copy.placeMove(computer2_move, (byte)1);
            if (gameResult(copy) == 1){
                return -2;
            }
            if (copy.legalMoves().size() == 0) {
                return 1;
            }
            int move_index1 = new Random().nextInt(copy.legalMoves().size());
            int computer1_move = copy.legalMoves().get(move_index1);
            copy.placeMove(computer1_move, (byte)2);
            if (gameResult(copy) == 2) {
                return 2;
            }
        }
        return 1;
    }



    public void play_a_new_game(){

        System.out.println();
        System.out.println("|*************************************************|");
        System.out.println("|            WELCOME TO CONNECT-4                 |");
        System.out.println("|            PMCTS (2)    HMCTS (1)               |");
        System.out.println("|                                                 |");
        System.out.println("| The game will randomly choose one of the players|");
        System.out.println("| to go first in the game.                        |");
        System.out.println("|                                                 |");
        System.out.println("| RULES - Every player has to choose one spot     |");
        System.out.println("| out of the available spots/numbers when it is . |");
        System.out.println("| their turn.                                     |");
        System.out.println("|                                                 |");
        System.out.println("|*************************************************|");
        System.out.println();

        Scanner scanner = new Scanner(System.in);
        if(firstTurn() == 0) {
            System.out.print("PURE MONTE CARLO going first: Enter any key to continue");
            scanner.nextLine();
            pMCTS();
        }
        else  {
            System.out.print("HEURISTIC MONTE CARLO going first: Enter any key to continue");
            scanner.nextLine();
        }

        b.displayBoard();
        b.placeMove(3, 1);
        b.displayBoard();

        while(true){
            pMCTS();
            b.displayBoard();

            int gameResult = gameResult(b);
            if(gameResult==1){System.out.println("HEURISTIC MONTE CARLO TREE SEARCH WINS!");break;}
            else if(gameResult==2){System.out.println("PURE MONTE CARLO TREE SEARCH WINS!");break;}
            else if(gameResult==0){System.out.println("DRAW!");break;}

            b.placeMove(hMCTS(), 1);
            b.displayBoard();
            gameResult = gameResult(b);
            if(gameResult==1){System.out.println("HEURISTIC MONTE CARLO TREE SEARCH WINS!");break;}
            else if(gameResult==2){System.out.println("PURE MONTE CARLO TREE SEARCH WINS!");break;}
            else if(gameResult==0){System.out.println("DRAW!");break;}
        }

    }

    public static void main(String[] args) {
        Board b = new Board();
        Connect4 hmcts = new Connect4(b);
        hmcts.play_a_new_game();
    }
}

