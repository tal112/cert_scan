import sys
import os
import subprocess
import pandas as pd

def get_ciphers(version, data, length, data_dict):
   
    print("Fetching cipers for version {}".format(version))
    
    if length >= 0:
        section = data[length:]
        ciphers_index = section.find("ciphers")
        compressors_index = section.find("compressors")
        section_array = section[ciphers_index:compressors_index].split("\\n")
        section_array.pop(0)

        for cipher in section_array:
            cipher = cipher.replace("|       ", "")
            cipher_array = cipher.split("-")
            if len(cipher_array) >= 2:
                data_dict["Certificate"].append(version)
                data_dict["Cipher"].append(cipher_array[0])
                data_dict["Score"].append(cipher_array[1])

    return data_dict



print("#"*90)
print("     Author: Tal Sperling")
print("     This code is to be used for educational purposes or legal penetration testing only")
print("     I do not take responsibility for any misuse or illegal action/use of this code")
print("#"*90+"\n")

print("")
print("")

try:
    data = {"Certificate":[], "Cipher":[], "Score":[]}

    x = subprocess.check_output(['whoami'])
    print("Scanning {}".format(sys.argv[1]))
    command = "nmap -sV --script ssl-enum-ciphers -p 443 {}".format(sys.argv[1])
    result = subprocess.run([command], shell=True, capture_output=True, text=True)
    #os.system("nmap -sV --script ssl-enum-ciphers -p 443 {}".format(sys.argv[1]))
    result_str = str(result)
   
    tls10 = result_str.find("TLSv1.0")
    tls11 = result_str.find("TLSv1.1")
    tls12 = result_str.find("TLSv1.2")
    tls13 = result_str.find("TLSv1.3")
    
    #get_ciphers("tls1.0", result_str, tls10)

    data = get_ciphers("tls1.0", result_str,  tls10, data)
    data = get_ciphers("tls1.1", result_str,  tls11, data)
    data = get_ciphers("tls1.2", result_str,  tls12, data)
    data = get_ciphers("tls1.3", result_str,  tls13, data)
    
    print("")
    print("Scan complete")
    print("************")
    print("")
    
    dataDf = pd.DataFrame(data)
    print(dataDf)
except Exception as e:
    print("Scan failed")
    print(e)
