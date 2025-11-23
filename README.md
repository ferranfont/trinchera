# Trinchera Mean Reversion Strategy

Advanced mean reversion trading strategy for NQ (Nasdaq-100 E-mini) futures based on big volume detection and market profile analysis.

## ⚡ Quick Installation

**ABRIR UNA VENTANA POWERSHELL Y EJECUTAR:**

```powershell
# 1. Instalar todas las dependencias
pip install -r requirements.txt

# 2. Ejecutar el pipeline completo
python main_trinchera.py
```

**Dependencias instaladas:**
- ✅ pandas (procesamiento de datos)
- ✅ plotly (gráficos interactivos HTML)
- ✅ numpy (cálculos numéricos)
- ✅ python-dateutil (manejo de fechas)

## Overview

The Trinchera strategy identifies large volume spikes (>200 contracts) and creates mean reversion levels around the closing price. It trades when price touches these extreme levels (±10 points from the volume spike), expecting the price to revert to the mean.

### Key Features

- ✅ **Fully Portable**: Self-contained with local `utils/` folder (no external dependencies)
- ✅ **Automated Pipeline**: One command runs entire backtest workflow
- ✅ **Date-Based Configuration**: Centralized DATE parameter for easy batch processing
- ✅ **Interactive Visualizations**: HTML charts with Plotly showing trades, equity, and performance
- ✅ **Market Profile Analysis**: Rolling volume profile with 1-second precision
- ✅ **Multiple Filter System**: SMA, Time-of-Day, GRID, Trailing Stop
- ✅ **Comprehensive Reports**: Detailed performance metrics and risk analysis

---

## Quick Start

### 1. Configure Date

Edit `config_trinchera.py`:

```python
DATE = "20251104"  # Date for time_and_sales_nq_{DATE}.csv file
```

### 2. Add Data

Place your tick data file in:
```
data/historic/time_and_sales_nq_20251104.csv
```

### 3. Run Pipeline

```bash
python main_trinchera.py
```

This automatically:
- ✅ Checks if data is processed (runs `util_trinchera.py` if needed)
- ✅ Detects big volume events
- ✅ Executes trading strategy
- ✅ Generates interactive charts
- ✅ Creates summary reports

---

## Strategy Logic

### 1. Big Volume Detection

Identifies frames where `total_volume > BIG_VOLUME_TRIGGER` (default: 200 contracts)

### 2. Mean Reversion Levels

Calculates levels around the big volume close price:
- **Upper Level** (RED): `close_price + MEAN_REVERS_EXPAND` → SELL zone
- **Lower Level** (GREEN): `close_price - MEAN_REVERS_EXPAND` → BUY zone

### 3. Trade Execution

- **SELL Signal**: Price touches red line → expect drop
- **BUY Signal**: Price touches green line → expect rise

### 4. Risk Management

- **Take Profit**: 5 points ($100)
- **Stop Loss**: 9 points ($180)
- **Timeout**: Levels expire after configured duration

---

## Project Structure

```
trinchera_strategy/
├── README.md                          # This file
├── config_trinchera.py               # ⚙️ Centralized configuration (DATE, TP/SL, filters)
├── main_trinchera.py                 # 🚀 Main pipeline orchestrator
│
├── utils/                            # 📦 Portable utilities (self-contained)
│   ├── __init__.py
│   ├── rolling_profile.py           # Market Profile calculator
│   ├── tick.py                      # Tick data structure
│   └── parse_utils.py               # Timestamp & number parsers
│
├── util_trinchera.py                # STEP 0: Tick → Frame processor
├── find_big_volume.py               # STEP 1: Volume detector
├── strat_trinchera.py               # STEP 2: Trading strategy
├── plot_trinchera_trades.py         # STEP 3: Trade visualization
├── summary_trinchera.py             # STEP 4: Summary report
└── plot_equity_trinchera.py         # STEP 5: Equity curve
│
├── data/                            # 📁 Input data
│   └── historic/
│       └── time_and_sales_nq_{DATE}.csv
│
├── outputs/                         # 📊 Processed data
│   ├── db_trinchera_all_data_{DATE}.csv    # OHLCV + Market Profile
│   ├── db_trinchera_bins_{DATE}.csv        # Big volume events
│   └── db_trinchera_TR_{DATE}.csv          # Executed trades
│
└── charts/                          # 📈 HTML visualizations
    ├── chart_trinchera_trades_{DATE}.html  # Trade markers
    ├── summary_trinchera_{DATE}.html       # Performance metrics
    └── equity_trinchera_{DATE}.html        # Equity curve
```

