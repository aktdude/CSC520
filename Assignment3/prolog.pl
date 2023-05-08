% Creature has two types, bird and human
creature(X):-human(X).
creature(X):-bird(X).
not(bird(X)):-human(X).
not(human(X)):-bird(X).

% Human has a type man
human(X):-man(X).

% A human who isn't afraid can fly
fly(X):-human(X), not(afraid(X)).

% A bird has two types, turkey and eagle
bird(X):-turkey(X).
bird(X):-eagle(X).
not(eagle(X)):-turkey(X).
not(turkey(X)):-eagle(X).

% A bird that isn't a turkey can fly
fly(X):-bird(X), not(turkey(X)).

% What we know
man(louis).
afraid(louis).
man(albert).
not(afraid(albert)).
turkey(frank).
eagle(bob).
