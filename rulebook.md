# 📖 Kuzur Programming Language Rulebook v1.2
## 🚀 Introduction

Kuzur Programming Language is a lightweight, modern, and beginner-friendly programming language designed for CLI usage. It supports variables, loops, conditions, functions, and more — all in a simple and readable format.

💡 Goal: Write, test, and run your programs quickly and efficiently with KuzurLang.

### 📌 Basic Syntax Rules
#### 1. Statements

- Every command is a statement.
- Statements are executed line by line.
- End of line is a newline \n.
```
print("Hello, Kuzur!")  # Prints text
```
#### 2. Comments

- Single-line comments start with //
```
 // This is a comment
print("Hello")  // Prints Hello
```
#### 3. Variables

-Declare using assignment =.

-Types: number, string, boolean.
```
x = 10          # number
name = "Polash" # string
flag = true     # boolean
```
#### 4. Data Types

| Type    | Example          |
| ------- | ---------------- |
| Number  | `x = 10`         |
| String  | `name = "Kuzur"` |
| Boolean | `flag = true`    |

### 🌀 Control Flow
#### 1. If, Elif, Else
```
if (x > 10) {
    print("x is greater than 10")
} elif (x == 10) {
    print("x is 10")
} else {
    print("x is less than 10")
}
```
#### 2. Loops
- While Loop
```
  while (x < 5) {
    print(x)
    x = x + 1
}
```
- For Loop
```
  for i = 1; 5 {
    print("Loop: " + i)
}
```
- Do-While Loop
```
  do {
    print(x)
    x = x + 1
} while (x < 5)
```
#### 3. Break & Continue

- break → exit loop immediately

- continue → skip to next iteration
```
  for i = 1; 10 {
    if (i == 5) { break }       // stop loop at 5
    if (i % 2 == 0) { continue } // skip even numbers
    print(i)
}
```

### 🔹 Functions

- Defined with func keyword.

- Parameters in parentheses.

- return to give value.\
```
  func greet(name) {
    print("Hello, " + name + " 👋")
}

greet("Polash")  # Output: Hello, Polash 👋
```
Functions can return values: 

```
func add(a, b) {
    return a + b
}

result = add(5, 7)
print(result)  # 12
```
### 🛠 Built-in Functions

| Function  | Description        | Example                       |
| --------- | ------------------ | ----------------------------- |
| `print()` | Prints to console  | `print("Hello")`              |
| `input()` | Takes user input   | `name = input("Enter name:")` |
| `len()`   | Length of string   | `len("Kuzur") → 5`            |
| `int()`   | Converts to number | `int("10") → 10`              |
| `str()`   | Converts to string | `str(10) → "10"`              |

### ⚡ Operators
#### Arithmetic:
```
+  -  *  /  %
```
#### Comparison:
```
==  !=  <  <=  >  >=
```
#### Logical:
```
&&  ||  !
```
##### Example:
```
x = 5
y = 10
if (x < y && y > 5) {
    print("True ✅")
}
```
### 💡 Variables & Scope
```
- Variables inside functions are local.

= Use functions to avoid global conflicts.
x = 10  # global
func test() {
    x = 5  # local to function
    print(x)
}
test()  # prints 5
print(x) # prints 10
```
