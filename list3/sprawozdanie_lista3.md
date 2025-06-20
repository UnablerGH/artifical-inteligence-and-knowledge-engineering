# Sprawozdanie - Lista 3: Planowanie z wykorzystaniem języka PDDL

## 1. Wprowadzenie

Lista 3 dotyczyła implementacji trzech problemów planowania w języku PDDL (Planning Domain Definition Language). Zadanie obejmowało stworzenie generatora PDDL w Pythonie oraz modelowanie trzech różnych scenariuszy: transportu paczek, sprzątającego robota i robota przenoszącego piłki.

## 2. Analiza implementacji

### 2.1 Generator PDDL w Pythonie

Implementacja zawiera trzy główne klasy:

#### `PDDLDomain`
- Odpowiada za definicję domeny planowania
- Zawiera: requirements, types, predicates, actions
- Metoda `to_pddl()` generuje poprawną składnię PDDL

#### `PDDLAction` 
- Reprezentuje pojedynczą akcję w domenie
- Definiuje: parametry, warunki wstępne, efekty
- Integruje się z domeną jako lista akcji

#### `PDDLProblem`
- Opisuje konkretny problem planowania
- Zawiera: obiekty, stan początkowy, cel
- Łączy się z domeną przez nazwę

### 2.2 Jakość kodu

**Zalety:**
- Czytelna struktura obiektowa
- Modularne podejście do budowy PDDL
- Automatyczne generowanie składni
- Ponowne wykorzystanie komponentów

**Obszary do poprawy:**
- Brak walidacji składni PDDL
- Ograniczona obsługa błędów
- Brak wsparcia dla zaawansowanych konstrukcji PDDL

## 3. Analiza problemów

### 3.1 Problem 1: Transport paczek

**Opis:** Robot transportuje paczki między lokacjami

**Specyfikacja:**
- Domeny: robot, package, location
- Akcje: load, unload, move
- Requirements: :strips, :typing, :negative-preconditions, :numeric-fluents

**Błędy znalezione:**
- **KRYTYCZNY:** Brak deklaracji predykatu `(loaded ?p - package ?r - robot)`
- W akcji `unload` brak sprawdzenia lokacji robota
- Jednostronne połączenia między lokacjami

**Poprawki:**
- Dodano missing predykat `loaded`
- Poprawiono warunki w akcji `unload`
- Utworzono bidirectional connections w problemie

**Złożoność:**
- Obiekty: 6 (1 robot, 2 paczki, 3 lokacje)
- Szacowana przestrzeń stanów: ~162
- Minimalny plan: 7-8 kroków

### 3.2 Problem 2: Sprzątający robot

**Opis:** Robot porusza się po pokojach i je sprząta

**Specyfikacja:**
- Domeny: robot, room
- Akcje: move, clean
- Requirements: :strips, :typing

**Stan:** POPRAWNA IMPLEMENTACJA

**Charakterystyka:**
- Najprostszy z trzech problemów
- Robot może się "teleportować" między pokojami
- Brak ograniczeń topologicznych

**Złożoność:**
- Obiekty: 4 (1 robot, 3 pokoje)
- Szacowana przestrzeń stanów: ~24
- Minimalny plan: 5 kroków

**Możliwe ulepszenia:**
- Dodanie predykatu `connected` dla realizmu
- Ograniczenie ruchu do sąsiadujących pokojów

### 3.3 Problem 3: Robot z piłkami

**Opis:** Robot z dwoma ramionami przenosi piłki między pokojami

**Specyfikacja:**
- Domeny: robot, room, ball, arm
- Akcje: move, pick-up, put-down
- Requirements: :strips, :typing

**Stan:** POPRAWNA IMPLEMENTACJA

**Charakterystyka:**
- Najbardziej zaawansowany problem
- Robot może nieść 2 piłki jednocześnie
- Efektywne wykorzystanie wielu ramion

**Złożoność:**
- Obiekty: 9 (1 robot, 4 piłki, 2 pokoje, 2 ramiona)
- Szacowana przestrzeń stanów: ~512
- Minimalny plan: 7 kroków (z wykorzystaniem 2 ramion)

**Optymalna strategia:**
1. Podnieś 2 piłki jednocześnie
2. Przenieś do drugiego pokoju
3. Odłóż piłki
4. Wróć po pozostałe 2 piłki
5. Powtórz proces

## 4. Analiza techniczna PDDL

### 4.1 Wykorzystane rozszerzenia PDDL

| Problem | Requirements używane |
|---------|---------------------|
| Problem 1 | :strips, :typing, :negative-preconditions, :numeric-fluents |
| Problem 2 | :strips, :typing |
| Problem 3 | :strips, :typing |

### 4.2 Wzorce projektowe

**Typowe konstrukcje:**
- Predykaty pozycyjne: `(at ?obj ?location)`
- Predykaty stanowe: `(clean ?room)`, `(dirty ?room)`
- Predykaty relacyjne: `(connected ?from ?to)`
- Predykaty dzierżenia: `(holding ?arm ?ball)`

**Wzorce akcji:**
- Przemieszczanie: warunek lokacji + efekt zmiany lokacji
- Manipulacja obiektów: warunki obecności + efekty posiadania
- Zmiana stanu: warunki aktualnego stanu + efekty nowego stanu

### 7.1 Złożoność obliczeniowa

| Problem | Branching Factor | Głębokość | Złożoność |
|---------|------------------|-----------|-----------|
| Transport | ~6-8 | 7-8 | Średnia |
| Cleaning | ~4-6 | 5 | Niska |
| Ball Moving | ~8-12 | 7 | Wysoka |

### 7.2 Skalowalność

**Problem 1 (Transport):**
- Liniowa w liczbie paczek
- Kwadratowa w liczbie lokacji
- Praktyczne do ~10 paczek, 10 lokacji

**Problem 2 (Cleaning):**
- Liniowa w liczbie pokojów
- Bardzo skalowalna
- Praktyczne do dziesiątek pokojów

**Problem 3 (Ball Moving):**
- Eksponencjalna w liczbie piłek
- Ograniczona liczbą ramion
- Praktyczne do ~8-10 piłek z 2 ramionami

