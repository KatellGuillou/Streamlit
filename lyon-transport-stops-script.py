import os
import logging
from pathlib import Path

import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
import streamlit as st

def configure_logging():
    """Configure logging for the application"""
    logging.basicConfig(
        level=logging.INFO, 
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

def read_csv_in_chunks(file_path, chunk_size=1000):
    """
    Read CSV file in chunks with error handling
    
    Args:
        file_path (str or Path): Path to the input CSV file
        chunk_size (int, optional): Number of rows to read in each chunk. Defaults to 1000.
    
    Returns:
        tuple: A tuple containing chunks iterator and total number of lines
    """
    try:
        # Get total number of lines for progress tracking
        total_lines = sum(1 for _ in open(file_path, 'r', encoding='utf-8')) - 1
        
        chunks = pd.read_csv(
            file_path,
            chunksize=chunk_size,
            encoding='utf-8'
        )
        return chunks, total_lines
    except Exception as e:
        logging.error(f"Error reading CSV file: {e}")
        raise

def create_geometry(df):
    """
    Create geometry points from latitude and longitude
    
    Args:
        df (pandas.DataFrame): DataFrame with 'lon' and 'lat' columns
    
    Returns:
        list: List of Shapely Point geometries
    """
    try:
        geometry = [Point(xy) for xy in zip(df['lon'], df['lat'])]
        return geometry
    except Exception as e:
        logging.error(f"Error creating geometry: {e}")
        raise

def process_data(input_file, output_file):
    """
    Process the input CSV file and create a GeoDataFrame with geometry
    
    Args:
        input_file (str or Path): Path to the input CSV file
        output_file (str or Path): Path to save the output CSV file
    
    Returns:
        pandas.DataFrame: Processed DataFrame with geometry
    """
    try:
        # Verify input file exists
        if not os.path.exists(input_file):
            raise FileNotFoundError(f"Input file not found at {input_file}")

        chunks, total_lines = read_csv_in_chunks(input_file)
        processed_chunks = []
        
        # Streamlit progress bar
        progress_bar = st.progress(0)
        
        for i, chunk in enumerate(chunks):
            # Validate lat/lon columns
            if 'lat' not in chunk.columns or 'lon' not in chunk.columns:
                raise ValueError("Required columns 'lat' and 'lon' not found in CSV")
            
            # Create GeoDataFrame
            geometry = create_geometry(chunk)
            gdf = gpd.GeoDataFrame(chunk, geometry=geometry, crs="EPSG:4326")
            
            # Convert geometry to WKT format for CSV storage
            gdf['geometry'] = gdf['geometry'].astype(str)
            
            processed_chunks.append(gdf)
            
            # Update progress bar
            progress_bar.progress((i + 1) / total_lines)
        
        # Combine all chunks
        final_df = pd.concat(processed_chunks, ignore_index=True)
        
        # Save to CSV
        final_df.to_csv(output_file, index=False, encoding='utf-8')
        st.success(f"Successfully saved processed data to {output_file}")
        
        return final_df
        
    except Exception as e:
        st.error(f"Error in data processing: {e}")
        raise

def display_summary_statistics(df):
    """
    Display summary statistics of the processed data
    
    Args:
        df (pandas.DataFrame): Processed DataFrame
    """
    st.subheader("Summary Statistics")
    st.write(f"Total number of records: {len(df)}")
    st.write(f"Number of unique locations: {len(df.groupby(['lat', 'lon']))}")
    
    # Display DataFrame information
    st.subheader("Column Information")
    buffer = []
    df.info(buf=buffer)
    st.text('\n'.join(buffer))

def main():
    """
    Streamlit main application
    """
    st.title("Lyon Public Transport Stops Geometry Processor")
    
    # Configure logging
    configure_logging()
    
    # File uploader
    uploaded_file = st.file_uploader(
        "Choose a CSV file", 
        type=['csv'], 
        help="Upload the Lyon public transport stops CSV file"
    )
    
    if uploaded_file is not None:
        # Temporary file paths
        input_file = Path.home() / 'Downloads' / 'input_transport_stops.csv'
        output_file = Path.home() / 'Downloads' / 'lyon_transport_stops_with_geometry.csv'
        
        # Save uploaded file
        with open(input_file, 'wb') as f:
            f.write(uploaded_file.getbuffer())
        
        # Process the data
        try:
            result_df = process_data(input_file, output_file)
            
            # Display sample of processed data
            st.subheader("Sample of Processed Data")
            st.dataframe(result_df.head())
            
            # Display summary statistics
            display_summary_statistics(result_df)
            
            # Optional: Provide download link for processed file
            with open(output_file, 'rb') as f:
                st.download_button(
                    label="Download Processed CSV",
                    data=f,
                    file_name='lyon_transport_stops_with_geometry.csv',
                    mime='text/csv'
                )
        
        except Exception as e:
            st.error(f"An error occurred during processing: {e}")
        
        # Clean up temporary files
        finally:
            if os.path.exists(input_file):
                os.remove(input_file)

if __name__ == "__main__":
    main()
