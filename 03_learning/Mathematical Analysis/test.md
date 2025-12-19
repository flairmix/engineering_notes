<h3> Полезные свойства </h3>

<h4> 1. Двойное Отрицание</h4>

$$
\neg(\neg A) \iff A
$$

<h4> 2. Отрицание Конъюнкции</h4>

$$
\neg(A \land B) \iff (\neg A \lor \neg B)
$$

<h4> 3. Отрицание Дизъюнкции</h4>

$$
\neg (A \lor B) \iff (A \land B)
$$
```python
A = [True, False]
B = [True, False]

for a in A:
    ai = a
    for b in B:
        bi = b
        print(f"A_{ai}, B_{bi}= {not(ai <= bi) == (ai and (not bi))}")
```

<h4> 4. Отрицание Импликации</h4>

$$
\neg (A \to B) \iff (A \land \neg B)
$$

```python
A = [True, False]
B = [True, False]

for a in A:
    ai = a
    for b in B:
        bi = b
        print(f"A_{ai}, B_{bi}= {not(ai <= bi) == (ai and (not bi))}")
```
