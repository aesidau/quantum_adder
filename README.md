# Quantum Adder
This is some simple Qiskit code to add two two-bit numbers and get a three-bit result, in a way that can be run on a five qubit quantum computer or simulator. The current code adds 2 (0b10) and 3 (0b11) and should get 5 (0b101).

The adder is based on: [Thapliyal, Himanshu & Ranganathan, N. (2013). Design of Efficient Reversible Logic-Based Binary and BCD Adder Circuits. ACM Journal on Emerging Technologies in Computing Systems (JETC). 9. 10.1145/2491682.](https://www.researchgate.net/publication/262163558_Design_of_Efficient_Reversible_Logic-Based_Binary_and_BCD_Adder_Circuits)

## Getting started
To get this running, first install Qiskit
```
% pip3 install qiskit
```
and set up an account on [IBM Quantum](https://quantum-computing.ibm.com/). Also ensure you have [saved your API token](https://quantum-computing.ibm.com/lab/docs/iql/manage/account/ibmq).

## Running the code
There are two version of the code:
1. `add.py` runs the addition in the simulator
2. `addcloud.py` runs the addition in a cloud-based quantum computer (by default, on the five qubit Belem system)
Both of these work the same way, just run it like this:
```
% python3 add.py
           ░                                                                      ░          
q_0: ──────░─────────────■──────────────────────────■──────────────■──────────────░──────────
     ┌───┐ ░           ┌─┴─┐                     ┌──┴───┐┌──────┐  │  ┌────┐      ░          
q_1: ┤ X ├─░───■────■──┤ X ├───■──────────────■──┤ Sxdg ├┤ Sxdg ├──┼──┤ Sx ├──■───░──────────
     ├───┤ ░   │    │  └─┬─┘   │              │  └──────┘└──┬───┘┌─┴─┐└─┬──┘  │   ░ ┌─┐      
q_2: ┤ X ├─░───┼────┼────■─────┼──────────────┼─────────────■────┤ X ├──■─────┼───░─┤M├──────
     ├───┤ ░ ┌─┴─┐  │          │            ┌─┴─┐                └───┘      ┌─┴─┐ ░ └╥┘┌─┐   
q_3: ┤ X ├─░─┤ X ├──┼──────────┼───────■────┤ X ├───■───────────────────────┤ X ├─░──╫─┤M├───
     └───┘ ░ └───┘┌─┴─┐     ┌──┴───┐┌──┴───┐└───┘ ┌─┴──┐                    └───┘ ░  ║ └╥┘┌─┐
q_4: ──────░──────┤ X ├─────┤ Sxdg ├┤ Sxdg ├──────┤ Sx ├──────────────────────────░──╫──╫─┤M├
           ░      └───┘     └──────┘└──────┘      └────┘                          ░  ║  ║ └╥┘
c: 3/════════════════════════════════════════════════════════════════════════════════╩══╩══╩═
                                                                                     0  1  2 
Total counts are: {'101': 1000}
```
You can see that it has run 1000 times, and every time it has come up with the right answer of 2 + 3, i.e. 5 (0b101).

The `addcloud.py` version will take longer to run as it is executing on a real quantum computer somewhere, which might take a while if that quantum computer has a lot of compute jobs queued up. It will also return a range of counts due to the noise inherent in a real quantum computer, so the code will pop up a histogram at the end to make it easier to understand. The histogram from a real quantum computer will look something like this:
![Screenshot of histogram from an actual run of addcloud.py](assets/histogram_example.png)
