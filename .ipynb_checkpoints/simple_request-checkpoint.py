# encoding: utf-8

import requests
import argparse

URL = 'http://127.0.0.1:5000/predict'


def predict_result(image_path):
    # Initialize image path
    image = open(image_path, 'rb').read()
    payload = {'image': image}
    output_string=''
    r = requests.post(URL, files=payload).json()

    # Ensure the request was successful.
    if r['success']:
        # Loop over the predictions and display them.
        #print(image_path,end ="\t")
        output_string=output_string+image_path +'\t'
        
        for (i, result) in enumerate(r['predictions']):
            #print(' {}: {:.4f}'.format(result['label'],result['probability']),end ="\t")
            output_string=output_string+'{}'.format(result['label'])+'\t' +'{:.4f}'.format(result['probability'])+'\t'
    
        
        #print(output_string)
    # Otherwise, the request failed.
    else:
        print('Request failed')
    
    return output_string


if __name__ == '__main__':
    #parser = argparse.ArgumentParser(description='Classification')
    #parser.add_argument('--file', type=str, help='image file')

    #args = parser.parse_args()
    #string = predict_result(args.file)
    
    mypath='../dataset/'
    from os import listdir
    from os.path import isfile, join
    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    #print(onlyfiles)
    
    output_all=''
    for x in onlyfiles:
        string = predict_result(mypath+x)
        output_all=output_all+string+ '\n'
    
    print(output_all)

    text_file = open("Output.txt", "w")
    text_file.write(output_all)
    text_file.close()