"""Exercise 2: Compare Naive, KMP, and Rabin-Karp string matching."""
import tkinter as tk
from tkinter import messagebox, ttk


def naive(text, pattern):
    matches, comparisons = [], 0
    for i in range(len(text) - len(pattern) + 1):
        for j, char in enumerate(pattern):
            comparisons += 1
            if text[i + j] != char:
                break
        else:
            matches.append(i)
    return matches, comparisons


def lps_table(pattern):
    table, length, i = [0] * len(pattern), 0, 1
    while i < len(pattern):
        if pattern[i] == pattern[length]:
            length += 1; table[i] = length; i += 1
        elif length:
            length = table[length - 1]
        else:
            i += 1
    return table


def kmp(text, pattern):
    table, matches, comparisons = lps_table(pattern), [], 0
    i = j = 0
    while i < len(text):
        comparisons += 1
        if text[i] == pattern[j]:
            i += 1; j += 1
            if j == len(pattern):
                matches.append(i - j); j = table[j - 1]
        elif j:
            j = table[j - 1]
        else:
            i += 1
    return matches, comparisons


def rabin_karp(text, pattern):
    matches, comparisons, base, mod = [], 0, 256, 101
    length = len(pattern); factor = pow(base, length - 1, mod)
    p_hash = t_hash = 0
    for i in range(length):
        p_hash = (base * p_hash + ord(pattern[i])) % mod
        t_hash = (base * t_hash + ord(text[i])) % mod
    for start in range(len(text) - length + 1):
        if p_hash == t_hash:
            for offset, char in enumerate(pattern):
                comparisons += 1
                if text[start + offset] != char:
                    break
            else:
                matches.append(start)
        if start < len(text) - length:
            t_hash = (base * (t_hash - ord(text[start]) * factor) + ord(text[start + length])) % mod
    return matches, comparisons


def run():
    text, pattern = text_var.get(), pattern_var.get()
    if not pattern or len(pattern) > len(text):
        messagebox.showerror("Invalid input", "The pattern must be non-empty and no longer than the text.")
        return
    results = [("Naive", *naive(text, pattern)), ("KMP", *kmp(text, pattern)), ("Rabin-Karp", *rabin_karp(text, pattern))]
    output.delete(*output.get_children())
    for name, matches, comparisons in results:
        output.insert("", "end", values=(name, matches or "No matches", comparisons))


root = tk.Tk(); root.title("Exercise 2 - String Matching"); root.geometry("700x390")
frame = ttk.Frame(root, padding=18); frame.pack(fill="both", expand=True)
ttk.Label(frame, text="String Matching Algorithm Comparison", font=("Segoe UI", 18, "bold")).pack(anchor="w")
text_var = tk.StringVar(value="AABAACAADAABAABA"); pattern_var = tk.StringVar(value="AABA")
for label, variable in [("Text", text_var), ("Pattern", pattern_var)]:
    ttk.Label(frame, text=label).pack(anchor="w", pady=(12, 2)); ttk.Entry(frame, textvariable=variable).pack(fill="x")
ttk.Button(frame, text="Compare algorithms", command=run).pack(anchor="w", pady=16)
output = ttk.Treeview(frame, columns=("algorithm", "matches", "comparisons"), show="headings", height=6)
for key, title, width in [("algorithm", "Algorithm", 170), ("matches", "Match indices", 290), ("comparisons", "Comparisons", 130)]:
    output.heading(key, text=title); output.column(key, width=width, anchor="center")
output.pack(fill="both", expand=True)
root.mainloop()
