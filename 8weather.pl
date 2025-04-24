% Implement Bayesian reasoning for probabilistic inference for Weather prediction.
% Prior probabilities for weather conditions
prior(sunny, 0.5).
prior(rainy, 0.3).
prior(cloudy, 0.2).

% Conditional probabilities of evidence given weather condition
probability(cloudy_given_sunny, 0.2).
probability(cloudy_given_rainy, 0.7).
probability(cloudy_given_cloudy, 0.9).
probability(humidity_given_sunny, 0.3).
probability(humidity_given_rainy, 0.8).
probability(humidity_given_cloudy, 0.6).

% Bayesian inference for weather prediction
bayes(Weather, Evidence, Posterior) :-
prior(Weather, Prior),
probability(Evidence, GivenProb),
Posterior is Prior * GivenProb.

% Sample Queries 1
% ?- bayes(sunny, cloudy_given_sunny, P).
% Expected Output: P = 0.1.

% Sample Queries 2
% ?- bayes(rainy, humidity_given_rainy, P).
% Expected Output: P = 0.24.