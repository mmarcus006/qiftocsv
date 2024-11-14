import streamlit as st
from src.core.qif_parser import QIFParser
from src.core.csv_generator import CSVGenerator

def main():
    st.set_page_config(page_title="QIF to CSV Converter", layout="centered")
    st.title("QIF to CSV Converter")

    uploaded_file = st.file_uploader("Upload your QIF file", type=["qif"], accept_multiple_files=False)
    
    if uploaded_file is not None:
        try:
            parser = QIFParser()
            parser.parse_file(uploaded_file)
            transactions = parser.get_transactions()
            
            generator = CSVGenerator()
            csv_data = generator.generate_csv(transactions)
            
            st.success("File converted successfully!")
            st.download_button(
                label="Download CSV",
                data=csv_data,
                file_name="converted.csv",
                mime="text/csv"
            )
        except Exception as e:
            st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main() 