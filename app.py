import string
from genetic_algorithms.build_quote.population import Population

if __name__ == "__main__":
    quote = "testing"
    new_population = Population(10, quote)
    traits = {i: string.ascii_lowercase for i in range(len(quote))}
    new_population.create_new_population(traits)

    for _ in range(1000):
        new_population.natural_selection()
        new_population.next_generation(0.10)
    print(new_population.get_most_fit_dna())
