adiciona(X, L1, [X|L1]).

apaga(X, [X|T], T).
apaga(X, [H|T], [H|R]) :- remover(X, T, R).

concatena([], L, L).
concatena([H|T], L, [H|R]) :-
    concat(T, L, R).

membro(X, [X|T]).
membro(X, [H|T]) :- membro(X, T).

comprimento(0, []).
comprimento(X, [_|T]) :- 
  comprimento(X2, T),
  X is X2 + 1.
