# Z70 Hypothetical Architecture Emulator

## Introduction

The hypothetical **Z70 architecture** is a rudimentary version of Intel's x86 architecture. It is an **8-bit architecture** with a **microprogrammed control unit**. Instructions can be encoded in up to **2 bytes**, and the architecture allows addressing up to **256 bytes of memory**. Data is represented using **two's complement**.

This project provides a **Python-based assembler and emulator** for the Z70 architecture, designed for **educational and academic purposes**. It allows users to write, assemble, and execute Z70 assembly programs, inspect registers, flags, and memory dumps, and experiment with low-level computer architecture concepts.

The emulator is **flexible and easy to extend** for custom instructions or architectural modifications.

---

## Project Structure

The codebase is structured for maintainability:

- **`arch.py`**  
  Defines opcodes, addressing modes, and instruction mnemonics.

- **`assembler.py`**  
  Handles parsing, two-pass assembly, and code generation.

- **`CPU.py`**  
  Implements the CPU emulator, including execution and flag management.

- **`Z70.py`**  
  Entry point for running programs, with a command-line interface.

- **`code_samples/`**  
  A collection of example Z70 assembly programs that demonstrate common use cases and instruction patterns.

---

## Z70 Architecture Overview

### Bus

- Address/Data width: **8 bits**

### Registers (8 bits each)

- **A**, **B** – General-purpose registers
- **I** – Addressing register
- **FLAGS** – Status register

### ALU (Arithmetic Logic Unit)

- 8-bit ALU
- Auxiliary registers: **TEMP1**, **TEMP2**, **S**

### Control Registers

- **RDM** – Memory Data Register
- **REM** – Memory Address Register
- **PC** – Program Counter
- **RI** – Instruction Register

### Architecture Model

The architecture follows a **von Neumann model**, with a unified memory space for both code and data.

