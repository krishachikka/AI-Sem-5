% Implement	forward	chaining	reasoning	for	Medical Diagnosis System Using Prolog.
% Declare dynamic facts so we can assert symptoms
:- dynamic has_symptom/1.

% Define symptoms for different diseases
symptom(covid19, fever).
symptom(covid19, cough).
symptom(covid19, fatigue).
symptom(covid19, breathlessness).
symptom(covid19, sore_throat).
symptom(covid19, loss_of_smell).
symptom(covid19, loss_of_taste).
symptom(covid19, headache).
symptom(covid19, body_aches).

symptom(flu, sore_throat).
symptom(flu, fever).
symptom(flu, cough).
symptom(flu, fatigue).
symptom(flu, headache).
symptom(flu, body_aches).

symptom(cold, sneezing).
symptom(cold, cough).
symptom(cold, sore_throat).
symptom(cold, runny_nose).

symptom(malaria, sweating).
symptom(malaria, fever).
symptom(malaria, headache).
symptom(malaria, body_aches).
symptom(malaria, chills).

% Keep track of symptoms that have been asked
:- dynamic asked_symptom/1.

% Questions to ask the user
ask_symptom(Symptom) :-
    % Only ask if the symptom has not been asked yet
    \+ asked_symptom(Symptom),
    format('Do you have ~w? (yes/no): ', [Symptom]),
    read(Response),
    (Response == yes -> 
        assert(has_symptom(Symptom));
     Response == no -> true;
     write('Please answer with "yes" or "no".\n'), ask_symptom(Symptom)),
    assert(asked_symptom(Symptom)).

% Ask all relevant symptoms for a specific disease
ask_disease_symptoms(Disease) :-
    symptom(Disease, Symptom),
    ask_symptom(Symptom),
    fail.  % Continue asking for all symptoms of the disease

ask_disease_symptoms(_).  % Stop when no more symptoms to ask

% Diagnosis based on symptoms
diagnosis(Diseases) :-
    findall(Symptom, has_symptom(Symptom), Symptoms),
    diagnose(Symptoms, Diseases).

% Analyze the symptoms and provide a diagnosis for a specific disease
diagnose(Symptoms, [Disease | _]) :-
    disease_symptoms(Disease, DiseaseSymptoms),
    subset(DiseaseSymptoms, Symptoms),
    format('You might have ~w. Please consult a healthcare provider for further testing.\n', [Disease]), !.

diagnose(Symptoms, [_ | Rest]) :-
    diagnose(Symptoms, Rest).

% Get the symptoms for a disease
disease_symptoms(Disease, Symptoms) :-
    findall(Symptom, symptom(Disease, Symptom), Symptoms).

% Start the diagnosis process
start_diagnosis :-
    write('Welcome to the disease self-diagnosis system.\n'),
    ask_all_symptoms,
    diagnosis([covid19, flu, cold, malaria]).

% Ask all symptoms
ask_all_symptoms :-
    ask_disease_symptoms(covid19),
    ask_disease_symptoms(flu),
    ask_disease_symptoms(cold),
    ask_disease_symptoms(malaria).