% Tic-Tac-Toe with AI opponent
% Board representation: [1,2,3,4,5,6,7,8,9]
% X - human player, O - AI

% Main predicate to start game
play :-
    write('Tic-Tac-Toe - You are X, AI is O'), nl,
    display_board([1,2,3,4,5,6,7,8,9]),
    play_game([1,2,3,4,5,6,7,8,9], x).

% Game loop
play_game(Board, Player) :-
    (win(Board, x) -> write('You win!'), nl, !;
    win(Board, o) -> write('AI wins!'), nl, !;
    board_full(Board) -> write('Tie game!'), nl, !;
    Player = x -> player_move(Board, NewBoard),
        display_board(NewBoard),
        play_game(NewBoard, o);
    ai_move(Board, NewBoard),
        write('AI moves:'), nl,
        display_board(NewBoard),
        play_game(NewBoard, x)
    ).

% Human player move
player_move(Board, NewBoard) :-
    repeat,
    write('Enter position (1-9): '),
    read(Pos),
    integer(Pos),
    between(1, 9, Pos),
    nth1(Pos, Board, Cell),
    integer(Cell),  % Check if position is empty
    replace(Board, Pos, x, NewBoard), !.

% AI move selection (prioritizes winning, then blocking, then center/corners)
ai_move(Board, NewBoard) :-
    (select_winning_move(Board, NewBoard) -> true
    ; select_blocking_move(Board, NewBoard) -> true
    ; select_best_move(Board, NewBoard) -> true
    ).

% Check for winning move
select_winning_move(Board, NewBoard) :-
    between(1, 9, Pos),
    nth1(Pos, Board, Cell),
    integer(Cell),
    replace(Board, Pos, o, TempBoard),
    win(TempBoard, o),
    NewBoard = TempBoard.

% Block human winning move
select_blocking_move(Board, NewBoard) :-
    between(1, 9, Pos),
    nth1(Pos, Board, Cell),
    integer(Cell),
    replace(Board, Pos, x, TempBoard),
    win(TempBoard, x),
    replace(Board, Pos, o, NewBoard).

% Select best available move (center, corners, then others)
select_best_move(Board, NewBoard) :-
    member(Pos, [5,1,3,7,9,2,4,6,8]),
    nth1(Pos, Board, Cell),
    integer(Cell),
    replace(Board, Pos, o, NewBoard).

% Win conditions
win(Board, Player) :-
    row_win(Board, Player)
    ; col_win(Board, Player)
    ; diag_win(Board, Player).

row_win(Board, P) :- Board = [P,P,P,_,_,_,_,_,_].
row_win(Board, P) :- Board = [_,_,_,P,P,P,_,_,_].
row_win(Board, P) :- Board = [_,_,_,_,_,_,P,P,P].
col_win(Board, P) :- Board = [P,_,_,P,_,_,P,_,_].
col_win(Board, P) :- Board = [_,P,_,_,P,_,_,P,_].
col_win(Board, P) :- Board = [_,_,P,_,_,P,_,_,P].
diag_win(Board, P) :- Board = [P,_,_,_,P,_,_,_,P].
diag_win(Board, P) :- Board = [_,_,P,_,P,_,P,_,_].


% Board utilities
replace([_|T], 1, X, [X|T]).
replace([H|T], N, X, [H|R]) :- N > 1, N1 is N-1, replace(T, N1, X, R).
board_full(Board) :- \+ (member(Cell, Board), integer(Cell)).

% Display the current board state
display_board([A,B,C,D,E,F,G,H,I]) :-
    nl,
    write(' '), write(A), write(' | '), write(B), write(' | '), write(C), nl,
    write('-----------'), nl,
    write(' '), write(D), write(' | '), write(E), write(' | '), write(F), nl,
    write('-----------'), nl,
    write(' '), write(G), write(' | '), write(H), write(' | '), write(I), nl, nl.

% ?- play.