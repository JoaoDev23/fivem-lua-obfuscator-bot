# Lua FiveM Obfuscator Discord Bot

This repository contains an **old Lua obfuscator project** that I created 2023 ago for **FiveM servers**.

The project is a **Discord bot** that allows users to upload a `.lua` file.  
The bot downloads the file, obfuscates the code and sends the obfuscated version back to the user through **Discord DMs**.

The main goal at the time was to make it **harder to read or copy server scripts** by applying a basic layer of obfuscation.

---

# Important Notice

This project is **very old and extremely basic** compared to modern obfuscation methods.

The protection used here is **not secure anymore** and should **NOT be relied on for real script protection**.

Now that the source code is public, it is very likely that people can:

- create **deobfuscators**
- analyze how the loader works
- reverse the protection easily

Because of that, **this repository is shared only for archival and educational purposes**.

---

# Features

- Discord bot built with **Discordia**
- Accepts `.lua` files as attachments
- Simple **XOR-based obfuscation**
- Random identifier generation
- Runtime loader that decrypts the script

---

# Technologies Used

- **Lua**
- **Luvit**
- **Discordia**
- **coro-http**

---

# Why This Is Public

This project is being made public because:

- I am **no longer active in the FiveM market**
- The obfuscator itself is **very outdated**
- It may still be interesting for **learning or historical purposes**

Instead of letting the code sit unused, I decided to **publish it as part of my old projects archive**.

---

# Recommendation

If you are looking for real script protection, this project **is not suitable for production use**.



# License

Released for **educational and archival purposes only**.
