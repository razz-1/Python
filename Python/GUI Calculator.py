"""
GUI Calculator
==============
A fully interactive desktop calculator built with Tkinter (Python's built-in
GUI toolkit, so no extra installs are needed).

Features:
- Standard operations: + - * /
- Decimal point, percentage, sign toggle (+/-)
- Clear (C) and All-Clear (AC)
- Backspace (⌫)
- Keyboard support (type numbers/operators, Enter = "=", Esc = clear)
- Chained calculations (e.g. 5 + 3 + 2 =)
- Basic error handling (e.g. divide by zero)

Run with:
    python calculator.py
"""

import tkinter as tk

# ---------------------------------------------------------------------------
# App state
# ---------------------------------------------------------------------------
current_input = "0"     # what's currently being typed / shown
stored_value = None     # first operand, held while waiting for the second
pending_op = None       # "+", "-", "*", "/"
reset_on_next_digit = False  # True right after an operator or "="


def update_display():
    display_var.set(current_input)


def format_number(value):
    """Turn a float back into a clean string (no trailing .0 clutter)."""
    if value == int(value) and abs(value) < 1e15:
        return str(int(value))
    return str(value)


def input_digit(digit):
    global current_input, reset_on_next_digit
    if reset_on_next_digit or current_input == "0":
        current_input = digit
        reset_on_next_digit = False
    else:
        # avoid absurdly long numbers
        if len(current_input) < 18:
            current_input += digit
    update_display()


def input_decimal():
    global current_input, reset_on_next_digit
    if reset_on_next_digit:
        current_input = "0."
        reset_on_next_digit = False
    elif "." not in current_input:
        current_input += "."
    update_display()


def toggle_sign():
    global current_input
    if current_input != "0":
        if current_input.startswith("-"):
            current_input = current_input[1:]
        else:
            current_input = "-" + current_input
    update_display()


def input_percent():
    global current_input
    try:
        value = float(current_input) / 100
        current_input = format_number(value)
    except ValueError:
        pass
    update_display()


def backspace():
    global current_input
    if reset_on_next_digit:
        return
    if len(current_input) <= 1 or (len(current_input) == 2 and current_input.startswith("-")):
        current_input = "0"
    else:
        current_input = current_input[:-1]
    update_display()


def clear_entry():
    """C: clears just the current entry."""
    global current_input
    current_input = "0"
    update_display()


def all_clear():
    """AC: clears everything, including memory."""
    global current_input, stored_value, pending_op, reset_on_next_digit
    current_input = "0"
    stored_value = None
    pending_op = None
    reset_on_next_digit = False
    update_display()


def apply_pending_operation():
    """Combine stored_value and current_input using pending_op."""
    global stored_value, current_input
    if pending_op is None or stored_value is None:
        return
    a = stored_value
    b = float(current_input)
    try:
        if pending_op == "+":
            result = a + b
        elif pending_op == "-":
            result = a - b
        elif pending_op == "*":
            result = a * b
        elif pending_op == "/":
            result = a / b
        else:
            result = b
        current_input = format_number(result)
    except ZeroDivisionError:
        current_input = "Error"


def choose_operator(op):
    global stored_value, pending_op, reset_on_next_digit
    if stored_value is not None and pending_op is not None and not reset_on_next_digit:
        apply_pending_operation()
        update_display()
        if current_input == "Error":
            stored_value = None
            pending_op = None
            reset_on_next_digit = True
            return
        stored_value = float(current_input)
    else:
        stored_value = float(current_input)

    pending_op = op
    reset_on_next_digit = True
    highlight_operator(op)


def equals():
    global stored_value, pending_op, reset_on_next_digit
    if pending_op is None or stored_value is None:
        return
    apply_pending_operation()
    update_display()
    stored_value = None
    pending_op = None
    reset_on_next_digit = True
    highlight_operator(None)


# ---------------------------------------------------------------------------
# UI setup
# ---------------------------------------------------------------------------
root = tk.Tk()
root.title("Calculator")
root.resizable(False, False)

BG = "#1e1e1e"
DISPLAY_BG = "#1e1e1e"
DISPLAY_FG = "#ffffff"
NUM_BG = "#333333"
NUM_FG = "#ffffff"
OP_BG = "#ff9500"
OP_FG = "#ffffff"
FUNC_BG = "#a5a5a5"
FUNC_FG = "#000000"
ACTIVE_OP_BG = "#ffffff"

