#!/usr/bin/env python3
"""
AutoCSV - CSV Visualization and Connection Analysis Tool
Main entry point for the application
"""

import argparse
import sys
from pathlib import Path
from csv_analyzer import CSVAnalyzer
from visualizer import Visualizer

def main():
    parser = argparse.ArgumentParser(description='Analyze and visualize CSV files')
    parser.add_argument('file', help='Path to CSV file')
    parser.add_argument('--output', '-o', help='Output directory for visualizations', default='output')
    parser.add_argument('--connections', '-c', action='store_true', help='Find connections in data')
    parser.add_argument('--visualize', '-v', action='store_true', help='Generate visualizations')
    parser.add_argument('--format', choices=['png', 'html', 'both'], default='both', help='Output format')
    
    args = parser.parse_args()
    
    # Check if file exists
    csv_file = Path(args.file)
    if not csv_file.exists():
        print(f"Error: File '{args.file}' not found.")
        sys.exit(1)
    
    # Initialize analyzer and visualizer
    analyzer = CSVAnalyzer(csv_file)
    visualizer = Visualizer(output_dir=args.output)
    
    try:
        # Load and analyze data
        print(f"Loading CSV file: {csv_file}")
        data = analyzer.load_data()
        print(f"Loaded {len(data)} rows with {len(data.columns)} columns")
        
        # Basic analysis
        summary = analyzer.get_summary()
        print("\nData Summary:")
        print(summary)
        
        # Find connections if requested
        if args.connections:
            print("\nAnalyzing connections...")
            connections = analyzer.find_connections()
            print(f"Found {len(connections)} potential connections")
            
            # Visualize connections
            if args.visualize:
                visualizer.plot_connections(connections, data, format=args.format)
        
        # Generate basic visualizations if requested
        if args.visualize:
            print("\nGenerating visualizations...")
            visualizer.create_basic_plots(data, format=args.format)
            print(f"Visualizations saved to: {args.output}")
            
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()