import time
import copy
from typing import List, Tuple, Optional

# Globalny licznik odwiedzonych węzłów
node_counter = 0

class ClobberState:
    def __init__(self, board: List[List[str]], current_player: str = 'B'):
        self.board = board
        self.current_player = current_player  # 'B' lub 'W'
        self.n = len(board[0])
        self.m = len(board)

    def get_opponent(self) -> str:
        return 'W' if self.current_player == 'B' else 'B'

    def in_bounds(self, r: int, c: int) -> bool:
        return 0 <= r < self.m and 0 <= c < self.n

    def generate_moves(self) -> List[Tuple[int,int,int,int]]:
        moves = []
        dirs = [(-1,0),(1,0),(0,-1),(0,1)]
        for r in range(self.m):
            for c in range(self.n):
                if self.board[r][c] == self.current_player:
                    for dr,dc in dirs:
                        nr, nc = r+dr, c+dc
                        if self.in_bounds(nr,nc) and self.board[nr][nc] == self.get_opponent():
                            moves.append((r,c,nr,nc))
        return moves

    def apply_move(self, move: Tuple[int,int,int,int]) -> 'ClobberState':
        r,c,nr,nc = move
        new_board = copy.deepcopy(self.board)
        new_board[nr][nc] = self.current_player
        new_board[r][c] = '_'
        return ClobberState(new_board, current_player=self.get_opponent())

    def is_terminal(self) -> bool:
        return len(self.generate_moves()) == 0

    def __str__(self):
        return '\n'.join(' '.join(row) for row in self.board)

def heuristic_piece_diff(state: ClobberState) -> int:
    b = sum(row.count('B') for row in state.board)
    w = sum(row.count('W') for row in state.board)
    return b - w if state.current_player=='B' else w - b

def heuristic_mobility(state: ClobberState) -> int:
    own_moves = len(state.generate_moves())
    opp_state = ClobberState(state.board, state.get_opponent())
    opp_moves = len(opp_state.generate_moves())
    return own_moves - opp_moves

def heuristic_positional(state: ClobberState) -> int:
    weight = 0
    m,n = state.m, state.n
    for r in range(m):
        for c in range(n):
            if state.board[r][c] == state.current_player:
                if r in [0,m-1] or c in [0,n-1]:
                    weight += 2
                else:
                    weight += 1
            elif state.board[r][c] == state.get_opponent():
                if r in [0,m-1] or c in [0,n-1]:
                    weight -= 2
                else:
                    weight -= 1
    return weight

def evaluate(state: ClobberState, heuristic) -> float:
    return heuristic(state)

def minimax_clobber(state: ClobberState, depth: int, heuristic):
    global node_counter
    node_counter = 0
    start = time.time()

    def recurse(s: ClobberState, d: int, maximizing: bool) -> float:
        global node_counter
        node_counter += 1
        if d == 0 or s.is_terminal():
            return evaluate(s, heuristic)
        moves = s.generate_moves()
        if not moves:
            return evaluate(s, heuristic)
        if maximizing:
            best_val = float('-inf')
            for mv in moves:
                val = recurse(s.apply_move(mv), d-1, False)
                best_val = max(best_val, val)
            return best_val
        else:
            best_val = float('inf')
            for mv in moves:
                val = recurse(s.apply_move(mv), d-1, True)
                best_val = min(best_val, val)
            return best_val

    best_move = None
    best_value = float('-inf')
    for mv in state.generate_moves():
        val = recurse(state.apply_move(mv), depth-1, False)
        if val > best_value:
            best_value = val
            best_move = mv
    end = time.time()
    return best_move, best_value, node_counter, end-start

