import pulp

required_lengths = {4: 13, 2.65: 9, 0.7: 36, 0.65: 18}
max_length = 4.8
max_count = 26
tolerance = 0.03
lengths = list(required_lengths.keys())
counts = list(required_lengths.values())


def get_greedy_cuts(lengths: list, max_length: float, tolerance: float) -> list[list]:
    n = len(lengths)
    results = []

    def recurse(current_sum, comb, start_idx):
        any_fit = False
        indices = range(start_idx, n)

        for i in indices:
            L = lengths[i]
            if current_sum + L <= max_length - tolerance:
                any_fit = True
                next_start = i
                recurse(current_sum + L, comb + [L], next_start)

        # if no more cuts fit and we have at least one piece
        if not any_fit and comb:
            results.append(comb)

    recurse(0, [], 0)
    return results


def get_sub_cuts(cut: list) -> list[list]:
    from itertools import combinations

    sub_lists = []
    for r in range(1, len(cut) + 1):
        for combo in combinations(cut, r):
            dict_sub_cut = list_cut_to_dict_cut(combo)
            if dict_sub_cut not in sub_lists:
                sub_lists.append(dict_sub_cut)
    sub_cuts = [dict_cut_to_list_cut(sub_cut) for sub_cut in sub_lists]

    return [sub_cut for sub_cut in sub_cuts if len(sub_cut) > 0]


def get_all_cuts(lengths: list, max_length: float, tolerance: float) -> list[list]:
    base_cuts = get_greedy_cuts(lengths, max_length, tolerance)

    sub_cut_dicts = []
    for cut in base_cuts:
        sub_cuts = get_sub_cuts(cut)
        for sub_cut in sub_cuts:
            sub_cut_dict = list_cut_to_dict_cut(sub_cut)
            if sub_cut_dict not in sub_cut_dicts:
                sub_cut_dicts.append(sub_cut_dict)

    return [[]] + [dict_cut_to_list_cut(sub_cut) for sub_cut in sub_cut_dicts]


def list_cut_to_dict_cut(list_cut: list) -> dict:
    return {i: list_cut.count(i) for i in lengths}


def dict_cut_to_list_cut(dict_cut: dict) -> list:
    return [key for key, value in dict_cut.items() for _ in range(value)]


def get_var_names(n: int) -> list[str]:
    return [f"x{i}" for i in range(n)]


all_cuts = get_all_cuts(lengths, max_length, tolerance)

# 1. Create the problem
problem = pulp.LpProblem("Minimize count", pulp.LpMinimize)

# 2. Decision variables (integer)
var_names = get_var_names(len(all_cuts))
vars = [pulp.LpVariable(name, lowBound=0, cat="Integer") for name in var_names]

# 3. Objective function
problem += pulp.lpSum(vars), "Total cuts"

# 4. Constraints
all_cuts_dicts = [list_cut_to_dict_cut(cut) for cut in all_cuts]
for length, count in zip(lengths, counts):
    problem += (
        pulp.lpSum([var * cut[length] for var, cut in zip(vars, all_cuts_dicts)])
        == count
    )

# 5. Solve
problem.solve()

# 6. Output results
total_used = 0
for var, cut in zip(vars, all_cuts):
    if var.value() > 0:
        total_used += var.value()
        print(f"{cut} x {int(var.value())}, extra: {round(max_length - sum(cut), 2)} m")

print(f"Total count: {total_used}")
