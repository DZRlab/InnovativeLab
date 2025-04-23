import pandas as pd
import os
import codecs
import logging

def merge_csv_files(base_file='D:\\test\\Merging\\Contracts.csv', 
                    update_file='D:\\test\\Merging\\ContractNew.csv', 
                    output_file=None):
    """
    Merge two CSV files with UTF-16 LE encoding and semicolon delimiter,
    adding data from the update file to the base file without the header row.
    
    Parameters:
    -----------
    base_file : str
        Path to the base CSV file (e.g., D:\\test\\Merging\\Contracts.csv)
    update_file : str
        Path to the update file (e.g., D:\\test\\Merging\\ContractNew.csv)
    output_file : str, optional
        Path to save the merged file. If None, will overwrite the base file.
        
    Returns:
    --------
    str : Path to the merged file
    """
    try:
        logging.basicConfig(level=logging.INFO)
        
        def check_encoding(file_path):
            try:
                with codecs.open(file_path, 'r', encoding='utf-16le') as f:
                    f.read(100)
                logging.info(f"File {file_path} successfully opened with UTF-16 LE encoding")
                return True
            except UnicodeError:
                logging.warning(f"File {file_path} does not appear to be UTF-16 LE encoded")
                return False
        
        if os.path.exists(base_file):
            check_encoding(base_file)
        if os.path.exists(update_file):
            check_encoding(update_file)
        
        if not os.path.exists(base_file):
            logging.warning(f"Base file {base_file} does not exist. Creating new file.")
            if not os.path.exists(update_file):
                logging.error(f"Update file {update_file} does not exist.")
                return None
                
            update_df = pd.read_csv(update_file, encoding='utf-16le', sep=';', engine='python')
            merged_df = update_df
        else:
            base_df = pd.read_csv(base_file, encoding='utf-16le', sep=';', engine='python')
            
            if not os.path.exists(update_file):
                logging.error(f"Update file {update_file} does not exist.")
                return None
            
            update_df = pd.read_csv(update_file, encoding='utf-16le', sep=';', engine='python')
            update_df_without_header = update_df.iloc[1:] if len(update_df) > 1 else update_df.iloc[0:0]
            merged_df = pd.concat([base_df, update_df_without_header], ignore_index=True)
        
        if output_file is None:
            output_file = base_file
        
        # Write the BOM explicitly
        with open(output_file, 'wb') as f:
            f.write(codecs.BOM_UTF16_LE)
            merged_df.to_csv(f, index=False, sep=';', encoding='utf-16le')
        
        logging.info(f"Files merged successfully. Total records: {len(merged_df)}")
        logging.info(f"Merged file saved to: {output_file}")
        
        logging.info("\nPreview of merged data (first 3 rows):")
        logging.info(merged_df.head(3))
        
        return output_file
    
    except Exception as e:
        logging.error(f"Error merging files: {str(e)}")
        return None

if __name__ == "__main__":
    merge_csv_files()