def alphabeta_clobber(state: ClobberState, depth: int, heuristic):
    global node_counter
    node_counter = 0
    start = time.time()

    def recurse(s: ClobberState, d: int, alpha: float, beta: float, maximizing: bool) -> float:
        global node_counter
        node_counter += 1
        if d == 0 or s.is_terminal():
            return evaluate(s, heuristic)
        moves = s.generate_moves()
        if not moves:
            return evaluate(s, heuristic)
        if maximizing:
            value = float('-inf')
            for mv in moves:
                value = max(value, recurse(s.apply_move(mv), d-1, alpha, beta, False))
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
            return value
        else:
            value = float('inf')
            for mv in moves:
                value = min(value, recurse(s.apply_move(mv), d-1, alpha, beta, True))
                beta = min(beta, value)
                if beta <= alpha:
                    break
            return value

    best_move = None
    best_value = float('-inf')
    alpha, beta = float('-inf'), float('inf')
    for mv in state.generate_moves():
        val = recurse(state.apply_move(mv), depth-1, alpha, beta, False)
        if val > best_value:
            best_value = val
            best_move = mv
        alpha = max(alpha, best_value)
    end = time.time()
    return best_move, best_value, node_counter, end-start

def default_board(m=5, n=6) -> List[List[str]]:
    board = []
    for r in range(m):
        row = []
        for c in range(n):
            if (r + c) % 2 == 0:
                row.append('B')
            else:
                row.append('W')
        board.append(row)
    return board

def compare_algorithms():
    print("=== PORÓWNANIE ALGORYTMÓW MINIMAX vs ALPHA-BETA ===")
    state = ClobberState(default_board())
    
    depths = [2, 3, 4]
    heuristics = [
        ("Różnica pionków", heuristic_piece_diff),
        ("Mobilność", heuristic_mobility),
        ("Pozycyjna", heuristic_positional)
    ]
    
    for depth in depths:
        print(f"\n--- GŁĘBOKOŚĆ {depth} ---")
        for heur_name, heur_func in heuristics:
            print(f"\nHeurystyka: {heur_name}")
            
            # Minimax
            move_mm, val_mm, nodes_mm, time_mm = minimax_clobber(state, depth, heur_func)
            print(f"Minimax:    ruch={move_mm}, wartość={val_mm}, węzły={nodes_mm}, czas={time_mm:.4f}s")
            
            # Alpha-Beta
            move_ab, val_ab, nodes_ab, time_ab = alphabeta_clobber(state, depth, heur_func)
            print(f"Alpha-Beta: ruch={move_ab}, wartość={val_ab}, węzły={nodes_ab}, czas={time_ab:.4f}s")
            
            # Porównanie efektywności
            if nodes_mm > 0:
                reduction = (1 - nodes_ab/nodes_mm) * 100
                speedup = time_mm / time_ab if time_ab > 0 else float('inf')
                print(f"Redukcja węzłów: {reduction:.1f}%, Przyspieszenie: {speedup:.1f}x")

def test_heuristics_battle():
    print("\n=== PORÓWNANIE HEURYSTYK W GRZE ===")
    
    heuristics = [
        ("Różnica pionków", heuristic_piece_diff),
        ("Mobilność", heuristic_mobility),
        ("Pozycyjna", heuristic_positional)
    ]
    
    for i, (name1, heur1) in enumerate(heuristics):
        for j, (name2, heur2) in enumerate(heuristics):
            if i < j:  # Unikamy duplikatów
                print(f"\n{name1} (B) vs {name2} (W)")
                winner = play_game_between_heuristics(heur1, heur2, depth=3)
                print(f"Zwycięzca: {winner}")

def play_game_between_heuristics(heur1, heur2, depth=3):
    s = ClobberState(default_board())
    rounds = 0
    
    while not s.is_terminal() and rounds < 50:  # Limit rund
        if s.current_player == 'B':
            mv, _, _, _ = alphabeta_clobber(s, depth, heur1)
        else:
            mv, _, _, _ = alphabeta_clobber(s, depth, heur2)
        
        if mv is None:
            break
        s = s.apply_move(mv)
        rounds += 1
    
    return s.get_opponent()

if __name__ == "__main__":
    compare_algorithms()
    test_heuristics_battle() 