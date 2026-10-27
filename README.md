# Knight's Tour

A small Python program that searches for a knight's tour: a sequence of chess-knight moves that visits every square on a square board exactly once.

The program uses a Warnsdorff-style move-ordering heuristic with backtracking to find a tour, then displays the sequence of visited squares.

## Requirements

- Python 3.10 or later
- No third-party packages

## Run

From the project directory, start the interactive program:

```bash
python TourDuCavalier.py
```

Follow the prompts to enter the board size and the knight's starting column and row. Starting coordinates are zero-based: on a 5 × 5 board, valid values are `0` through `4`. Press Enter when prompted to generate a solution. The program then asks whether you want to solve another board; enter `n` or `non` to quit.

The program handles 1 × 1 boards as a trivial tour and reports that 2 × 2 and 3 × 3 boards have no solution. Its configured maximum board size is 31, but larger searches can take a long time or exceed Python's recursion limit depending on the board and starting square.

## Use from Python

The solver can also be imported and called directly:

```python
from TourDuCavalier import setUpAndSolves

result = setUpAndSolves(boardSize=5, columnPosition=0, rowPosition=0)
print(result)
```

For a solved board, the function returns the tour as a string of square labels, using columns `A`, `B`, and so on and rows starting at `1`. For invalid or unsolvable inputs, it returns a message describing the result.

## Project structure

- `TourDuCavalier.py` — interactive command-line program and tour-solving functions.

## Contributing

You are welcome to fork this project and modify it to suit your needs.

## License

This project is intended to be open source, and I welcomes forking and modification. There is not currently a formal license file in the repository; simply ask me by mail if you want to distribute it : devanlaylucas006@gmail.com