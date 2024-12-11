import streamlit as st
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
import json
import io
from pathlib import Path
import ijson  # For handling large JSON files

st.set_page_config(
    page_title="GeoData Validator",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

def validate_json_file(file):
    """Validate JSON file and return any errors"""
    try:
        # Reset file pointer to start
        file.seek(0)
        
        # Try to parse the JSON file in chunks
        parser = ijson.parse(file)
        for prefix, event, value in parser:
            pass
        
        # Reset file pointer again
        file.seek(0)
        
        # If we got here, the JSON is valid
        data = json.load(file)
        return data, None
        
    except Exception as e:
        return None, f"Invalid JSON file: {str(e)}"

def validate_geojson_structure(data):
    """Validate GeoJSON structure and return any errors"""
    try:
        if not isinstance(data, dict):
            return False, "GeoJSON must be an object"
            
        if data.get("type") != "FeatureCollection":
            return False, "GeoJSON must have type 'FeatureCollection'"
            
        features = data.get("features")
        if not isinstance(features, list):
            return False, "GeoJSON must have a features array"
            
        return True, None
        
    except Exception as e:
        return False, f"Error validating GeoJSON structure: {str(e)}"

def clean_coordinate_data(feature):
    """Clean and validate coordinate data in a feature"""
    try:
        geom = feature.get("geometry", {})
        if geom.get("type") != "Point":
            return feature, "Not a point geometry"
            
        coords = geom.get("coordinates", [])
        if len(coords) != 2:
            return feature, "Invalid coordinate array length"
            
        # Clean coordinates
        lon, lat = coords
        if not (-180 <= lon <= 180 and -90 <= lat <= 90):
            return feature, "Coordinates out of valid range"
            
        return feature, None
        
    except Exception as e:
        return feature, f"Error cleaning coordinates: {str(e)}"

def main():
    st.title("🌍 GeoData Validator and Cleaner")
    st.write("Upload your CSV, JSON, or GeoJSON file to validate and clean geographic data")
    
    with st.sidebar:
        st.header("About")
        st.write("""
        This tool helps validate and clean geographic data files.
        It can handle:
        - CSV files with coordinate columns
        - JSON files with coordinate data
        - GeoJSON files with Point features
        """)
    
    uploaded_file = st.file_uploader("Choose a file", type=['csv', 'json', 'geojson'])
    
    if uploaded_file is not None:
        try:
            # First validate JSON structure
            data, json_error = validate_json_file(uploaded_file)
            
            if json_error:
                st.error(json_error)
                return
                
            # Validate GeoJSON structure
            is_valid, geojson_error = validate_geojson_structure(data)
            
            if geojson_error:
                st.error(geojson_error)
                return
                
            # Process features
            features = data["features"]
            clean_features = []
            issues = []
            
            with st.spinner('Processing features...'):
                for i, feature in enumerate(features):
                    cleaned_feature, error = clean_coordinate_data(feature)
                    if error:
                        issues.append(f"Feature {i}: {error}")
                    clean_features.append(cleaned_feature)
            
            # Show results
            st.success(f"Processed {len(features)} features")
            
            if issues:
                st.warning("Issues found:")
                for issue in issues:
                    st.write(f"- {issue}")
            
            # Create output GeoJSON
            output_geojson = {
                "type": "FeatureCollection",
                "features": clean_features
            }
            
            # Download buttons
            col1, col2 = st.columns(2)
            
            with col1:
                # GeoJSON download
                st.download_button(
                    label="Download Cleaned GeoJSON",
                    data=json.dumps(output_geojson, indent=2),
                    file_name="cleaned_data.geojson",
                    mime="application/json"
                )
            
            with col2:
                # Show preview
                with st.expander("View first 5 features"):
                    st.json(clean_features[:5])
                    
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
            st.write("Please check your file format and try again")

if __name__ == "__main__":
    main()