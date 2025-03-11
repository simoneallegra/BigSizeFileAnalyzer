
from pathlib import Path
from faker import Faker

script_path = Path(__file__).parent

def main() -> None:
    
    fake = Faker()     

    word_count = int(input("Inserisci il numero di parole casuali da generare: "))
    random_words = [fake.word() for _ in range(word_count)]

    with open(script_path / 'test.txt', 'w') as file:
            file.write(" ".join(random_words))

    print(f"Parole casuali salvate su 'test.txt'")

if __name__ == "__main__":
    main()