root.configure(bg=BG)

display_var = tk.StringVar(value=current_input)

display_frame = tk.Frame(root, bg=BG)
display_frame.grid(row=0, column=0, columnspan=4, sticky="nsew")

display_label = tk.Label(
    display_frame,
    textvariable=display_var,
    anchor="e",
    bg=DISPLAY_BG,
    fg=DISPLAY_FG,
    font=("Helvetica", 40),
    padx=20,
    pady=30,
)
display_label.pack(fill="both", expand=True)

operator_buttons = {}


def make_button(text, row, col, bg, fg, command, colspan=1):
    btn = tk.Button(
        root,
        text=text,
        font=("Helvetica", 20),
        bg=bg,
        fg=fg,
        activebackground=bg,
        activeforeground=fg,
        bd=0,
        relief="flat",
        command=command,
    )
    btn.grid(
        row=row,
        column=col,
        columnspan=colspan,
        sticky="nsew",
        padx=1,
        pady=1,
        ipady=18,
    )
    return btn


def highlight_operator(active_op):
    for op, btn in operator_buttons.items():
        if op == active_op:
            btn.configure(bg=ACTIVE_OP_BG, fg=OP_BG)
        else:
            btn.configure(bg=OP_BG, fg=OP_FG)


# Row 1: AC, +/-, %, /
make_button("AC", 1, 0, FUNC_BG, FUNC_FG, all_clear)
make_button("+/-", 1, 1, FUNC_BG, FUNC_FG, toggle_sign)
make_button("%", 1, 2, FUNC_BG, FUNC_FG, input_percent)
operator_buttons["/"] = make_button("÷", 1, 3, OP_BG, OP_FG, lambda: choose_operator("/"))

# Row 2: 7 8 9 *
make_button("7", 2, 0, NUM_BG, NUM_FG, lambda: input_digit("7"))
make_button("8", 2, 1, NUM_BG, NUM_FG, lambda: input_digit("8"))
make_button("9", 2, 2, NUM_BG, NUM_FG, lambda: input_digit("9"))
operator_buttons["*"] = make_button("×", 2, 3, OP_BG, OP_FG, lambda: choose_operator("*"))

# Row 3: 4 5 6 -
make_button("4", 3, 0, NUM_BG, NUM_FG, lambda: input_digit("4"))
make_button("5", 3, 1, NUM_BG, NUM_FG, lambda: input_digit("5"))
make_button("6", 3, 2, NUM_BG, NUM_FG, lambda: input_digit("6"))
operator_buttons["-"] = make_button("−", 3, 3, OP_BG, OP_FG, lambda: choose_operator("-"))

# Row 4: 1 2 3 +
make_button("1", 4, 0, NUM_BG, NUM_FG, lambda: input_digit("1"))
make_button("2", 4, 1, NUM_BG, NUM_FG, lambda: input_digit("2"))
make_button("3", 4, 2, NUM_BG, NUM_FG, lambda: input_digit("3"))
operator_buttons["+"] = make_button("+", 4, 3, OP_BG, OP_FG, lambda: choose_operator("+"))

# Row 5: ⌫ 0 . =
make_button("⌫", 5, 0, FUNC_BG, FUNC_FG, backspace)
make_button("0", 5, 1, NUM_BG, NUM_FG, lambda: input_digit("0"))
make_button(".", 5, 2, NUM_BG, NUM_FG, input_decimal)
make_button("=", 5, 3, OP_BG, OP_FG, equals)

# Make the grid cells expand evenly
for i in range(4):
    root.grid_columnconfigure(i, weight=1, uniform="col")
for i in range(1, 6):
    root.grid_rowconfigure(i, weight=1)


# ---------------------------------------------------------------------------
# Keyboard bindings
# ---------------------------------------------------------------------------
def on_key(event):
    key = event.keysym
    char = event.char

    if char.isdigit():
        input_digit(char)
    elif char == ".":
        input_decimal()
    elif char in ("+", "-", "*", "/"):
        choose_operator(char)
    elif key in ("Return", "KP_Enter", "equal"):
        equals()
    elif key == "BackSpace":
        backspace()
    elif key == "Escape":
        all_clear()
    elif char == "%":
        input_percent()


root.bind("<Key>", on_key)

update_display()
root.mainloop()