<img src="https://raw.githubusercontent.com/MarkusThill/AdventOfCode/main/2023/day21/illustration.png" width="500" height="500">

# --- Day 16: Proboscidea Volcanium ---

You can find the original problem statement here: [https://adventofcode.com/2023/day/21](https://adventofcode.com/2023/day/21)

In this riddle, the task is to help an Elf plan its steps on a farm consisting of garden plots and rocks. The Elf starts at a specific plot marked 'S' and can move one step north, south, east, or west, but only onto tiles that are garden plots. The Elf needs to determine which garden plots it can reach exactly with a given number of steps. The puzzle provides a map with the starting position 'S,' garden plots marked '.', and rocks marked '#.' The Elf's goal is to find the number of garden plots it can reach in a specific number of steps.

In the first part, the Elf needs to calculate the number of reachable garden plots in exactly 64 steps. The given example map is used to illustrate the process, but the actual puzzle input is a larger map.

In the second part, the Elf realizes its mistake and states that the map repeats infinitely in every direction. The task is then to determine the number of reachable garden plots starting from the center on an infinite map with a specified number of steps (26501365).

# Some Notes for Part 2:

```
# For the given example, the first few elements of the solutions s[n] look like
# this, where n is the budget of allowed steps.
# ===================================================================================
#
# > S[n]:
# > [  1    2    4    6    9   13   16   22   30   41   50   63   74   89
# >   99  115  129  145  165  192  216  234  261  294  326  353  395  427
# >  460  491  537  574  605  644  689  740  784  846  894  944  989 1053
# > 1107 1146 1196 1256 1324 1383 1464 1528 1594 1653 1735 1805 1853 1914
# > 1988 2072 2145 2244 2324 2406 2479 2579 2665 2722 2794 2882 2982 3069
# > 3186 3282 3380 3467 3585 3687 3753 3836 3938 4054 4155 4290 4402 4516
# > 4617 4753 4871 4946 5040 5156 5288 5403 5556 5684 5814 5929 6083 6217
# > 6301 6406 6536 6684 6813 6984 7128 7274 7403 7575 7725 7818 7934 8078
# > 8242 8385 8574 8734 8896 9039 9229 9395 9497 9624]
# ===================================================================================

# An interesting oberservation is that after some time (certain number of steps)
# we can observe an indirect relationship between s[n] & s[n + W].
# Let us start with the definition:
#
#    S[n] = s[n + 1] - s[n]                                                                    (1)
#
# If we print S[n], on first glance, we do not really notice anything relevant yet:
#
# ===================================================================================
#
# > S[n]:
# > [ 1   2   2   3   4   3   6   8  11   9  13  11  15  10  16  14  16  20
# >  27  24  18  27  33  32  27  42  32  33  31  46  37  31  39  45  51  44
# >  62  48  50  45  64  54  39  50  60  68  59  81  64  66  59  82  70  48
# >  61  74  84  73  99  80  82  73 100  86  57  72  88 100  87 117  96  98
# >  87 118 102  66  83 102 116 101 135 112 114 101 136 118  75  94 116 132
# > 115 153 128 130 115 154 134  84 105 130 148 129 171 144 146 129 172 150
# >  93 116 144 164 143 189 160 162 143 190 166 102 127]
# ===================================================================================
#
# However, if we visually rearange the sequence and take a close look again,
# we might actually detect some pattern:
#
# ===================================================================================
# > S[n]:
# > [ 1   2   2   3   4   3   6   8  11   9  13
# >  11  15  10  16  14  16  20  27  24  18  27
# >  33  32  27  42  32  33  31  46  37  31  39
# >  45  51  44  62  48  50  45  64  54  39  50
# >  60  68  59  81  64  66  59  82  70  48  61
# >  74  84  73  99  80  82  73 100  86  57  72
# >  88 100  87 117  96  98  87 118 102  66  83
# > 102 116 101 135 112 114 101 136 118  75  94
# > 116 132 115 153 128 130 115 154 134  84 105
# > 130 148 129 171 144 146 129 172 150  93 116
# > 144 164 143 189 160 162 143 190 166 102 127]
# ===================================================================================
#
# For example, if we look at the first column, we can see that 144 - 130 = 14,
# 116 - 102 = 14, or, 102 - 88 = 14. In the second column, we have a slightly different,
# but still recurring  pattern: 164 - 148 = 16, 148 - 132 = 16, 132 - 116 = 16, ...
#
# So, the actually interesting observation that we can make here is is the following one:
#
#   ΔS_W[n] = S[n + W] - S[n] = S[n + kW] - S[n + (k-1)W] = const.                             (2)
#
# Let us check, if the above Eq.2 is always valid:
# ===================================================================================
# > ΔS_W[n]:
# > [na na na na na na na na na na na
# >  10 13  8 13 10 13 14 19 13  9 14
# >  22 17 17 26 18 17 11 19 13 13 12
# >  12 19 17 20 16 17 14 18 17  8 11
# >  15 17 15 19 16 16 14 18 16  9 11
# >  14 16 14 18 16 16 14 18 16  9 11
# >  14 16 14 18 16 16 14 18 16  9 11
# >  14 16 14 18 16 16 14 18 16  9 11
# >  14 16 14 18 16 16 14 18 16  9 11
# >  14 16 14 18 16 16 14 18 16  9 11
# >  14 16 14 18 16 16 14 18 16  9 11]
# ===================================================================================
#
# While Eq.(2) does not hold for small n, it is true for n larger than a certain n_critical.
# Hence, assuming that n is sufficiently large, we can extend Eq.2:
#
#   S[n + kW] = S[n + (k-1)W] + ΔS_W[n]
#             = S[n + (k-2)W] + ΔS_W[n] + ΔS_W[n] = S[n + (k-2)W] + 2*ΔS_W[n]
#             = S[n + (k-3)W] + ΔS_W[n] + ΔS_W[n] + ΔS_W[n] = S[n + (k-3)W] + 3*ΔS_W[n]
#             = ...
#             = S[n + (0)W] + ΔS_W[n] + ... + ΔS_W[n]
#             = S[n] + kΔS_W[n]                                                                (3)
#
# Now, let us also look at the following straight-forward definition of the sequence s[n]:
#
#    Δs_W[n] := s[n + W] - s[n]    or:  s[n + W] = s[n] + Δs_W[n]                              (4)
#
# We will use Eq.4 in the following where we rearrange Eq.1:
#
#    s[n + 1] = s[n] + S[n]       <- Rearrangement of (1)
#    s[n + 2] = s[n + 1] + S[n + 1] = s[n] + S[n] + S[n + 1]    <- insert previous line here
#    s[n + 3] = s[n + 2] + S[n + 2] = s[n + 1] + S[n + 1] + S[n + 2] = s[n] + S[n] + S[n + 1] + S[n + 2]
#        .
#        .
#        .
#    s[n + W] = s[n] + S[n] + S[n + 1] + S[n + 2] + ... + S[n + W - 1]
#             = s[n] + Σ_{w=0..W-1}{ S[n + w] }                                                (5)
#
# By comparing Eq.(4) and Eq.(5) we find:
#
#   Σ_{w=0..W-1}{ S[n + w] } = Δs_W[n]                                                         (6)
#
# Equation (6) will be helpful, in the following, where we extend the
# recurrence relation to:
#
#    s[n + 2W] = s[n] + Σ_{w=0..2W-1}{ S[n + w] }
#              = s[n] + Σ_{w=0..W-1}{ S[n + w] } + Σ_{w=0..W-1}{ S[n + w + W] }
#              = s[n] + R(n, 0) + R(n, 1)
#              = s[n] + Δs_W[n] + Δs_W[n] + Σ_{w=0..W-1}{ ΔS_W[n + w] },
#
# where we identified:
#
#    R(n, k) = Σ_{w=0..W-1}{ S[n + w + kW] }
#            = Σ_{w=0..W-1}{ S[n + w] + kΔS_W[n + w] }
#            = Σ_{w=0..W-1}{ S[n + w] } + Σ_{w=0..W-1}{ kΔS_W[n + w] }
#            = Δs_W[n] + k * Σ_{w=0..W-1}{ ΔS_W[n + w] }   <- using (6)
#            = Δs_W[n] + k * Σ_{ΔD},                                                           (7)
# and
#
#   Σ_{ΔD} = Σ_{w=0..W-1}{ ΔS_W[n + w] }                                                       (8)
#
# Finally, we get the general solution:
#
#    s[n + kW] = s[n] + Σ_{w=0..kW-1}{ S[n + w] }
#              = s[n] + Σ_{i=0..k-1} [ Σ_{w=0..W-1}{ S[n + w + iW] } ]
#              = s[n] + Σ_{i=0..k-1} [ R(n, i) ]
#              = s[n] + R(n, 0) + R(n, 1)  + R(n, 2) + ... + R(n, k-1)
#              = s[n] + Δs_W[n] + (Δs_W[n] + Σ_{ΔD}) + (Δs_W[n] + 2Σ_{ΔD}) + ... + (Δs_W[n] + (k-1)Σ_{ΔD})
#              = s[n] + k * Δs_W[n] + Σ_{ΔD} + 2Σ_{ΔD} + ... + (k-1)Σ_{ΔD}
#              = s[n] + k * Δs_W[n] + (1 + 2 + ... + k - 1)Σ_{ΔD}
#              = s[n] + k * Δs_W[n] + k(k - 1)Σ_{ΔD} / 2                                       (9)
#
# Using Eq.(9) allows us to solve for an arbitrary s[n], just knowing a small part of its history!
```