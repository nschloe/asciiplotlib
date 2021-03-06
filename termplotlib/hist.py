from .barh import _get_matrix_of_eighths, _trim_trailing_zeros, barh
from .helpers import is_unicode_standard_output


def hist(
    counts,
    bin_edges,
    orientation="vertical",
    max_width=40,
    bins=20,
    grid=None,
    bar_width=1,
    strip=False,
    force_ascii=False,
):
    if orientation == "vertical":
        return hist_vertical(
            counts,
            xgrid=grid,
            bar_width=bar_width,
            strip=strip,
            force_ascii=force_ascii,
        )

    assert orientation == "horizontal", f"Unknown orientation '{orientation}'"
    return hist_horizontal(
        counts,
        bin_edges,
        max_width=40,
        bins=20,
        bar_width=bar_width,
        force_ascii=force_ascii,
    )


def hist_horizontal(
    counts,
    bin_edges,
    max_width=40,
    bins=20,
    bar_width=1,
    show_bin_edges=True,
    show_counts=True,
    force_ascii=False,
):
    if show_bin_edges:
        labels = [
            "{:+.2e} - {:+.2e}".format(bin_edges[k], bin_edges[k + 1])
            for k in range(len(bin_edges) - 1)
        ]
    else:
        labels = None

    out = barh(
        counts,
        labels=labels,
        max_width=max_width,
        bar_width=bar_width,
        show_vals=show_counts,
        force_ascii=force_ascii,
    )

    return out


def _flip(matrix):
    """Mirrors a matrix left to right"""
    n_cols = len(matrix[0])
    return [[row[-(col_i + 1)] for row in matrix] for col_i in range(n_cols)]


def hist_vertical(
    counts,
    bins=30,
    max_height=10,
    bar_width=2,
    strip=False,
    xgrid=None,
    force_ascii=False,
):
    if xgrid is None:
        xgrid = []

    matrix = _get_matrix_of_eighths(counts, max_height, bar_width)

    if strip:
        # Cut off leading and trailing rows of 0
        num_head_rows_delete = 0
        for row in matrix:
            if any([item != 0 for item in row]):
                break
            num_head_rows_delete += 1

        num_tail_rows_delete = 0
        for row in matrix[::-1]:  # trim from bottom row upwards
            if any([item != 0 for item in row]):
                break
            num_tail_rows_delete += 1  # if row was all zeros, mark it for deletions
        n_total_rows = len(matrix)
        matrix = matrix[num_head_rows_delete : n_total_rows - num_tail_rows_delete]
    else:
        num_head_rows_delete = 0

    if is_unicode_standard_output() and not force_ascii:
        block_chars = [" ", "▁", "▂", "▃", "▄", "▅", "▆", "▇", "█"]
        left_seven_eighths = "▉"
    else:
        block_chars = [" ", "*", "*", "*", "*", "*", "*", "*", "*"]
        left_seven_eighths = "*"

    # print text matrix
    out = []
    for row in _flip(matrix):
        # Cut off trailing zeros
        trimmed_row = _trim_trailing_zeros(row)

        # converts trimmed row into block chars
        c = [block_chars[item] for item in trimmed_row]

        # add grid lines
        for i in xgrid:
            pos = (i - num_head_rows_delete) * bar_width - 1
            if row[pos] == 8 and (pos + 1 == len(row) or row[pos + 1] > 0):
                c[pos] = left_seven_eighths

        out.append("".join(c))

    return out
