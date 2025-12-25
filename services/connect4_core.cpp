#include <pybind11/pybind11.h>
#include <vector>
#include <algorithm>
#include <cmath>
#include <iostream>

namespace py = pybind11;

constexpr int EMPTY = 0;
constexpr int PLAYER = 1;
constexpr int COMPUTER = -1;
constexpr int ROWS = 6;
constexpr int COLS = 7;

class Connect4Core
{
public:
    int board[ROWS][COLS] = {};

    Connect4Core()
    {
        reset();
    }

    void reset()
    {
        for (auto& r : board)
            for (int& c : r)
                c = EMPTY;
    }

    int make_move(const int col, const int piece)
    {
        if (col < 0 || col >= COLS) return -1;
        for (int row = ROWS - 1; row >= 0; row--)
            if (board[row][col] == EMPTY)
            {
                board[row][col] = piece;
                return row;
            }
        return -1;
    }

    void remove_piece(const int row, const int col)
    {
        board[row][col] = EMPTY;
    }

    bool check_winner(const int piece, const int last_row, const int last_col) const
    // last_row and last_col are the position of the last placed piece
    // This function checks all four directions for a win around the last placed piece
    {
        for (int i = 0; i < 4; i++)
        {
            constexpr int dc[] = {1, 0, 1, -1};
            constexpr int dr[] = {0, 1, 1, 1};
            int count = 0;
            // check positive direction
            for (int step = 1; step < 4; step++)
            {
                const int r = last_row + dr[i] * step;
                const int c = last_col + dc[i] * step;
                if (r < 0 || r >= ROWS || c < 0 || c >= COLS || board[r][c] != piece)
                    break;
                count++;
            }

            // check negative direction
            for (int step = 1; step < 4; step++)
            {
                const int r = last_row - dr[i] * step;
                const int c = last_col - dc[i] * step;
                if (r < 0 || r >= ROWS || c < 0 || c >= COLS || board[r][c] != piece)
                    break;
                count++;
            }

            if (count >= 3)
                return true;
        }
        return false;
    }

    // --- Minimax Logic ---

    int score_window(const int r, const int c, const int dr, const int dc) const
    {
        int score = 0;

        int count_piece = 0;
        int count_empty = 0;
        int count_opp = 0;

        for (int i = 0; i < 4; i++)
        {
            const int val = board[r + i * dr][c + i * dc];
            if (val == COMPUTER) count_piece++;
            else if (val == EMPTY) count_empty++;
            else count_opp++;
        }

        // Reward our progress
        if (count_piece == 4) score += 100;
        else if (count_piece == 3 && count_empty == 1) score += 5;
        else if (count_piece == 2 && count_empty == 2) score += 2;

        // Penalize opponent threats (Block them!)
        if (count_opp == 3 && count_empty == 1) score -= 80;

        return score;
    }

    int evaluate_board()
    {
        int score = 0;

        // 1. Score Center Column (Control the center = better options)
        int center_count = 0;
        for (const auto& r : board)
        {
            if (r[3] == COMPUTER) center_count++;
        }
        score += center_count * 3;

        // 2. Score Horizontal
        for (int r = 0; r < ROWS; r++)
        {
            for (int c = 0; c < COLS - 3; c++)
            {
                score += score_window(r, c, 0, 1);
            }
        }

        // 3. Score Vertical
        for (int c = 0; c < COLS; c++)
        {
            for (int r = 0; r < ROWS - 3; r++)
            {
                score += score_window(r, c, 1, 0);
            }
        }

        // 4. Score Diagonal (Positive Slope /)
        for (int r = 0; r < ROWS - 3; r++)
        {
            for (int c = 0; c < COLS - 3; c++)
            {
                score += score_window(r, c, 1, 1);
            }
        }

        // 5. Score Diagonal (Negative Slope \)
        for (int r = 3; r < ROWS; r++)
        {
            for (int c = 0; c < COLS - 3; c++)
            {
                score += score_window(r, c, -1, 1);
            }
        }

        return score;
    }

    std::pair<int, int> get_best_move(const int depth, int alpha, int beta, const int piece)
    {
        std::vector<int> valid_moves;
        for (int c = 0; c < COLS; c++)
        {
            if (board[0][c] == EMPTY)
                valid_moves.push_back(c);
        }
        // Prioritize center columns
        std::sort(valid_moves.begin(), valid_moves.end(), [](const int a, const int b)
        {
            return abs(a - 3) < abs(b - 3);
        });
        int best_col = -1;
        int best_score = (piece == COMPUTER) ? -2000000 : 200000;
        if (valid_moves.empty()) return {0, -1};

        for (int col : valid_moves)
        {
            const int row = make_move(col, piece);

            // check for win
            if (check_winner(piece, row, col))
            {
                remove_piece(row, col);
                // prioritize winning sooner (add depth to score) and losing later (subtract depth from score)
                return {(piece == COMPUTER) ? 1000000 + depth : -1000000 - depth, col};
            }

            int score;
            if (depth == 0)
            {
                score = evaluate_board();
            }
            else
            {
                score = get_best_move(depth - 1, alpha, beta, -piece).first;
            }
            remove_piece(row, col);
            if (piece == COMPUTER)
            {
                if (score > best_score)
                {
                    best_score = score;
                    best_col = col;
                }
                alpha = std::max(alpha, best_score);
            }
            else
            {
                if (score < best_score)
                {
                    best_score = score;
                    best_col = col;
                }
                beta = std::min(beta, best_score);
            }
            if (beta <= alpha)
                break; // Alpha-Beta Pruning
        }
        if (best_col == -1 && !valid_moves.empty())
            best_col = valid_moves[0];

        if (depth == 9) {
                std::cout << "Best choice: Col " << best_col << " with score " << best_score << std::endl;
            }
        return {best_score, best_col};
    }
};

PYBIND11_MODULE(connect4_core, m)
{
    py::class_<Connect4Core>(m, "Connect4Core")
        .def(py::init<>())
        .def("make_move", &Connect4Core::make_move)
        .def("check_winner", &Connect4Core::check_winner)
        .def("reset", &Connect4Core::reset)
        // Wrapper: Automatically handles Alpha/Beta infinities for Python
        .def("get_best_move", [](Connect4Core& self, int depth, int piece)
        {
            return self.get_best_move(depth, -1000000000, 1000000000, piece);
        });
}
