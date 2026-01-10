aresta(1, 2).
aresta(2, 1).
aresta(2, 3).
aresta(3, 2).

adjacente(A, B) :- aresta(A, B), aresta(B, A).

caminho(A, B) :- caminho(A, B, [A]).
caminho(A, B, _) :- adjacente(A, B).

caminho(A, B, Visitados) :-
    adjacente(A, C),
    C \= B,
    \+ member(C, Visitados),
    caminho(C, B, [C|Visitados]).

grau(V, G) :-
  findall(U, adjacente(V, U), Lista),
  sort(Lista, SemDuplicatas),
  length(SemDuplicatas, G).

