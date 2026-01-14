# IPO BULKCHECK

This program can be used to check bulk IPO allotments using PAN cards.  
Currently there is only one registrar (**kfintech**) more will be added in future.

---

## Steps to Follow

---

### **Step 1: Clone the repository**

```bash
git clone https://github.com/VishalYadavGit/IPO_BULKCHECK/
```

---

### **Step 2: Install the dependencies**

```bash
pip install -r requirements.txt
```

---

### **Step 3: Create and rename the `.env.example` file or edit the details in config file**

<img width="887" height="68" alt="image" src="https://github.com/user-attachments/assets/37cf2650-3866-4d7f-b9c5-13fe34382b6e" />

> **Note:**  
> If you are editing the config file the `IPO_NAME` should be a string and `PAN_NUMBER` should be a list of strings.

---

### **Step 4: Run the program**

```bash
python kfintech.py
```

---

### **Step 5: Output**

A file named **`allotment_results.svg`** will be generate which will be a table showing all the allotment details.

<img width="1010" height="285" alt="image" src="https://github.com/user-attachments/assets/e55447f1-5f5b-401f-ba73-225aa137ed52" />



