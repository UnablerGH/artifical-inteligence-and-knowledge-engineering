## 2. Wyniki eksperymentów

### 2.1 Efektywność Alpha-Beta vs Minimax

#### Głębokość 2:
- Redukcja węzłów: 85.5% - 93.4%
- Przyspieszenie: 4.8x - 17.1x

#### Głębokość 3:
- Redukcja węzłów: 97.3% - 97.5%
- Przyspieszenie: 31.8x - 41.6x

#### Głębokość 4:
- Redukcja węzłów: 99.1% - 99.8%
- Przyspieszenie: 91.2x - 569.7x

### 2.2 Obserwacje dotyczące efektywności
- Efektywność alpha-beta rośnie wykładniczo z głębokością przeszukiwania
- Przy głębokości 4 alpha-beta odwiedza prawie 1000 razy mniej węzłów niż minimax
- Przyspieszenie czasowe jest często większe niż redukcja węzłów ze względu na oszczędności w alokacji pamięci

## 3. Analiza heurystyk

### 3.1 Heurystyka różnicy pionków
- Najprostsza w implementacji
- Skuteczna w sytuacjach z wyraźną przewagą materialną
- Może prowadzić do defensywnej gry

### 3.2 Heurystyka mobilności
- Uwzględnia liczbę dostępnych ruchów
- Wydaje się najsilniejsza w testach praktycznych
- Promuje aktywną grę i kontrolę centrum

### 3.3 Heurystyka pozycyjna
- Preferuje kontrolę krawędzi planszy
- Uwzględnia strategiczne aspekty pozycji
- Może być rozwinięta o dodatkowe czynniki pozycyjne

### 3.4 Wyniki porównania heurystyk
W testach bezpośrednich:
- Heurystyka mobilności wykazała przewagę nad pozostałymi
- Gracz W (White) częściej wygrywał, co może wskazywać na przewagę drugiego gracza
- Różnice między heurystykami są znaczące w praktycznej grze

## 4. Charakterystyka gry Clobber

### 4.1 Złożoność obliczeniowa
- Średni branching factor: 40-57 ruchów
- Średnia długość gry: 46-72 ruchy
- Wysoka złożoność drzewa gry (10^74 dla planszy 8x8)

### 4.2 Właściwości strategiczne
- Gra często rozpada się na niezależne podgry (subgames)
- Brak możliwości remisu - zawsze jest zwycięzca
- Taktyczny charakter z elementami strategicznymi

## 5. Wnioski techniczne
- Cięcia alfa-beta są niezwykle skuteczne w grach typu Clobber
- Porządek przeszukiwania ruchów ma duży wpływ na efektywność
- Implementacja jest skalowalna dla większych głębokości

## 6. Wnioski praktyczne
- Alpha-beta pruning jest niezbędne dla gier o wysokiej złożokości
- Dobra heurystyka może znacząco poprawić siłę gry
- Pomiar wydajności jest kluczowy dla optymalizacji
