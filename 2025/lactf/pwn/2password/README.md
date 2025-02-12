# 2password

This was an easy format string leak challenge, where the flag is stored in the stack. We have to use format strings like `%<idx>$p` to leak the flag from memory and hex decrypt it to get plain string flag.