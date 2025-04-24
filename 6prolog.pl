% Implement a knowledge base for a medical diagnosis system using Prolog.
% Facts: Symptoms and their relationship to COVID-19
symptom(fever).
symptom(cough).
symptom(fatigue).
symptom(shortness_of_breath).
symptom(sore_throat).
symptom(headache).
symptom(migraine).

% Rules: If a person has certain symptoms, they might have COVID-19
has_covid(Person) :-
    has_symptom(Person, fever),
    has_symptom(Person, cough),
    has_symptom(Person, shortness_of_breath).

has_covid(Person) :-
    has_symptom(Person, fever),
    has_symptom(Person, cough),
    has_symptom(Person, fatigue).

has_covid(Person) :-
    has_symptom(Person, fever),
    has_symptom(Person, sore_throat),
    has_symptom(Person, headache).

% Facts: Example symptoms of people
has_symptom(krisha, fever).
has_symptom(krisha, shortness_of_breath).
has_symptom(krisha, cough).

has_symptom(vaidehi, fever).
has_symptom(vaidehi, sore_throat).
has_symptom(vaidehi, fatigue).