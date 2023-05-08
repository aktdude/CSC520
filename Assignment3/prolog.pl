% Creature has two types, bird and human
creature(X):-human(X);bird(X).


% Human has a type man
human(X):-man(X).

% A bird that isn't a turkey can fly
fly(X):-bird(X), not(turkey(X)).
% A human who isn't afraid can fly
fly(X):-human(X), not(afraid(X)).

% A bird has two types, turkey and eagle
bird(X):-turkey(X);eagle(X).




% What we know
man(albert).
man(louis).
afraid(louis).
turkey(frank).
eagle(bob).
