import argparse
import os
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


def get_fileNames(filePath):
    """
    Extract a list of .csv file names from fluorescence data folder.
    :param filePath: path to .csv file folder.
    :return: list of file names.
    """ 
    fileList = os.listdir(filePath)
    fileNames = sorted([file for file in fileList if file.endswith('.csv')])
    
    return fileNames

def get_XYZ(filePath, fileName):
    """
    Read fluorescence file into a Pandas DataFrame. Returns arrays of x,y coordinates along contour data.
    :param filePath: path to .csv file folder.
    :param fileName: file name.
    :return: X,Y coordinate arrays and Z contour array. 
    """
    # Import data into Dataframe and transpose so that excitation data (x-axis) is arranged in to columns
    # and emission data (y-axis) is arranged into rows.
    Z = pd.read_csv(os.path.join(filePath, fileName), header=0, index_col=0).T
    
    # Set x- and y-axis values
    x = Z.columns
    y = Z.index.astype(int)
    # Set X and Y (2D arrays of the x and y points)
    X, Y = np.meshgrid(x, y)
    #print(X.shape, Y.shape)
    
    return X, Y, Z

def plot_contour(X, Y, Z, filePath, fileName, outFormat='png'):
    """
    Plot excitation and emission data and saves as .png file.
    :param X: x points array
    :param Y: y points array
    :param Z: contour array for X and Y
    :param filePath: path to CD file folder.
    :param fileName: file name.
    :outFormat: output file extension (.png, .svg, .pdf). Default is .png.
    :return: None
    """
    hfont = {'fontname':'Arial'}

    fig, ax = plt.subplots(1, 1)
    cs = ax.contourf(X, Y, Z, 100, cmap='jet')
    
    plt.rcParams.update({'font.size': 18})
    #ax.set_title(os.path.basename(f'{fileName[:-4]}'), **hfont)
    ax.set_xlabel('Emission Wavelength (nm)', **hfont) 
    ax.set_ylabel('Excitation Wavelength (nm)', **hfont)

    plt.xticks(**hfont)
    plt.yticks(**hfont)
    
    plt.tight_layout()
    
    # Configure colorbar scale between 0 and maximum 
    maxZ = round(max(Z.max()), -2) # max intensity value
    cbar = fig.colorbar(cs, spacing = 'proportional')
    cbar.set_ticks(np.arange(0, maxZ+1, maxZ/5))
    
    outfile = os.path.join(filePath, fileName[:-4])
    fig.savefig(f'{outfile}.{outFormat}', dpi=300, bbox_inches='tight', transparent=True)
    
    return

def main():
    parser = argparse.ArgumentParser(description='This script accepts a file path to a folder containing .csv files of emission-excitation data and outputs the corresponding contour plots in .png or .svg format.')
    parser.add_argument('file_path', help='File path to the .csv file folder.')
    parser.add_argument('save_as', help='Output file type. Choose between .png or .svg.', type=str, default='png')
    
    args = parser.parse_args()
    
    filePath = args.file_path
    outFormat = args.save_as
    fileNames = get_fileNames(filePath)
    print(f'There are {len(fileNames)} files to parse.\nFile list = {fileNames}')

    count = 0
    for file in fileNames:
        try:
            X, Y, Z = get_XYZ(filePath, file)
            plot_contour(X, Y, Z, filePath, file, outFormat)
            count += 1
        except:
            print(f'Failed to plot {file}.')
            continue
            
    print(f'Succesfully plotted {count}/{len(fileNames)} files.')  

if __name__ == "__main__":
    main()