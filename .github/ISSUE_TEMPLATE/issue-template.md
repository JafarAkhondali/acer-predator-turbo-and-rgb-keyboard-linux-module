---
name: Issue template
about: Describe this issue template's purpose here.
title: ''
labels: ''
assignees: ''

---
## Is this an issue or a reproduction result?  ✔️ OR ⁉️
## Please fill in the template 
|Feature|Value|
|---	|---	|
|Model|```sudo dmidecode \| grep "Product Name" -B 2 -A 4```|
|Number of CPU Fans| ? |
|Number of GPU Fans| ? |
|Number of RGB Zones| 1\3\4\PerKeyRGB\Other(Please specify)|
|RGB keyboard works?|  Yes\No |
|Turbo button turns on fans?| Yes\No |
|Turbo button turn on LED?| Yes\No |
|Turbo button activates overclock?| Yes\No |
|Distribution Specific Information|`lsb_release -a`|
|Kernel Version|`uname -a`|

If the turbo button is not working, what is the output of the command below when you press the turbo key?  
```bash sudo dmesg | grep "Unknown function number"```
