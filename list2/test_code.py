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
        """Zwraca listę ruchów jako krotek (r_from, c_from, r_to, c_to)."""
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
    # zmień gracza, zbadaj ruchy przeciwnika
    opp_state = ClobberState(state.board, state.get_opponent())
    opp_moves = len(opp_state.generate_moves())
    return own_moves - opp_moves

def heuristic_positional(state: ClobberState) -> int:
    weight = 0
    m,n = state.m, state.n
    for r in range(m):
        for c in range(n):
            if state.board[r][c] == state.current_player:
                # krawędź zwiększa wagę
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
    print(f"Alpha-Beta: ruch={best_move}, wartość={best_value}, odwiedzone węzły={node_counter}, czas={end-start:.4f}s")
    return best_move, best_value

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

def play_full_game(depth: int, heuristic):
    s = ClobberState(default_board())
    rounds = 0
    print("Plansza startowa:")
    print(s)
    print()
    
    while True:
        if s.is_terminal():
            break
        mv, _ = alphabeta_clobber(s, depth, heuristic)
        if mv is None:
            break
        s = s.apply_move(mv)
        rounds += 1
        if rounds <= 5:  # Pokazuj pierwsze 5 ruchów
            print(f"Po ruchu {rounds}:")
            print(s)
            print()
    print("Koniec gry po rundach:", rounds)
    print("Finalna plansza:")
    print(s)
    print("Zwycięzca:", s.get_opponent())

if __name__ == "__main__":
    print("=== Test podstawowych funkcji ===")
    state = ClobberState(default_board())
    print('Plansza startowa:')
    print(state)
    print('Dostępne ruchy:', len(state.generate_moves()))
    print('Pierwszy ruch:', state.generate_moves()[0] if state.generate_moves() else 'Brak')
    print()
    
    print("=== Test heurystyk ===")
    print("Heurystyka różnicy pionków:", heuristic_piece_diff(state))
    print("Heurystyka mobilności:", heuristic_mobility(state))
    print("Heurystyka pozycyjna:", heuristic_positional(state))
    print()
    
    print("=== Rozgrywka z głębokością 3 ===")
    play_full_game(depth=3, heuristic=heuristic_piece_diff) 