"""
CSV Analysis module for finding patterns and connections in data
"""

import pandas as pd
import numpy as np
from scipy.stats import pearsonr, spearmanr
from pathlib import Path
from typing import Dict, List, Tuple, Any

class CSVAnalyzer:
    def __init__(self, file_path: Path):
        self.file_path = file_path
        self.data = None
        self.numeric_columns = []
        self.categorical_columns = []
        
    def load_data(self) -> pd.DataFrame:
        """Load CSV data and identify column types"""
        try:
            # Try different encodings
            encodings = ['utf-8', 'latin-1', 'cp1252']
            for encoding in encodings:
                try:
                    self.data = pd.read_csv(self.file_path, encoding=encoding)
                    break
                except UnicodeDecodeError:
                    continue
            
            if self.data is None:
                raise ValueError("Unable to read CSV file with any supported encoding")
            
            # Identify column types
            self.numeric_columns = self.data.select_dtypes(include=[np.number]).columns.tolist()
            self.categorical_columns = self.data.select_dtypes(include=['object']).columns.tolist()
            
            return self.data
            
        except Exception as e:
            raise Exception(f"Error loading CSV file: {e}")
    
    def get_summary(self) -> Dict[str, Any]:
        """Get basic summary statistics"""
        if self.data is None:
            raise ValueError("Data not loaded. Call load_data() first.")
        
        summary = {
            'shape': self.data.shape,
            'columns': list(self.data.columns),
            'numeric_columns': self.numeric_columns,
            'categorical_columns': self.categorical_columns,
            'missing_values': self.data.isnull().sum().to_dict(),
            'basic_stats': self.data.describe().to_dict() if self.numeric_columns else {}
        }
        
        return summary
    
    def find_connections(self) -> List[Dict[str, Any]]:
        """Find statistical connections between columns"""
        connections = []
        
        # Numeric correlations
        if len(self.numeric_columns) > 1:
            corr_matrix = self.data[self.numeric_columns].corr()
            
            for i, col1 in enumerate(self.numeric_columns):
                for j, col2 in enumerate(self.numeric_columns[i+1:], i+1):
                    correlation = corr_matrix.loc[col1, col2]
                    
                    if abs(correlation) > 0.3:  # Threshold for significant correlation
                        connections.append({
                            'type': 'correlation',
                            'column1': col1,
                            'column2': col2,
                            'strength': abs(correlation),
                            'direction': 'positive' if correlation > 0 else 'negative',
                            'value': correlation
                        })
        
        # Categorical associations (basic frequency analysis)
        for cat_col in self.categorical_columns:
            for num_col in self.numeric_columns:
                # Check if categorical variable affects numeric variable
                grouped = self.data.groupby(cat_col)[num_col].agg(['mean', 'std', 'count'])
                if len(grouped) > 1:  # More than one category
                    variance_ratio = grouped['std'].max() / (grouped['std'].min() + 1e-10)
                    if variance_ratio > 2:  # Significant difference in variance
                        connections.append({
                            'type': 'categorical_influence',
                            'categorical_column': cat_col,
                            'numeric_column': num_col,
                            'strength': min(variance_ratio / 10, 1.0),  # Normalize to 0-1
                            'details': grouped.to_dict()
                        })
        
        return sorted(connections, key=lambda x: x['strength'], reverse=True)
    
    def get_outliers(self, column: str, method: str = 'iqr') -> pd.Series:
        """Identify outliers in a numeric column"""
        if column not in self.numeric_columns:
            raise ValueError(f"Column '{column}' is not numeric")
        
        data_col = self.data[column].dropna()
        
        if method == 'iqr':
            Q1 = data_col.quantile(0.25)
            Q3 = data_col.quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            return data_col[(data_col < lower_bound) | (data_col > upper_bound)]
        
        elif method == 'zscore':
            z_scores = np.abs((data_col - data_col.mean()) / data_col.std())
            return data_col[z_scores > 3]
        
        return pd.Series()