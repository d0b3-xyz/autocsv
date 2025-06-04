"""
Visualization module for creating charts and connection graphs
"""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import networkx as nx
from pathlib import Path
from typing import List, Dict, Any

class Visualizer:
    def __init__(self, output_dir: str = 'output'):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        # Set style
        plt.style.use('seaborn-v0_8')
        sns.set_palette("husl")
        
    def create_basic_plots(self, data: pd.DataFrame, format: str = 'both'):
        """Create basic visualization plots for the dataset"""
        numeric_cols = data.select_dtypes(include=[np.number]).columns
        categorical_cols = data.select_dtypes(include=['object']).columns
        
        # Distribution plots for numeric columns
        if len(numeric_cols) > 0:
            self._create_distribution_plots(data, numeric_cols, format)
        
        # Bar plots for categorical columns
        if len(categorical_cols) > 0:
            self._create_categorical_plots(data, categorical_cols, format)
        
        # Correlation heatmap
        if len(numeric_cols) > 1:
            self._create_correlation_heatmap(data, numeric_cols, format)
        
        # Pairplot for numeric data (if not too many columns)
        if 2 <= len(numeric_cols) <= 6:
            self._create_pairplot(data, numeric_cols, format)
    
    def _create_distribution_plots(self, data: pd.DataFrame, numeric_cols: pd.Index, format: str):
        """Create distribution plots for numeric columns"""
        n_cols = len(numeric_cols)
        n_rows = (n_cols + 2) // 3  # 3 columns per row
        
        fig, axes = plt.subplots(n_rows, 3, figsize=(15, 5 * n_rows))
        
        # Korrigiere die axes-Behandlung
        if n_rows == 1 and n_cols == 1:
            axes = [axes]
        elif n_rows == 1:
            axes = axes  # axes ist bereits ein Array
        else:
            axes = axes.flatten()
        
        for i, col in enumerate(numeric_cols):
            if i < len(axes):
                axes[i].hist(data[col].dropna(), bins=30, alpha=0.7, edgecolor='black')
                axes[i].set_title(f'Distribution of {col}')
                axes[i].set_xlabel(col)
                axes[i].set_ylabel('Frequency')
        
        # Hide empty subplots
        for i in range(len(numeric_cols), len(axes)):
            axes[i].set_visible(False)
        
        plt.tight_layout()
        
        if format in ['png', 'both']:
            plt.savefig(self.output_dir / 'distributions.png', dpi=300, bbox_inches='tight')
        
        if format in ['html', 'both']:
            # Create interactive plotly version
            fig_plotly = make_subplots(
                rows=n_rows, cols=3,
                subplot_titles=[f'Distribution of {col}' for col in numeric_cols]
            )
            
            for i, col in enumerate(numeric_cols):
                row = i // 3 + 1
                col_pos = i % 3 + 1
                fig_plotly.add_trace(
                    go.Histogram(x=data[col].dropna(), name=col, showlegend=False),
                    row=row, col=col_pos
                )
            
            fig_plotly.update_layout(height=400 * n_rows, title_text="Data Distributions")
            fig_plotly.write_html(self.output_dir / 'distributions.html')
        
        plt.close()
    
    def _create_categorical_plots(self, data: pd.DataFrame, categorical_cols: pd.Index, format: str):
        """Create bar plots for categorical columns"""
        n_cols = len(categorical_cols)
        n_rows = (n_cols + 2) // 3  # 2 columns per row
        
        fig, axes = plt.subplots(n_rows, 3, figsize=(15, 5 * n_rows))
        if n_rows == 1 and n_cols == 1:
            axes = [axes] if n_cols == 1 else axes
        else:
            axes = axes.flatten()
        
        for i, col in enumerate(categorical_cols):
            if i < len(axes):
                value_counts = data[col].value_counts().head(10)  # Top 10 categories
                axes[i].bar(range(len(value_counts)), value_counts.values)
                axes[i].set_title(f'Top Categories in {col}')
                axes[i].set_xlabel('Categories')
                axes[i].set_ylabel('Count')
                axes[i].set_xticks(range(len(value_counts)))
                axes[i].set_xticklabels(value_counts.index, rotation=45, ha='right')
        
        # Hide empty subplots
        for i in range(len(categorical_cols), len(axes)):
            axes[i].set_visible(False)
        
        plt.tight_layout()
        
        if format in ['png', 'both']:
            plt.savefig(self.output_dir / 'categorical.png', dpi=300, bbox_inches='tight')
        
        plt.close()
    
    def _create_correlation_heatmap(self, data: pd.DataFrame, numeric_cols: pd.Index, format: str):
        """Create correlation heatmap"""
        corr_matrix = data[numeric_cols].corr()
        
        plt.figure(figsize=(10, 8))
        sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', center=0,
                   square=True, fmt='.2f')
        plt.title('Correlation Heatmap')
        plt.tight_layout()
        
        if format in ['png', 'both']:
            plt.savefig(self.output_dir / 'correlation_heatmap.png', dpi=300, bbox_inches='tight')
        
        if format in ['html', 'both']:
            fig_plotly = px.imshow(corr_matrix, text_auto=True, aspect="auto",
                                 title="Correlation Heatmap")
            fig_plotly.write_html(self.output_dir / 'correlation_heatmap.html')
        
        plt.close()
    
    def _create_pairplot(self, data: pd.DataFrame, numeric_cols: pd.Index, format: str):
        """Create pairplot for numeric columns"""
        if format in ['png', 'both']:
            pairplot = sns.pairplot(data[numeric_cols].dropna())
            pairplot.fig.suptitle('Pairwise Relationships', y=1.02)
            plt.savefig(self.output_dir / 'pairplot.png', dpi=300, bbox_inches='tight')
            plt.close()
    
    def plot_connections(self, connections: List[Dict[str, Any]], data: pd.DataFrame, format: str = 'both'):
        """Visualize connections found in the data"""
        if not connections:
            print("No connections to visualize")
            return
        
        # Create network graph of connections
        self._create_connection_network(connections, format)
        
        # Create detailed plots for strongest connections
        self._create_connection_details(connections[:5], data, format)  # Top 5 connections
    
    def _create_connection_network(self, connections: List[Dict[str, Any]], format: str):
        """Create network graph showing connections between variables"""
        G = nx.Graph()
        
        # Add nodes and edges
        for conn in connections:
            if conn['type'] == 'correlation':
                G.add_edge(conn['column1'], conn['column2'], 
                          weight=conn['strength'], 
                          type=conn['type'],
                          direction=conn['direction'])
            elif conn['type'] == 'categorical_influence':
                G.add_edge(conn['categorical_column'], conn['numeric_column'],
                          weight=conn['strength'],
                          type=conn['type'])
        
        plt.figure(figsize=(12, 8))
        pos = nx.spring_layout(G, k=1, iterations=50)
        
        # Draw nodes
        nx.draw_networkx_nodes(G, pos, node_color='lightblue', 
                              node_size=1000, alpha=0.8)
        
        # Draw edges with different colors for different connection types
        correlation_edges = [(u, v) for u, v, d in G.edges(data=True) if d['type'] == 'correlation']
        influence_edges = [(u, v) for u, v, d in G.edges(data=True) if d['type'] == 'categorical_influence']
        
        if correlation_edges:
            nx.draw_networkx_edges(G, pos, edgelist=correlation_edges, 
                                 edge_color='red', alpha=0.6, width=2)
        if influence_edges:
            nx.draw_networkx_edges(G, pos, edgelist=influence_edges,
                                 edge_color='blue', alpha=0.6, width=2, style='dashed')
        
        # Draw labels
        nx.draw_networkx_labels(G, pos, font_size=10, font_weight='bold')
        
        plt.title('Variable Connection Network')
        plt.axis('off')
        
        # Add legend
        legend_elements = []
        if correlation_edges:
            legend_elements.append(plt.Line2D([0], [0], color='red', lw=2, label='Correlation'))
        if influence_edges:
            legend_elements.append(plt.Line2D([0], [0], color='blue', lw=2, 
                                            linestyle='--', label='Categorical Influence'))
        
        if legend_elements:
            plt.legend(handles=legend_elements)
        
        if format in ['png', 'both']:
            plt.savefig(self.output_dir / 'connection_network.png', dpi=300, bbox_inches='tight')
        
        plt.close()
    
    def _create_connection_details(self, top_connections: List[Dict[str, Any]], 
                                 data: pd.DataFrame, format: str):
        """Create detailed plots for the strongest connections"""
        n_connections = len(top_connections)
        if n_connections == 0:
            return
        
        fig, axes = plt.subplots(n_connections, 1, figsize=(10, 4 * n_connections))
        if n_connections == 1:
            axes = [axes]
        
        for i, conn in enumerate(top_connections):
            if conn['type'] == 'correlation':
                # Scatter plot for correlations
                x_data = data[conn['column1']].dropna()
                y_data = data[conn['column2']].dropna()
                
                # Align the data (remove rows where either is NaN)
                common_idx = x_data.index.intersection(y_data.index)
                x_data = x_data[common_idx]
                y_data = y_data[common_idx]
                
                axes[i].scatter(x_data, y_data, alpha=0.6)
                axes[i].set_xlabel(conn['column1'])
                axes[i].set_ylabel(conn['column2'])
                axes[i].set_title(f"Correlation: {conn['column1']} vs {conn['column2']} "
                                f"(r = {conn['value']:.3f})")
                
                # Add trend line
                z = np.polyfit(x_data, y_data, 1)
                p = np.poly1d(z)
                axes[i].plot(x_data, p(x_data), "r--", alpha=0.8)
                
            elif conn['type'] == 'categorical_influence':
                # Box plot for categorical influence
                data.boxplot(column=conn['numeric_column'], 
                           by=conn['categorical_column'], ax=axes[i])
                axes[i].set_title(f"Influence: {conn['categorical_column']} on {conn['numeric_column']}")
        
        plt.tight_layout()
        
        if format in ['png', 'both']:
            plt.savefig(self.output_dir / 'connection_details.png', dpi=300, bbox_inches='tight')
        
        plt.close()