---

## Installation

### Prerequisites

- Python 3.8 or higher
- Git (for cloning the repository)

### Step 1: Install Git

If you don't have Git installed, download and install it from:
- **Windows**: [https://git-scm.com/download/win](https://git-scm.com/download/win)
- **Mac**: [https://git-scm.com/download/mac](https://git-scm.com/download/mac) or use `brew install git`
- **Linux**: `sudo apt-get install git` (Debian/Ubuntu) or `sudo yum install git` (Red Hat/CentOS)

Verify Git installation:
```bash
git --version
```

### Step 2: Clone Repository

```bash
git clone https://github.com/ferranfont/trinchera.git
cd trinchera
```

### Step 3: Install Python Dependencies

```bash
pip install -r requirements.txt
```

Or install manually:
```bash
pip install pandas plotly
```

---

## Configuration

### DATE Configuration (CRITICAL)

**The `DATE` parameter is the ONLY place where you specify the date to process.**

All scripts automatically use this centralized DATE:
- ✅ `util_trinchera.py` - Looks for `time_and_sales_nq_{DATE}.csv`
- ✅ `find_big_volume.py` - Loads `db_trinchera_all_data_{DATE}.csv`, creates `db_trinchera_bins_{DATE}.csv`
- ✅ `strat_trinchera.py` - Loads bins and data with DATE, creates `db_trinchera_TR_{DATE}.csv`
- ✅ `plot_trinchera_trades.py` - Loads all files with DATE
- ✅ `summary_trinchera.py` - Loads trades with DATE, includes DATE in HTML title
- ✅ `plot_equity_trinchera.py` - Loads trades with DATE

**Important**: NEVER hardcode dates in individual scripts. Always import and use `DATE` from `config_trinchera.py`.

### Core Parameters (`config_trinchera.py`)

```python
# ============================================================================
# DATA SOURCE
# ============================================================================
DATE = "20251104"  # Date for time_and_sales_nq_{DATE}.csv file

# ============================================================================
# BIG VOLUME DETECTION
# ============================================================================
BIG_VOLUME_TRIGGER = 200           # Minimum volume to detect (contracts)
BIG_VOLUME_TIMEOUT = 10            # Big volume effect duration (minutes)

# ============================================================================
# TRADING PARAMETERS
# ============================================================================
TP_POINTS = 5.0                    # Take profit (points) → $100
SL_POINTS = 9.0                    # Stop loss (points) → $180
MEAN_REVERS_EXPAND = 10            # Distance from close price (points)
MEAN_REVERSE_TIMEOUT_ORDER = 3    # Mean reversion timeout (minutes)

# ============================================================================
# FILTERS
# ============================================================================
FILTER_BY_SMA = False              # Enable SMA-200 directional filter
FILTER_TIME_OF_DAY = False         # Enable time-of-day filter
FILTER_USE_GRID = False            # Enable second entry (grid system)

# ============================================================================
# ADVANCED FEATURES
# ============================================================================
# SMA Trailing Stop
SMA_TRAILING_STOP = False          # Dynamic trailing stop (disables fixed TP)
TRAILING_STOP_ATR_MULT = 0.75      # Distance from extreme price (points)

# Cash & Trail Hybrid
SMA_CASH_TRAILING_ENABLED = False  # Hybrid: Fixed SL → Trailing after profit
SMA_CASH_TRAILING = 25.0           # Activation threshold (points in favor)
SMA_CASH_TRAILING_DISTANCE = 10.0  # Trailing distance after activation

# GRID System (Second Entry)
GRID_MEAN_REVERS_EXPAND = 5.0      # Additional distance for 2nd entry
GRID_TP_POINTS = 4.0               # TP from average entry price
GRID_SL_POINTS = 3.0               # SL beyond second entry
```

---

## Data Format

### Input File

**Location**: `data/historic/time_and_sales_nq_{DATE}.csv`

**Format** (European CSV):
```csv
Timestamp;Precio;Volumen;Lado
2025-11-04 06:00:00.404;20425.25;1;BID
2025-11-04 06:00:00.512;20425.50;2;ASK
```

**Requirements**:
- Separator: `;` (semicolon)
- Decimal: `,` (comma)
- Columns: `Timestamp`, `Precio`, `Volumen`, `Lado`
- `Lado` values: `"BID"` or `"ASK"`

---

## Pipeline Execution

### Automatic Mode (Recommended)

```bash
python main_trinchera.py
```

**Steps executed**:
1. ✅ Check if `db_trinchera_all_data_{DATE}.csv` exists
2. ✅ If not → Run `util_trinchera.py` automatically
3. ✅ Detect big volume events → `db_trinchera_bins_{DATE}.csv`
4. ✅ Execute strategy → `db_trinchera_TR_{DATE}.csv`
5. ✅ Generate trade chart → `chart_trinchera_trades_{DATE}.html`
6. ✅ Generate summary → `summary_trinchera_{DATE}.html`
7. ✅ Generate equity curve → `equity_trinchera_{DATE}.html`

### Manual Mode (Step by Step)

```bash
# STEP 0: Process tick data (run once per date)
python util_trinchera.py

# STEP 1: Detect big volume
python find_big_volume.py

# STEP 2: Run strategy
python strat_trinchera.py

# STEP 3: Generate trade chart
python plot_trinchera_trades.py

# STEP 4: Generate summary
python summary_trinchera.py

# STEP 5: Generate equity curve
python plot_equity_trinchera.py
```

---

## Output Files

### Processed Data (`outputs/`)

| File | Description | Size (typical) |
|------|-------------|----------------|
| `db_trinchera_all_data_{DATE}.csv` | 1-second OHLCV + Market Profile | ~10-15 MB |
| `db_trinchera_bins_{DATE}.csv` | Big volume events with levels | ~6-30 KB |
| `db_trinchera_TR_{DATE}.csv` | Executed trades with P&L | ~4-30 KB |

### HTML Charts (`charts/`)

| File | Description | Features |
|------|-------------|----------|
| `chart_trinchera_trades_{DATE}.html` | Trade visualization | Interactive markers, levels, volume |
| `summary_trinchera_{DATE}.html` | Performance report | Metrics table with date in header |
| `equity_trinchera_{DATE}.html` | Equity curve | 3-panel chart (equity, P&L, drawdown) |

**Note**: All files include `{DATE}` in filename and title for easy identification.

---

## Performance Metrics

### Typical Results (1-day backtest)

```
Total Trades: 95
Win Rate: 78.9%
Total P&L: +$3,900 (195 points)
Profit Factor: 2.08
Max Drawdown: -$1,420

Winners: 75 trades (avg: +$100)
Losers: 20 trades (avg: -$180)

BUY trades: 44 (46.3%) → +$1,600
SELL trades: 51 (53.7%) → +$2,300
```

### Processing Speed

- **Tick Processing**: ~193K ticks → ~61K frames in 2-3 minutes
- **Big Volume Detection**: ~61K frames → ~22-103 events in <10 seconds
- **Strategy Backtest**: ~22-103 events → ~20-95 trades in <30 seconds
- **Chart Generation**: 3 HTML files in <20 seconds
- **Total Pipeline**: 3-4 minutes end-to-end

---

## Advanced Features

### SMA Filter

```python
FILTER_BY_SMA = True
```

**Logic**:
- Price < SMA-200 → ONLY SELL orders
- Price > SMA-200 → ONLY BUY orders

### Time-of-Day Filter

```python
FILTER_TIME_OF_DAY = True
START_TRADING_TIME = "18:50:00"
END_TRADING_TIME = "22:50:00"
```

**Logic**: Only trades within specified hours

### GRID System (Second Entry)

```python
FILTER_USE_GRID = True
GRID_MEAN_REVERS_EXPAND = 5.0
```

**Logic**:
- 1st entry: `MEAN_REVERS_EXPAND` (10 pts)
- 2nd entry: `MEAN_REVERS_EXPAND + GRID_MEAN_REVERS_EXPAND` (15 pts)
- TP/SL calculated from average entry price

### Trailing Stop

```python
SMA_TRAILING_STOP = True
TRAILING_STOP_ATR_MULT = 0.75
```

**Logic**:
- **Disables** fixed TP (let profits run)
- LONG: SL = `highest_price - TRAILING_STOP_ATR_MULT` (moves UP only)
- SHORT: SL = `lowest_price + TRAILING_STOP_ATR_MULT` (moves DOWN only)

---

## Troubleshooting

### Issue: No data file found

```
FileNotFoundError: Data file not found: db_trinchera_all_data_20251104.csv
```

**Solution**:
```bash
# main_trinchera.py will auto-run util_trinchera.py if missing
python main_trinchera.py
```

### Issue: No big volume events detected

**Solution**: Lower volume trigger
```python
BIG_VOLUME_TRIGGER = 150  # Lower from 200
```

### Issue: No trades executed

**Solution**: Increase mean reversion distance
```python
MEAN_REVERS_EXPAND = 15  # Increase from 10
```

### Issue: Charts not opening

**Solution**: Manually open from `charts/` folder
```bash
# Windows
explorer charts\chart_trinchera_trades_20251104.html

# Linux/Mac
open charts/chart_trinchera_trades_20251104.html
```

### Issue: Chart X-axis misalignment (different time ranges)

**Symptom**: Chart shows data from two different dates on same X-axis

**Cause**: Different data sources (price, trades, bins) loading from different dates

**Solution**: Ensure all scripts use `DATE` from `config_trinchera.py`:
```python
# ✅ Correct (uses DATE from config)
BINS_FILE = OUTPUTS_DIR / f"db_trinchera_bins_{DATE}.csv"

# ❌ Wrong (searches for latest file - can load wrong date)
bins_files = sorted(OUTPUTS_DIR.glob("db_trinchera_bins_*.csv"))
BINS_FILE = bins_files[-1]
```

**Verification**: All files should show same DATE:
- `db_trinchera_all_data_{DATE}.csv`
- `db_trinchera_bins_{DATE}.csv`
- `db_trinchera_TR_{DATE}.csv`

---

## Batch Processing Multiple Dates

```python
# batch_process.py
from pathlib import Path
import subprocess

dates = ["20251103", "20251104", "20251105"]

for date in dates:
    # Update config
    config = Path("config_trinchera.py").read_text()
    config = config.replace(
        f'DATE = "{dates[0]}"' if dates[0] else 'DATE = "20251104"',
        f'DATE = "{date}"'
    )
    Path("config_trinchera.py").write_text(config)

    # Run pipeline
    subprocess.run(["python", "main_trinchera.py"])
```

---

## Strategy Optimization

### Parameter Sensitivity

| Parameter | Effect | Recommendation |
|-----------|--------|----------------|
| `BIG_VOLUME_TRIGGER` | Lower = More trades | Start at 200, test 150-300 |
| `MEAN_REVERS_EXPAND` | Higher = More touches | Test 8-15 points |
| `TP_POINTS` | Higher = Better R:R | Test 4-10 points |
| `SL_POINTS` | Lower = Less risk | Test 7-12 points |

### Optimization Workflow

1. Run baseline with default parameters
2. Modify ONE parameter at a time
3. Compare metrics (Profit Factor, Sharpe, Drawdown)
4. Document results in `optimization_log.csv`

---

## Development

### Adding New Features

1. **Update `config_trinchera.py`** with new parameters
2. **Modify strategy script** (`strat_trinchera.py`)
3. **Test on single date** first
4. **Update README.md** with documentation
5. **Commit changes** with descriptive message

### Code Style

- European CSV format: `sep=';', decimal=','`
- Use `DATE` parameter from config
- Progress messages: `[INFO]`, `[OK]`, `[ERROR]`
- All outputs include `{DATE}` in filename

---

## Citation

If you use this strategy in research or production:

```bibtex
@software{trinchera2025,
  title={Trinchera Mean Reversion Strategy},
  author={Ferran Font},
  year={2025},
  url={https://github.com/ferranfont/trinchera}
}
```

---

## License

Proprietary - Internal use only

---

## Support

For questions or issues:
1. Check [Troubleshooting](#troubleshooting) section
2. Review code comments in Python files
3. Contact: [GitHub Issues](https://github.com/ferranfont/trinchera/issues)

---

**Version**: 2.0
**Last Updated**: 2025-11-22
**Status**: Production Ready ✅

**Key Improvements in v2.0**:
- ✅ Fully portable with local `utils/` folder
- ✅ Centralized DATE configuration (all files use config_trinchera.py)
- ✅ Automatic data processing in pipeline
- ✅ Date displayed in all HTML titles and filenames
- ✅ Self-contained (no external dependencies)
- ✅ Fixed X-axis alignment in charts (all data sources use same DATE)
- ✅ Removed duplicate time filter code (unified in config)
