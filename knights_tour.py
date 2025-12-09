import time
import tkinter as tk


class KnightsTour:
    def __init__(self, n):
        self.n = n
        # init board n x n = -1 (unvisited)
        self.board = [[-1 for _ in range(n)] for _ in range(n)]
        
        # L-shape move (x, y)
        self.moves = [(2, 1), (1, 2), (-1, 2), (-2, 1),(-2, -1), (-1, -2), (1, -2), (2, -1)]

    def is_safe(self, x, y):
        """
        check apakah move (x, y) valid:
        1. move berada di dalam board
        2. node == -1 (unvisited)
        """
        return 0 <= x < self.n and 0 <= y < self.n and self.board[x][y] == -1

    # Warndsdorff's heuristic
    # count next valid move dari posisi (x, y)
    def get_degree(self, x, y):
        count = 0
        for dx, dy in self.moves:
            if self.is_safe(x + dx, y + dy):
                count += 1
        return count

    def solve(self, start_x, start_y, closed_tour=False):
        # set semua vertex == -1 (unvisited)
        self.board = [[-1 for _ in range(self.n)] for _ in range(self.n)]
        
        # state awal kuda
        self.board[start_x][start_y] = 0
        
        # recursive backtracking
        if self.solve_util(start_x, start_y, 1, closed_tour, start_x, start_y):
            # self.print_solution()
            return True
        else:
            print("Solusi tidak ditemukan")
            return False

    def solve_util(self, x, y, move_count, closed_tour, start_x, start_y):
        # base case: jika move count == total vertex (n*n) => semua vertex visited
        if move_count == self.n * self.n:
            if closed_tour:
                # Closed Tour posisi terakhir di posisi awal
                for dx, dy in self.moves:
                    if x + dx == start_x and y + dy == start_y:
                        return True
                return False
            return True

        # set degrees untuk setiap next move
        next_moves = []
        for dx, dy in self.moves:
            nx, ny = x + dx, y + dy
            if self.is_safe(nx, ny):
                degree = self.get_degree(nx, ny)
                next_moves.append((degree, nx, ny))
        
        # sort berdasarkan degree dari yg terkecil
        next_moves.sort(key=lambda item: item[0])

        # recursive next move berdasarkan urutan degree
        for _, nx, ny in next_moves:
            self.board[nx][ny] = move_count 
            
            if self.solve_util(nx, ny, move_count + 1, closed_tour, start_x, start_y):
                return True
            
            self.board[nx][ny] = -1 # backtracking. kalau tidak berhasil, set unvisited kembali

        return False

    def print_solution(self):
        print("-" * (self.n * 5 + 1))
        for i in range(self.n):
            print("|", end=" ")
            for j in range(self.n):
                print(f"{self.board[i][j]:2d}", end=" | ")
            print()
            print("-" * (self.n * 5 + 1))

class KnightsTourGUI:
    def __init__(self, n, board):
        self.n = n
        self.board = board
        self.window = tk.Tk()
        self.window.title("Knight's Tour Solution")
        
        screen_height = self.window.winfo_screenheight()
        self.canvas_size = min(600, screen_height - 100)
        self.cell_size = self.canvas_size // n
        
        self.canvas = tk.Canvas(self.window, width=self.canvas_size, height=self.canvas_size)
        self.canvas.pack()
        
        self.draw_board()
        self.window.mainloop()

    def draw_board(self):
        # map move numbers to coordinates
        moves = {}
        for r in range(self.n):
            for c in range(self.n):
                moves[self.board[r][c]] = (r, c)

        # draw cells and numbers
        for i in range(self.n):
            for j in range(self.n):
                x1 = j * self.cell_size
                y1 = i * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size
                
                # draw pattern
                color = "white" if (i + j) % 2 == 0 else "#f0f0f0"
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="gray")
                
                move_num = self.board[i][j]
                font_size = max(8, int(self.cell_size/3))
                self.canvas.create_text((x1 + x2) // 2, (y1 + y2) // 2, text=str(move_num+1), font=("Arial", 12, "bold"))
                # self.canvas.create_text((x1 + x2) // 2, (y1 + y2) // 2, text=str(move_num), font=("Arial", 6, "bold"))
                
                if (i, j) == moves[0]:
                    self.canvas.create_oval(x1 + 5, y1 + 5, x2 - 5, y2 - 5, outline="green", width=3)
                if (i, j) == moves[self.n * self.n - 1]:
                    self.canvas.create_oval(x1 + 5, y1 + 5, x2 - 5, y2 - 5, outline="red", width=3)
                

        # path lines
        for k in range(self.n * self.n - 1):
            if k in moves and (k+1) in moves:
                r1, c1 = moves[k]
                r2, c2 = moves[k+1]
                
                x1 = c1 * self.cell_size + self.cell_size // 2
                y1 = r1 * self.cell_size + self.cell_size // 2
                x2 = c2 * self.cell_size + self.cell_size // 2
                y2 = r2 * self.cell_size + self.cell_size // 2
                
                self.canvas.create_line(x1, y1, x2, y2, fill="blue", width=2, arrow=tk.LAST)
                # self.canvas.create_line(x1, y1, x2, y2, fill="black", width=2, arrow=tk.LAST)

        # last move
        last_move = self.n * self.n - 1
        if 0 in moves and last_move in moves:
            r_start, c_start = moves[0]
            r_end, c_end = moves[last_move]
            
            # check if valid
            if (abs(r_start - r_end), abs(c_start - c_end)) in [(1, 2), (2, 1)]:
                 # line from last to first
                x1 = c_end * self.cell_size + self.cell_size // 2
                y1 = r_end * self.cell_size + self.cell_size // 2
                x2 = c_start * self.cell_size + self.cell_size // 2
                y2 = r_start * self.cell_size + self.cell_size // 2
                self.canvas.create_line(x1, y1, x2, y2, fill="red", width=2, arrow=tk.LAST, dash=(4, 2))

if __name__ == "__main__":
    n = 8
    kt = KnightsTour(n)
    # input
    start_x, start_y = int(input("Masukkan posisi awal x (1-8): ")), int(input("Masukkan posisi awal y (1-8): "))
    start_x -= 1  
    start_y -= 1  
    tour_type = input("Pilih tipe tour - open (o) / closed (c): ").strip().lower()
    if tour_type == 'o':
        closed_tour = False
    elif tour_type == 'c':
        closed_tour = True
    else:
        print("Invalid")
    
    if kt.solve(start_x, start_y, closed_tour=closed_tour):
        # kt.print_solution()
        gui = KnightsTourGUI(n, kt.board)
    else:
        print("Solusi tidak ditemukan")


