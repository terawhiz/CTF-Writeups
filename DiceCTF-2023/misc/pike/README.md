# pike

We were given a [Dockerfile](./Dockerfile) and [server.py](). The server uses python RPC library rpyc to deliver remote procedure calls to clients.

As always checking the newest version of rpyc module, it is 5.3.0 (as of the day challenge was released). There was a bug ([CVE-2019-16328](https://nvd.nist.gov/vuln/detail/CVE-2019-16328)) patched in 4.1.2 which affects 4.1.x

After a bit of googling we can find this github [security advisory](https://github.com/advisories/GHSA-pj4g-4488-wmxm) where a Poc script is attached. No shame, just copy the poc, remove the unit tests code then simply execute it. It works.:)

[Link](./hack.py) to exploit
