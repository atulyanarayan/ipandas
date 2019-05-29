# ipandas
Enhanced pandas intelligence

Added functions to default pandas functionality:
  1. read_data(filename): automatically detects correct full name of the file using regex match and the required file type, if file is in the current working directory
  > Example: jan = read_data('jan') will automatically read the file named 'ParisJanData.xlsx' and return as a pandas dataframe, while printing the complete file name, top 5 rows of the data and the actual dimensions of the read dataframe.
  2. converttxt(): automatically detects all the txt files present in the current working directory and converts to xlsx.

