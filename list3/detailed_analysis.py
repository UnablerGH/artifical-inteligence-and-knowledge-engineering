def analyze_domain_problems():
    """Szczegółowa analiza błędów w plikach PDDL"""
    
    print("=== SZCZEGÓŁOWA ANALIZA DOMEN I PROBLEMÓW ===\n")
    
    # Analiza Domain 1
    print("1. ANALIZA DOMAIN1.PDDL:")
    
    print("   Błędy znalezione:")
    print("   - BRAK deklaracji predykatu (loaded ?p - package ?r - robot)")
    print("   - W akcji 'load' używany jest predykat 'loaded', ale nie jest zdeklarowany")
    print("   - W akcji 'unload' warunek nie sprawdza gdzie jest robot")
    print("   - Brak sprawdzenia czy robot jest w tej samej lokacji co cel")
    
    print("\n   Poprawki:")
    print("   - Dodano predykat (loaded ?p - package ?r - robot)")
    print("   - Zmieniono warunek w 'unload' na (and (loaded ?p ?r) (at ?r ?l))")
    print("   - Dodano bidirectional connections w problem1.pddl")
    
    # Analiza Domain 2
    print("\n2. ANALIZA DOMAIN2.PDDL:")
    print("   Stan: POPRAWNA")
    print("   - Wszystkie predykaty są zdeklarowane")
    print("   - Akcje są logicznie spójne")
    print("   - Może poruszać się po wszystkich pokojach (brak ograniczeń)")
    
    print("\n   Potencjalne ulepszenia:")
    print("   - Można dodać predykat (connected ?from ?to - room) dla realizmu")
    print("   - Robot może się teleportować między pokojami")
    
    # Analiza Domain 3
    print("\n3. ANALIZA DOMAIN3.PDDL:")
    print("   Stan: POPRAWNA")
    print("   - Wszystkie predykaty zadeklarowane prawidłowo")
    print("   - Robot ma 2 ramiona - może nieść 2 piłki jednocześnie")
    print("   - Logika pick-up/put-down jest spójna")
    
    print("\n   Obserwacje:")
    print("   - Robot może się teleportować między pokojami")
    print("   - Minimalna liczba kroków: 6 (pick-up x4, move x1, put-down x4)")
    print("   - Maksymalna efektywność: 2 piłki na raz")
    
    print("\n=== ANALIZA PROBLEMÓW ===")
    
    # Problem 1
    print("\n1. PROBLEM1.PDDL:")
    print("   Zadanie: pkg1 (loc1→loc3), pkg2 (loc2→loc1)")
    print("   Stan początkowy: rob1 w loc1, pkg1 w loc1, pkg2 w loc2")
    print("   Minimalny plan: 8 kroków")
    print("   1. load pkg1 loc1")
    print("   2. move loc1→loc2") 
    print("   3. unload pkg1 loc2, load pkg2 loc2")
    print("   4. move loc2→loc3")
    print("   5. unload pkg1 loc3")
    print("   6. move loc3→loc1")
    print("   7. unload pkg2 loc1")
    
    # Problem 2
    print("\n2. PROBLEM2.PDDL:")
    print("   Zadanie: wyczyścić 3 pokoje")
    print("   Minimalny plan: 6 kroków")
    print("   1. clean pokoj1")
    print("   2. move pokoj1→pokoj2")
    print("   3. clean pokoj2") 
    print("   4. move pokoj2→pokoj3")
    print("   5. clean pokoj3")
    
    # Problem 3
    print("\n3. PROBLEM3.PDDL:")
    print("   Zadanie: przenieść 4 piłki z room1 do room2")
    print("   Minimalny plan: 7 kroków (z 2 ramionami)")
    print("   1. pick-up ball1 arm1, pick-up ball2 arm2")
    print("   2. move room1→room2") 
    print("   3. put-down ball1 arm1, put-down ball2 arm2")
    print("   4. move room2→room1")
    print("   5. pick-up ball3 arm1, pick-up ball4 arm2")
    print("   6. move room1→room2")
    print("   7. put-down ball3 arm1, put-down ball4 arm2")

def test_online_solver():
    """Test rozwiązywania problemów online"""
    print("\n=== TEST ONLINE SOLVER ===\n")
    
    import requests
    import json
    
    # Test prostego problemu
    simple_domain = """(define (domain simple-test)
  (:requirements :strips :typing)
  (:types location)
  (:predicates (at ?l - location) (goal))
  (:action achieve-goal
    :parameters ()
    :precondition (at loc1)
    :effect (goal))
)"""
    
    simple_problem = """(define (problem test1)
  (:domain simple-test)
  (:objects loc1 - location)
  (:init (at loc1))
  (:goal (goal))
)"""
    
    try:
        data = {
            'domain': simple_domain,
            'problem': simple_problem
        }
        
        print("Wysyłanie zapytania do solver.planning.domains...")
        response = requests.post(
            'http://solver.planning.domains/solve',
            json=data,
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"Status: {result.get('status', 'unknown')}")
            
            if result.get('status') == 'ok':
                plan = result.get('result', {}).get('plan', [])
                print(f"Plan znaleziony: {len(plan)} kroków")
                for i, action in enumerate(plan, 1):
                    print(f"  {i}. {action.get('name', action)}")
            else:
                print(f"Błąd planowania: {result.get('result', 'unknown error')}")
                
        else:
            print(f"Błąd HTTP: {response.status_code}")
            
    except Exception as e:
        print(f"Błąd połączenia: {e}")
        print("Solver niedostępny - prawdopodobnie ograniczenia sieciowe")

def evaluate_pddl_complexity():
    """Ocena złożoności problemów PDDL"""
    print("\n=== OCENA ZŁOŻONOŚCI PROBLEMÓW ===\n")
    
    problems = [
        {
            'name': 'Problem 1 - Transport',
            'objects': {'robot': 1, 'package': 2, 'location': 3},
            'actions': 3,
            'predicates': 4,
            'estimated_states': 3 * 3 * 3 * 2,  # robot_pos * pkg1_pos * pkg2_pos * loaded_state
            'complexity': 'Średnia'
        },
        {
            'name': 'Problem 2 - Cleaning',
            'objects': {'robot': 1, 'room': 3},
            'actions': 2,
            'predicates': 3,
            'estimated_states': 3 * (2**3),  # robot_pos * clean_states
            'complexity': 'Niska'
        },
        {
            'name': 'Problem 3 - Ball Moving',
            'objects': {'robot': 1, 'ball': 4, 'room': 2, 'arm': 2},
            'actions': 3,
            'predicates': 4,
            'estimated_states': 2 * (2**4) * (4**2),  # robot_pos * ball_positions * arm_states  
            'complexity': 'Wysoka'
        }
    ]
    
    for prob in problems:
        print(f"{prob['name']}:")
        print(f"  Obiekty: {sum(prob['objects'].values())}")
        print(f"  Akcje: {prob['actions']}")
        print(f"  Predykaty: {prob['predicates']}")
        print(f"  Szacowana przestrzeń stanów: ~{prob['estimated_states']}")
        print(f"  Złożoność: {prob['complexity']}")
        print()

if __name__ == "__main__":
    analyze_domain_problems()
    test_online_solver()
    evaluate_pddl_complexity()
    print("=== ANALIZA ZAKOŃCZONA ===") 