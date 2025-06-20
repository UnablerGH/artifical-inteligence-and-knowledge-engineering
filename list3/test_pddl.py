class PDDLDomain:
    def __init__(self, name, requirements=None, types=None, predicates=None, actions=None):
        self.name = name
        self.requirements = requirements or []
        self.types = types or []
        self.predicates = predicates or []  # list of strings
        self.actions = actions or []        # list of PDDLAction

    def to_pddl(self):
        parts = [f"(define (domain {self.name})"]
        if self.requirements:
            reqs = ' '.join(self.requirements)
            parts.append(f"  (:requirements {reqs})")
        if self.types:
            types_str = ' '.join(self.types)
            parts.append(f"  (:types {types_str})")
        if self.predicates:
            parts.append("  (:predicates")
            for pred in self.predicates:
                parts.append(f"    {pred}")
            parts.append("  )")
        for action in self.actions:
            parts.append(action.to_pddl())
        parts.append(")")
        return '\n'.join(parts)

class PDDLAction:
    def __init__(self, name, parameters, precondition, effect):
        self.name = name
        self.parameters = parameters  # list of strings like '?r - robot'
        self.precondition = precondition  # string
        self.effect = effect              # string

    def to_pddl(self):
        params = ' '.join(self.parameters)
        return (f"  (:action {self.name}\n"
                f"    :parameters ({params})\n"
                f"    :precondition {self.precondition}\n"
                f"    :effect {self.effect}\n"
                f"  )")

class PDDLProblem:
    def __init__(self, name, domain, objects=None, init=None, goal=None):
        self.name = name
        self.domain = domain
        self.objects = objects or {}  # dict type->list of names
        self.init = init or []        # list of strings
        self.goal = goal              # string

    def to_pddl(self):
        parts = [f"(define (problem {self.name})",
                 f"  (:domain {self.domain})"]
        if self.objects:
            parts.append("  (:objects")
            for t, objs in self.objects.items():
                line = ' '.join(objs) + ' - ' + t
                parts.append(f"    {line}")
            parts.append("  )")
        if self.init:
            parts.append("  (:init")
            for fact in self.init:
                parts.append(f"    {fact}")
            parts.append("  )")
        if self.goal:
            parts.append(f"  (:goal {self.goal})")
        parts.append(")")
        return '\n'.join(parts)

def analyze_pddl_files():
    """Analizuje wygenerowane pliki PDDL"""
    
    print("=== ANALIZA PLIKÓW PDDL ===\n")
    
    # Sprawdzenie istnienia plików
    import os
    files = ['domain1.pddl', 'problem1.pddl', 'domain2.pddl', 'problem2.pddl', 'domain3.pddl', 'problem3.pddl']
    
    print("1. Sprawdzenie istnienia plików:")
    for file in files:
        exists = os.path.exists(file)
        print(f"   {file}: {'✓' if exists else '✗'}")
    
    print("\n2. Sprawdzenie składni PDDL:")
    
    # Prosta walidacja składni
    def validate_pddl_file(filename):
        try:
            with open(filename, 'r') as f:
                content = f.read()
            
            # Sprawdzenie podstawowej struktury
            if content.strip().startswith('(define'):
                if content.count('(') == content.count(')'):
                    return "✓ Poprawna składnia"
                else:
                    return "✗ Nieprawidłowe nawiasy"
            else:
                return "✗ Brak define"
        except Exception as e:
            return f"✗ Błąd: {e}"
    
    for file in files:
        if os.path.exists(file):
            result = validate_pddl_file(file)
            print(f"   {file}: {result}")
    
    print("\n3. Analiza złożoności problemów:")
    
    # Analiza każdego problemu
    problems_analysis = [
        ("Problem 1 - Transport paczek", "2 paczki, 3 lokacje, 1 robot"),
        ("Problem 2 - Sprzątający robot", "3 pokoje, 1 robot"),
        ("Problem 3 - Robot z piłkami", "4 piłki, 2 pokoje, 1 robot, 2 ramiona")
    ]
    
    for name, desc in problems_analysis:
        print(f"   {name}: {desc}")
    
    print("\n4. Ocena kompletności:")
    
    requirements_check = [
        ("Domain 1", [":strips", ":typing", ":negative-preconditions", ":numeric-fluents"]),
        ("Domain 2", [":strips", ":typing"]),
        ("Domain 3", [":strips", ":typing"])
    ]
    
    for domain_name, reqs in requirements_check:
        print(f"   {domain_name}: {', '.join(reqs)}")

def test_regeneration():
    """Test regeneracji plików PDDL"""
    
    print("\n=== TEST REGENERACJI PLIKÓW ===\n")
    
    # Zadanie 1 - Transport paczek
    domain1 = PDDLDomain(
        name='transport-paczek',
        requirements=[':strips', ':typing', ':negative-preconditions', ':numeric-fluents'],
        types=['robot', 'package', 'location'],
        predicates=[
            '(at ?r - robot ?l - location)',
            '(at-packet ?p - package ?l - location)',
            '(connected ?from ?to - location)',
            '(loaded ?p - package ?r - robot)'  # Dodane missing predicate
        ],
        actions=[
            PDDLAction(
                name='load',
                parameters=['?r - robot', '?p - package', '?l - location'],
                precondition='(and (at ?r ?l) (at-packet ?p ?l))',
                effect='(and (not (at-packet ?p ?l)) (loaded ?p ?r))'
            ),
            PDDLAction(
                name='unload',
                parameters=['?r - robot', '?p - package', '?l - location'],
                precondition='(and (loaded ?p ?r) (at ?r ?l))',  # Poprawione
                effect='(and (at-packet ?p ?l) (not (loaded ?p ?r)))'
            ),
            PDDLAction(
                name='move',
                parameters=['?r - robot', '?from - location', '?to - location'],
                precondition='(and (at ?r ?from) (connected ?from ?to))',
                effect='(and (not (at ?r ?from)) (at ?r ?to))'
            )
        ]
    )
    
    print("Regeneracja domain1.pddl z poprawkami...")
    with open('domain1_fixed.pddl', 'w') as f:
        f.write(domain1.to_pddl())
    
    # Problem 1 - dodanie połączeń bidirectional
    problem1 = PDDLProblem(
        name='transport1',
        domain='transport-paczek',
        objects={
            'location': ['loc1', 'loc2', 'loc3'],
            'robot': ['rob1'],
            'package': ['pkg1', 'pkg2']
        },
        init=[
            '(at rob1 loc1)',
            '(at-packet pkg1 loc1)',
            '(at-packet pkg2 loc2)',
            '(connected loc1 loc2)',
            '(connected loc2 loc1)',  # Bidirectional
            '(connected loc2 loc3)',
            '(connected loc3 loc2)',  # Bidirectional
            '(connected loc3 loc1)',
            '(connected loc1 loc3)'   # Bidirectional
        ],
        goal='(and (at-packet pkg1 loc3) (at-packet pkg2 loc1))'
    )
    
    print("Regeneracja problem1.pddl z poprawkami...")
    with open('problem1_fixed.pddl', 'w') as f:
        f.write(problem1.to_pddl())
    
    print("✓ Pliki zostały zregenerowane z poprawkami")

if __name__ == "__main__":
    analyze_pddl_files()
    test_regeneration()
    print("\n=== ANALIZA ZAKOŃCZONA ===") 