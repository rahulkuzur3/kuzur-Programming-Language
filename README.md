[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Snap](https://img.shields.io/badge/Snap-Ready-orange.svg)](snap/)
# Kuzur programming language  🐍✨

**Kuzur programming language ** is a tiny, learnable programming language designed by Rahul Kuzur.  
It’s inspired by Python and allows you to run `.kz` files easily on Windows and Linux.  

## 🚀 Features

-  Variables: numbers, strings, booleans
- Conditional statements: `if`, `elif`, `else` 🔄
- Loops: `while`, `for`, `do-while` 🔁
- Control: `break`, `continue` ⛔✅
- Functions: `func`, `return` 🔹
- Blocks with `{ ... }` like C/JavaScript 
- Built-ins: `print()`, `input()`, `len()`, `int()`, `str()`
- Fully CLI-based, lightweight & lightning fast ⚡
- Cross-platform: Windows & Linux standalone executables
- Single-line comments with `//`
---

## 💻 Installation

### **Windows**

1. Download the latest **Kuzur interpreter** from here.  
2. Run `kuzur.exe`.  
3. Run your `.kz` program:

```bat
kuzur myprogram.kz
```
Optional: Add kuzur.exe to your PATH for global access.


---

### **Linux**

#### Debian/Ubuntu-based:
```
sudo apt update
sudo apt install wget
wget -O kuzur https://example.com/file.zip](https://raw.githubusercontent.com/rahulkuzur3/kuzur-Programming-Language/refs/heads/main/interpreter/Linux/kuzur
sudo mv kuzur /usr/local/bin/
chmod +x /usr/local/bin/kuzur
sudo rm -f kuzur
```
#### Fedora/RedHat/CentOS:
```
sudo dnf install wget   # Fedora
```
```
sudo yum install wget   # CentOS/RedHat
```

```
wget -O kuzur https://example.com/file.zip](https://raw.githubusercontent.com/rahulkuzur3/kuzur-Programming-Language/refs/heads/main/interpreter/Linux/kuzur
sudo mv kuzur /usr/local/bin/
chmod +x /usr/local/bin/kuzur
sudo rm -f kuzur
```
#### Arch Linux/Manjaro:
```
sudo pacman -S wget
wget -O kuzur https://example.com/file.zip](https://raw.githubusercontent.com/rahulkuzur3/kuzur-Programming-Language/refs/heads/main/interpreter/Linux/kuzur
sudo mv kuzur /usr/local/bin/
chmod +x /usr/local/bin/kuzur
sudo rm -f kuzur
```
#### OpenSUSE:
```
sudo zypper install wget
wget -O kuzur https://example.com/file.zip](https://raw.githubusercontent.com/rahulkuzur3/kuzur-Programming-Language/refs/heads/main/interpreter/Linux/kuzur
sudo mv kuzur /usr/local/bin/
chmod +x /usr/local/bin/kuzur
sudo rm -f kuzur
```

### Termux:

```
pkg update
pkg install wget
wget -O kuzur https://example.com/file.zip](https://raw.githubusercontent.com/rahulkuzur3/kuzur-Programming-Language/refs/heads/main/interpreter/Linux/kuzur
mv kuzur $PREFIX/bin/
chmod +x $PREFIX/bin/kuzur
rm -rf kuzur
```

#### Run your .kz program:


```
kuzur myprogram.kz
```

#### 📝 Quick Start

Example program:
```
// hello_world.kz
print("Hello, KuzurLang!")

func add(a, b) {
    return a + b
}

print("2 + 3 =", add(2, 3))
```
Run it:
```
kuzur hello_world.kz
```
Output:
```
Hello, KuzurLang!
2 + 3 = 5

```

🤝 Contributing

Feel free to submit pull requests or open issues.
Follow the code style in kuzurlang.py and add examples to examples/.


---

📜 License

MIT License. See LICENSE for details.


---

Made with ❤️ by Rahul Kuzur 

