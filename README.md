# X9
X9 is a featured URL maker that helps identify potentially vulnerable parameters in web applications.
## Installation
```console
git clone https://github.com/Q0120S/X9.git
cd X9
python3 x9.py -h
```
You can add this tool to your bashrc for ease of use:
```bash
x9() {                  
python3 /path/to/your/tool/x9.py "$@"
}
```
## Usage
```bash
python3 x9.py -h
```
This will display help for the tool. Here are all the switches it supports.
```console
usage: x9.py [-h] [-l LIST] [-p PARAMETERS] [-c CHUNK] [-v VALUE] -gs {normal,ignore,combine,all} -vs {replace,suffix} [-s] [-o OUTPUT]

X9

options:
  -h, --help            show this help message and exit
  -l LIST, --list LIST  List of urls to edit.
  -p PARAMETERS, --parameters PARAMETERS
                        Parameters wordlist to fuzz.
  -c CHUNK, --chunk CHUNK
                        Chunk to fuzz the parameters. [default: 15]
  -v VALUE, --value VALUE
                        Value for parameters to FUZZ. [default: "<b/NOOBI,"NOOBI",'NOOBI']
  -gs {normal,ignore,combine,all}, --generate-strategy {normal,ignore,combine,all}
                        Select the mode strategy from the available choices:
                                normal: Remove all parameters and put the worlist
                                combine: Pitchfork combine on the existing parameters
                                ignore: Don't touch the URL and put the wordlist
                                all: All in one method
  -vs {replace,suffix}, --value-strategy {replace,suffix}
                        Select the mode strategy from the available choices:
                                replace: Replace the value with gathered value
                                suffix: Append the value to the end of the parameters
  -s, --silent          Silent mode
  -o OUTPUT, --output OUTPUT
                        Output results
```
It has two main features: **generate strategy**, **value strategy**:
### Generate Strategy
Modes:
* normal: It removes all the parameters from the input url and then puts the parameters from the given parameters wordlist in the url.
* combine: It uses the pitchfork method to make a combination of default parameters(key, value) and given parameters(key, value).
* ignore: It doesn't manipulate or remove any parameters of the url and just appends the new parameters and values to the url.
* all: It merges the results of ignore and combine modes.
### Value Strategy
Modes:
* replace: It replaces the parameter's value with the given value.
* suffix: It appends the given value to the end of each parameter's value.
## Running X9
```bash
python3 x9.py -l urls.txt -c 25 -s -p top25-xss.txt -v "'NOOBI'" -gs normal -vs suffix
```
```bash
cat urls.txt | python3 x9.py -c 40 -s -v "<b/NOOBI" -gs combine -vs replace
```
### Output:
```console
https://example.com/path1/?param1=%3Cb%2FNOOBI&param2=value2
https://example.com/path1/?param1=value1&param2=%3Cb%2FNOOBI
https://example.com/path1/?param1=%22NOOBI%22&param2=value2
https://example.com/path1/?param1=value1&param2=%22NOOBI%22
https://example.com/path1/?param1=%27NOOBI%27&param2=value2
https://example.com/path1/?param1=value1&param2=%27NOOBI%27
https://example.com/pathx/file.php?param3=%3Cb%2FNOOBI&param4=value4
https://example.com/pathx/file.php?param3=value3&param4=%3Cb%2FNOOBI
https://example.com/pathx/file.php?param3=%22NOOBI%22&param4=value4
https://example.com/pathx/file.php?param3=value3&param4=%22NOOBI%22
https://example.com/pathx/file.php?param3=%27NOOBI%27&param4=value4
https://example.com/pathx/file.php?param3=value3&param4=%27NOOBI%27
```
## Advance usage
You can merge x9 with other tools:
```bash
cat urls.txt | python3 x9.py -c 40 -s -p top25-xss.txt -gs all -vs replace | nuclei -t templates/parameter-discovery-html.yaml -silent
```
### Result:
```console
[parameter-discovery] [http] [Info] https://example.com/path1/?param1=%3Cb%2FNOOBI&param2=value2&q=%3Cb%2FNOOBI&s=%3Cb%2FNOOBI&search=%3Cb%2FNOOBI&id=%3Cb%2FNOOBI&lang=%3Cb%2FNOOBI&keyword=%3Cb%2FNOOBI&query=%3Cb%2FNOOBI&page=%3Cb%2FNOOBI&keywords=%3Cb%2FNOOBI&year=%3Cb%2FNOOBI&view=%3Cb%2FNOOBI&email=%3Cb%2FNOOBI&type=%3Cb%2FNOOBI&name=%3Cb%2FNOOBI&p=%3Cb%2FNOOBI&month=%3Cb%2FNOOBI&image=%3Cb%2FNOOBI&list_type=%3Cb%2FNOOBI&url=%3Cb%2FNOOBI&terms=%3Cb%2FNOOBI&categoryid=%3Cb%2FNOOBI&key=%3Cb%2FNOOBI&login=%3Cb%2FNOOBI&begindate=%3Cb%2FNOOBI&enddate=%3Cb%2FNOOBI
[parameter-discovery] [http] [Info] https://example.com/pathx/file.php?param3=value3&param4=value4&q=%22NOOBI%22&s=%22NOOBI%22&search=%22NOOBI%22&id=%22NOOBI%22&lang=%22NOOBI%22&keyword=%22NOOBI%22&query=%22NOOBI%22&page=%22NOOBI%22&keywords=%22NOOBI%22&year=%22NOOBI%22&view=%22NOOBI%22&email=%22NOOBI%22&type=%22NOOBI%22&name=%22NOOBI%22&p=%22NOOBI%22&month=%22NOOBI%22&image=%22NOOBI%22&list_type=%22NOOBI%22&url=%22NOOBI%22&terms=%22NOOBI%22&categoryid=%22NOOBI%22&key=%22NOOBI%22&login=%22NOOBI%22&begindate=%22NOOBI%22&enddate=%22NOOBI%22
```
