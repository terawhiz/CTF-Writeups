import io
import torch
import base64

banner = \
'''
8""8""8                   8""""8                                      
8  8  8 eeee eeeeeee eeee 8    " eeeee eeeee eeeee eeeee  eeeee e     
8e 8  8 8    8  8  8 8    8e     8  88 8   8   8   8   8  8  88 8     
88 8  8 8eee 8e 8  8 8eee 88     8   8 8e  8   8e  8eee8e 8   8 8e    
88 8  8 88   88 8  8 88   88   e 8   8 88  8   88  88   8 8   8 88    
88 8  8 88ee 88 8  8 88ee 88eee8 8eee8 88  8   88  88   8 8eee8 88eee 
'''

try: 
    print(banner)
    base64_string = input("Send the base64 encoded model: ")
    bytes_data = base64.b64decode(base64_string)

    print("Evaluating the model ...")
    device = torch.device("cpu")
    model = torch.load(io.BytesIO(bytes_data), map_location=device)
    model.eval()
    print("Finished evaluating the model!")
except Exception as e:
    print(f"Ooops, this model is no good: {e}".format(e))