<div align="center">
    <img src="https://img.shields.io/badge/version-1.0.0-blueviolet" alt="Version">
    <img src="https://img.shields.io/badge/status-active-success" alt="Status">
    <img src="https://img.shields.io/badge/platform-windows%20%7C%20linux-blue" alt="Platform">
</div>

<br />

<div align="center">
  <img src="https://via.placeholder.com/800x400.png?text=Gamma+AI+Watermark+Remover" alt="Project Banner">
</div>

<h1 align="center">🔓 Gamma AI Watermark Remover</h1>

<p align="center">
  Effortlessly remove watermarks from Gamma AI generated PDFs with a sleek, user-friendly interface
</p>

## 🌟 Features

- 📄 **Drag and Drop Support**: Simple PDF file handling
- 🕵️ **Intelligent Watermark Detection**: Advanced image comparison algorithms
- 🧹 **One-Click Watermark Removal**: Clean, hassle-free process
- 💻 **Cross-Platform**: Works on Windows and Linux
- 🎨 **Modern UI**: Elegant and intuitive design

## 🚀 Quick Start

### Prerequisites

- 🐍 Python 3.8+
- 💻 Windows or Linux OS

### Installation

#### 1. Clone the Repository

```bash
git clone https://github.com/YourUsername/GammaWatermarkRemover.git
cd GammaWatermarkRemover
```

#### 2. Create Virtual Environment

<details open>
<summary><strong>🪟 Windows Setup</strong></summary>

```batch
# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```
</details>

<details>
<summary><strong>🐧 Linux Setup</strong></summary>

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```
</details>

### 🖥️ Running the Application

```bash
# With virtual environment activated
python main.py
```

## 🛠️ Building Executable

<details open>
<summary><strong>Build Instructions</strong></summary>

### Prerequisites
- PyInstaller
- Project files

### Build Process

#### Windows
```batch
# Activate virtual environment
venv\Scripts\activate

# Run build script
python build.py
```

#### Linux
```bash
# Activate virtual environment
source venv/bin/activate

# Run build script
python build.py
```

### Output
- Executable in `dist` folder
- Named `GammaWatermarkRemover`
</details>

## 📦 Dependencies

| Library | Version | Purpose |
|---------|---------|---------|
| PyQt5 | >=5.15.0 | User Interface |
| PyMuPDF | >=1.18.0 | PDF Processing |
| Pillow | >=8.0.0 | Image Manipulation |
| NumPy | >=1.19.0 | Numerical Computing |
| PyInstaller | >=4.5.0 | Application Packaging |

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 👥 Authors

- **Original Author**: [@DedInc](https://github.com/DedInc)
- **Ported By**: [@AlexanderQueen](https://github.com/AlexanderQueen)

## 📜 License

[Specify Your License Here]

---

<div align="center">
    <sub>Built with ❤️ for PDF enthusiasts</sub>
</div>
