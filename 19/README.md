# Day 19 solution

## Description (or, confession)
What began as a pretty straightforward recursive solution for Part 1 ended up making Part 2 needlessly difficult. I started Day 19 one day late already, because I was too busy the day of, and spent several more days struggling to shoehorn my existing solution to solve Part 2.

The result is basically the same recursive algorithm, but each recursive step can return a "backtrack index" that indicates how far into that rule's list of alternations it got. Then, the caller can use that backtrack index to generate a new alternation to add to its own list, effectively allowing it to backtrack to that previous child rule. If the new alternation is reached, then the child rule resumes from the previously returned backtrack index, dismissing the alternations prior to that index. This is accomplished by appending a "!" to the name of the child rule, followed by the backtrack index. The index is later parsed back out from the rule string.

Unfortunately, since each child rule may have done this very same thing to its own child rules (generating new alternations to its list along the way), then when a rule is revisited during a backtrack, it must still visit all of its alternations in order to ensure that it regenerates the additional alternations for its child rules. But during this pass, any matches are ignored. This is very inefficient and I'm frankly not sure it even works in general, but it gives the right result for this challenge.

I'm not particularly proud of this solution. It is hacky, slow, and poorly engineered in the interest of "just getting the thing to work." But as I said in [the top-level README for this repository](../README.md):

> my only metric for whether the program "works" is if it provides the correct answer for the purposes of the AoC challenge.

## Inputs
Most of my solution directories have a single `input.txt` file. This one has two. `input.txt` is the input I was given by the AoC website. `input2.txt` is the Part 2 input, with rules 8 and 11 manually edited as the website directed. Looking at Reddit comments and solutions posted by others, it seems some people chose to specially overwrite those rules in their Part 2 code.

I decided to treat the two parts as two different inputs that can be given to the same program. I believe this is the cleaner/more natural way to view this challenge, and this is the one area in which I will claim superiority for my solution. So there.

## Performance
Just to underscore how atrocious my solution is, here is how the two parts perform on my laptop (i7-7500U, albeit running under WSL 1):

```
$ time ./grammar.py ./input.txt
Matches: 233

real    0m1.916s
user    0m1.750s
sys     0m0.063s

$ time ./grammar.py ./input2.txt
Matches: 396

real    0m24.935s
user    0m21.047s
sys     0m0.734s
```