<body style="
    background-color: #1D1E2D; padding: 4rem; color:#9FA1B9;
    font-family: Montserrat-Regular,sans-serif;
    font-style: normal;
    font-weight: 300;">
<div align="center">
  <div style="background-color: #ffc0c0; color: black; padding: 1rem; border-radius: 1rem;">
   <h1 style="padding: 0;">Disclaimer:</h1>
   <p style="color: black">
      Official Adamnite has beed discontinued recently. So I publish my current implementation
      of my work performed for Adamnite. This project will be continued as my private
      Project.
   </p>
  </div>
  <h3 align="center">PyAdamnite</h3>
   <p align="center">
      Adamnite's implementation in Python
   </p>
</div>

## About The Project

Adamnite is a new-generation layer-1 blockchain development platform serving to 
increase blockchain adoption. By providing a development platform that enables 
developers to easily build safe and efficient decentralized applications 
(dApps), Adamnite hopes to be at the center of both dApp development and 
blockchain innovation. Adamnite’s core philosophy is centered around ease of 
use, scalability, and security. Its primary focus is on solving two main 
problems in the space: a lack of proper security tools for smart contract 
developers, and a lack of widespread use of blockchain technology in both 
public and private sectors. While these problems are well-known, we believe 
that there are specific issues with current platforms that significantly 
increase the likelihood of exploits happening in dApps and hinder adoption.
<p align="right">(<a href="#top">back to top</a>)</p>

## Getting Started

### Prerequisites

* python 3.9

### Installation

This Project is currently developed as a private Repo. If you want to clone and 
work on the Repo you need have given acces by the Adamnite Team.
1. Authenticate yourself with GitHub over SSH!
[How to add my SSH Key to GitHub](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/adding-a-new-ssh-key-to-your-github-account) 
2. Clone the repo over SSH
    ```sh
        git clone git@github.com:Adamnite/PyAdamnite.git
      ```
3. Get inside the new created Folder
   ```sh
    cd PyAdamnite
   ```
4. Install Python Dependency's. Preferably into an venv! [How to create a venv in Python](https://docs.python.org/3/library/venv.html)
   ```sh
   pip install -r requirements.txt
   ```
<p align="right">(<a href="#top">back to top</a>)</p>

## Usage

### Start Software

```sh
cd src
python main.py
```
You will be greeted with an CLI interface running on your Terminal.

![cli_client.png](/doc/cli_client.png)

### Send a Transaction
1. Press 1 + Enter
2. Type in the amount and press Enter
3. Type in the receiver address or copy and paste it and type Enter
4. If everything is fine press 1 or abord with 9 and confirm with Enter

## Tests
### Run all tests

```sh
cd src
python main_tests.py
```

### Run one by one

```sh
python -m unittest tests/test_flask.py
python -m unittest tests/test_tree.py
python -m unittest tests/TEST_FILE.py
```

## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#top">back to top</a>)</p>

## Contact

- [Discord](https://discord.gg/A75DHMzU)
- [Twiter](https://twitter.com/adamnitehq)
- [Reddit](https://www.reddit.com/r/AdamniteHq/)

Github Organisation: [https://github.com/Adamnite](https://github.com/Adamnite)

<p align="right">(<a href="#top">back to top</a>)</p>
</body>
