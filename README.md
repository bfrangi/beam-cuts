# Beam Cuts

Script for finding the optimal way to cut a set of beams or lengths of material.
The solution is obtained using integer linear programming via the package `pulp`.

## Set-up

1. Clone the repo and install `pulp` (using `pip`, for example).
2. Replace the variables at the start of the script with your desired values:

  ```python
  # Dictionary containing the `length: count` requirements.
  # In the example below, we want 13 units of length 4, 9 units
  # of length 2.65, 36 units of length 0.7 and 18 units of length
  # 0.65.
  required_lengths = {4: 13, 2.65: 9, 0.7: 36, 0.65: 18}
  # The length of the raw material.
  max_length = 4.8
  # The maximum available units of the raw material.
  max_count = 26
  # The tolerance left to make the cuts between each piece, since
  cutting often takes up a certain width.
  tolerance = 0.03
  ```
3. Run the script: `python solve_cuts.py`.
