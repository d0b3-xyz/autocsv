# AutoCSV - CSV Visualization and Connection Analysis Tool

A Python tool for analyzing CSV files, finding connections between data columns, and creating visualizations.

## Features

- **CSV Loading**: Supports multiple encodings and handles various CSV formats
- **Data Analysis**: 
  - Basic statistical summaries
  - Correlation analysis between numeric columns
  - Categorical variable influence on numeric variables
  - Outlier detection
- **Visualizations**:
  - Distribution plots for numeric data
  - Bar charts for categorical data
  - Correlation heatmaps
  - Pairwise relationship plots
  - Connection network graphs
- **Multiple Output Formats**: PNG images and interactive HTML plots
- **Connection Analysis**: Automatically finds and visualizes relationships in your data

## Installation

1. Clone this repository:
```bash
git clone https://github.com/d0b3-xyz/autocsv.git
cd autocsv
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage

Analyze a CSV file:
```bash
python main.py your_data.csv
```

### Advanced Options

```bash
# Find connections and generate visualizations
python main.py data.csv --connections --visualize

# Specify output directory
python main.py data.csv --output results/

# Choose output format
python main.py data.csv --visualize --format html
```

### Command Line Options

- `file`: Path to your CSV file (required)
- `--output, -o`: Output directory for visualizations (default: 'output')
- `--connections, -c`: Find connections in the data
- `--visualize, -v`: Generate visualizations
- `--format`: Output format - 'png', 'html', or 'both' (default: 'both')

## Examples

### Analyzing Sales Data
```bash
python main.py sales_data.csv --connections --visualize
```

This will:
1. Load the sales data
2. Analyze correlations between numeric columns
3. Find categorical influences on numeric data
4. Generate distribution plots, correlation heatmaps, and connection networks
5. Save results to the 'output' directory

### Output Files

The tool generates several types of visualizations:

- `distributions.png/html`: Histograms of numeric columns
- `categorical.png`: Bar charts of categorical data
- `correlation_heatmap.png/html`: Correlation matrix visualization
- `pairplot.png`: Pairwise relationships (for datasets with 2-6 numeric columns)
- `connection_network.png`: Network graph showing variable relationships
- `connection_details.png`: Detailed plots of strongest connections

## Connection Types

The tool identifies two main types of connections:

1. **Correlations**: Statistical relationships between numeric variables
   - Pearson correlation coefficient
   - Threshold: |r| > 0.3 for significance

2. **Categorical Influence**: How categorical variables affect numeric variables
   - Based on variance differences across categories
   - Useful for identifying grouping effects

## Requirements

- Python 3.7+
- pandas
- numpy
- matplotlib
- seaborn
- plotly
- scipy
- networkx

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is open source. Please check the license file for details.

## Future Enhancements

- [ ] Support for more file formats (Excel, JSON, etc.)
- [ ] Advanced statistical tests for connections
- [ ] Machine learning-based pattern detection
- [ ] Interactive web interface
- [ ] Real-time data streaming support
- [ ] Custom connection rule definitions