<p align="center">
  <em>
    <a href="documents/z70_instruction_set.pdf">
      PDF – Z70 architecture datapath diagram (Adami's Notes)
    </a>
  </em>
</p>

---

## Status Register (FLAGS)

The status register is updated by ALU-related instructions. Flags can be used to control program flow.

<p align="center"><strong>FLAGS</strong></p>

<table align="center">
  <tr>
    <th>Bit</th>
    <th>7</th>
    <th>6</th>
    <th>5</th>
    <th>4</th>
    <th>3</th>
    <th>2</th>
    <th>1</th>
    <th>0</th>
  </tr>
  <tr>
    <th>Name</th>
    <td><b>OF</b></td>
    <td><b>CF</b></td>
    <td><b>ZF</b></td>
    <td><b>PF</b></td>
    <td><b>SF</b></td>
    <td>—</td>
    <td>—</td>
    <td>—</td>
  </tr>
</table>

### Flag Definitions

- **OF (Overflow Flag)**: Set when the result of an operation exceeds the representable size limits of the operand.
- **CF (Carry Flag)**: Set (value 1) when an addition operation produces a carry out (carry-out), or when a subtraction operation produces a borrow (borrow-in).
- **ZF (Zero Flag)**: Set when the result of an operation is zero.
- **PF (Parity Flag)**: Set when the result of an operation contains an even number of bits in the logical state 1.
- **SF (Sign Flag)**: Set when the result has a negative sign; this flag copies the most significant bit (sign bit) of the result.
---
## Instruction Set and Addressing Modes

<h3 align="center">Instructions</h3>

<table align="center">
  <tr>
    <th>Type</th>
    <th>Code (Hex)</th>
    <th>Mnemonic</th>
    <th>Function</th>
  </tr>

  <tr>
    <td rowspan="5"><b>Arithmetic</b></td>
    <td>0</td><td><code>add</code></td><td>Addition</td>
  </tr>
  <tr><td>1</td><td><code>sub</code></td><td>Subtraction</td></tr>
  <tr><td>2</td><td><code>cmp</code></td><td>Comparison</td></tr>
  <tr><td>3</td><td><code>inc</code></td><td>Increment</td></tr>
  <tr><td>4</td><td><code>dec</code></td><td>Decrement</td></tr>

  <tr>
    <td rowspan="5"><b>Logical</b></td>
    <td>5</td><td><code>and</code></td><td>Logical AND</td>
  </tr>
  <tr><td>6</td><td><code>or</code></td><td>Logical OR</td></tr>
  <tr><td>7</td><td><code>not</code></td><td>Logical NOT</td></tr>
  <tr><td>8</td><td><code>shr</code></td><td>Shift Right</td></tr>
  <tr><td>9</td><td><code>shl</code></td><td>Shift Left</td></tr>

  <tr>
    <td rowspan="6"><b>Branch</b></td>
    <td>A0</td><td><code>jmp</code></td><td>Unconditional jump</td>
  </tr>
  <tr><td>A1</td><td><code>jz</code></td><td>Jump if zero</td></tr>
  <tr><td>A2</td><td><code>js</code></td><td>Jump if negative</td></tr>
  <tr><td>A3</td><td><code>jc</code></td><td>Jump if carry</td></tr>
  <tr><td>A4</td><td><code>jo</code></td><td>Jump if overflow</td></tr>
  <tr><td>A5</td><td><code>jp</code></td><td>Jump if parity</td></tr>

  <tr>
    <td><b>Move</b></td>
    <td>B</td><td><code>mov</code></td><td>Data movement</td>
  </tr>

  <tr>
    <td><b>Control</b></td>
    <td>FF</td><td><code>nop</code></td><td>No operation</td>
  </tr>
</table>

<h3 align="center">Addressing Modes</h3>

<table align="center">
  <tr>
    <th>Mode</th>
    <th>Code (Hex)</th>
    <th>Operands</th>
  </tr>

  <tr>
    <td rowspan="4"><b>Register</b></td>
    <td>0</td><td>A, B</td>
  </tr>
  <tr><td>1</td><td>B, A</td></tr>
  <tr><td>2</td><td>A, I</td></tr>
  <tr><td>3</td><td>I, A</td></tr>

  <tr>
    <td rowspan="2"><b>Indirect</b></td>
    <td>4</td><td>A, [I]</td>
  </tr>
  <tr><td>5</td><td>[I], A</td></tr>

  <tr>
    <td rowspan="3"><b>Immediate</b></td>
    <td>6</td><td>A, constant</td>
  </tr>
  <tr><td>7</td><td>B, constant</td></tr>
  <tr><td>8</td><td>I, constant</td></tr>

  <tr>
    <td><b>Indirect</b></td>
    <td>9</td><td>[I], constant</td>
  </tr>

  <tr>
    <td rowspan="4"><b>Direct</b></td>
    <td>A</td><td>A, [memory]</td>
  </tr>
  <tr><td>B</td><td>B, [memory]</td></tr>
  <tr><td>C</td><td>[memory], A</td></tr>
  <tr><td>D</td><td>[memory], B</td></tr>
</table>

<h3 align="center">Unary Instructions (1 Operand)</h3>

<table align="center">
  <tr><th>Instructions</th><th>Code (Hex)</th><th>Operand</th></tr>
  <tr>
    <td rowspan="5"><b>inc, dec,<br>not<br>
shr, shl</b></td>
    <tr><td>0</td><td>A</td></tr>
  </tr>
  <tr><td>1</td><td>B</td></tr>
  <tr><td>2</td><td>I</td></tr>
  <tr><td>4</td><td>[I]</td></tr>
</table>

<p align="center">
  <em>
    <a href="documents/z70_instruction_set.pdf">
      PDF – Instruction set and addressing modes of the Z70 architecture (Adami's Notes)
    </a>
  </em>
</p>

---

## Emulator Functionality

### Assembler

- Two-pass assembler
- **First pass**: Parses lines, resolves labels, computes instruction sizes
- **Second pass**: Encodes instructions into memory and generates a listing file (`.lst`)

### CPU Emulator

- Executes instructions sequentially until program end (EOF)
- Implements all opcodes and addressing modes
- Updates flags using efficient bitwise operations
- Uses two's complement arithmetic

### Output

- Final register values: A, B, I, PC (hexadecimal)
- Flag states: OF, CF, ZF, PF, SF
- Optional memory dump (hex + ASCII)
- Optional assembly listing file

### Memory Model

- Unified 256-byte memory (00H–FFH)
- Code loaded starting at 00H
- Remaining space available for data

---

## Usage

Run from the command line:

```bash
python z70.py src.z70 [dump-range] [outfile]
```

### Arguments

- **`src.z70`** – Assembly Z70 source file
- **`dump-range`** *(optional)* – Memory dump range (e.g., `80H-8FH`)
- **`outfile`** *(optional)* – Assembly listing file (e.g., `out.txt`)

Dump ranges wrap around if `start > end` (e.g., `F0H-10H`).

### Example

```bash
python z70.py code_samples/hello_world.z70 80H-8BH out.txt
```

- Assembles and runs `hello_world.z70`
- Dumps memory from 80H to 8BH (ASCII: "Hello World!")
- Writes assembly listing to `out.txt`

---

## Source Syntax

- **Instructions**: `mov I, 80H`
- **Labels**: `LOOP: inc I` or label on its own line
- **Comments**: `// comment`
- **Hex constants**: `80H`, `-80H` (two's complement)

---

## What You Can Do

- Simulate arithmetic with overflow
- Experiment with flag-based branching
- Work with negative numbers using two's complement
- Manipulate memory via indirect addressing
- Implement loops and algorithms (e.g., Fibonacci, bit counting)
- Debug programs via post-execution inspection

---

## Extending the Architecture

To add a new instruction:

1. Update **`arch.py`**: Add opcode, mnemonic, and addressing mode
2. Update **`CPU.py`**: Implement handler logic

The assembler and emulator will automatically support the new instruction (I GUESS).

Custom architectures can be created by modifying opcode and mode tables in `arch.py`.

---

## Contributing

This repository is intended for students and academics studying computer architecture.

Contributions such as bug fixes, new examples, or architectural extensions are welcome. 

Ensure code is:

- Clear and readable
- Optimized (bitwise operations where appropriate)
- Properly tested

---

## Credits

This project is based on teaching materials and lecture notes by Prof. **André Gustavo Adami**, who uses the hypothetical **Z70 architecture** as a pedagogical tool in the course *Fundamentals of Computer Architecture* to introduce low-level concepts and prepare students for later studies in assembly x86 language.

## License

This project is licensed under the [MIT License](LICENSE).
