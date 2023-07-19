import argparse
import sys
from urllib.parse import urlencode, urlparse, urlunparse, parse_qs ,parse_qsl

# Pervent duplicates in results
def append_if_not_exists(my_list, item):
    if item not in my_list:
        my_list.append(item)
        
# Generate Strategy
def normal_generatation_strategy(base_url,value,max_params_per_url,params_list):
    parsed_url = urlparse(base_url)
    url_parameters_removed = urlunparse(parsed_url._replace(query=''))
    urls = []
    num_urls = (len(params_list) + max_params_per_url - 1)
    
    for i in range(num_urls):
        start_idx = i * max_params_per_url
        end_idx = (i + 1) * max_params_per_url
        url_params = ""
        for param in params_list[start_idx:end_idx]:
            url_params += f"{param}={value}&"

        url = f"{url_parameters_removed}?{url_params.rstrip('&')}"
        urls.append(url)
        if end_idx > len(params_list):
            break

    return urls

def combine_generatation_strategy(base_url,value,max_params_per_url,params_list):
    final_urls = []
    max_params_per_url -= len(list(parse_qs(urlparse(base_url).query).keys()))
    num_urls = (len(params_list) + max_params_per_url - 1)
    parsed_url = urlparse(base_url)
    params = parse_qs(parsed_url.query)
    # Generate the list of parameter names
    param_names = list(params.keys())

    # Generate URLs with different parameter values
    for i in range(len(param_names)):
        new_params = params.copy()
        new_params[param_names[i]] = [value]
        new_query = urlencode(new_params, doseq=True)
        new_url = urlunparse((parsed_url.scheme, parsed_url.netloc, parsed_url.path, '', new_query, ''))
        final_urls.append(new_url)
        # same_value_params = {param: value for param in param_names}

    # same_value_query = urlencode(same_value_params, doseq=True)
    # same_value_url = urlunparse((parsed_url.scheme, parsed_url.netloc, parsed_url.path, '', same_value_query, ''))
    # final_urls.append(same_value_url)
    urls = final_urls.copy()
    if params_list:
        urls = []
        for final_url in final_urls:
            for i in range(num_urls):
                start_idx = i * max_params_per_url
                end_idx = (i + 1) * max_params_per_url
                url_params = ""
                for param in params_list[start_idx:end_idx]:
                    url_params += f"{param}={value}&"
                test_url = f"{final_url}&{url_params.rstrip('&')}"
                urls.append(test_url)
                if end_idx > len(params_list):
                    break

    return urls

def ignore_generatation_strategy(base_url,value,max_params_per_url,params_list):
    urls = []
    max_params_per_url -= len(list(parse_qs(urlparse(base_url).query).keys()))
    num_urls = (len(params_list) + max_params_per_url - 1)

    parsed_url = urlparse(base_url)
    params = parse_qs(parsed_url.query)
    param_values_list = []
    for i in list(params.values()):
        for j in i:
            j = value
            append_if_not_exists(param_values_list, j)

    # Generate the list of parameter names
    param_names = list(params.keys())
    # Generate URLs with different same parameters values
    for i in range(len(param_names)):
        new_params = params.copy()
        new_params[param_names[i]] = [value]
        new_query = urlencode(new_params, doseq=True)
        new_url = urlunparse((parsed_url.scheme, parsed_url.netloc, parsed_url.path, '', new_query, ''))
        new_parsed_url = urlparse(new_url)
        query_params = parse_qs(new_parsed_url.query)

        for key in query_params:
            query_params[key] = [value]
        updated_query_string = urlencode(query_params, doseq=True)
        updated_url = urlunparse(parsed_url._replace(query=updated_query_string))
        append_if_not_exists(urls, updated_url)

    if params_list:
        urls = []
        for i in range(num_urls):
            start_idx = i * max_params_per_url
            end_idx = (i + 1) * max_params_per_url
            url_params = ""
            for param in params_list[start_idx:end_idx]:
                url_params += f"{param}={value}&"
            if not urlparse(base_url).query:
                url = f"{base_url}?{url_params.rstrip('&')}"
            else:
                url = f"{base_url}&{url_params.rstrip('&')}"
            urls.append(url)
            if end_idx > len(params_list):
                break

    return urls


# Value Strategy
def replace_value_strategy(base_url,value):
    # Generate the list of parameter values
    manipulated_values = []
    parsed_url = urlparse(base_url)
    params = parse_qs(parsed_url.query)
    param_values_list = list(params.values())

    if not param_values_list:
        manipulated_values.append(value)
    else:
        for param_value in param_values_list:
            for i in param_value:
                i = value
                manipulated_values.append(i)

    return manipulated_values

def suffix_value_strategy(base_url,value):
    # Generate the list of parameter values
    manipulated_values = []
    parsed_url = urlparse(base_url)
    params = parse_qs(parsed_url.query)
    param_values_list = list(params.values())

    if not param_values_list:
        append_if_not_exists(manipulated_values, value)
    else:
        for param_value in param_values_list:
            for i in param_value:
                i += value
                append_if_not_exists(manipulated_values, i)

    return manipulated_values

BANNER ='''                

    ██╗  ██╗ █████╗
    ╚██╗██╔╝██╔══██╗
     ╚███╔╝ ╚██████║
     ██╔██╗  ╚═══██║
    ██╔╝ ██╗ █████╔╝
    ╚═╝  ╚═╝ ╚════╝
                     NoobHunter
'''

default_values = "<b/NOOBI,\"NOOBI\",'NOOBI'"

def main():
    parser = argparse.ArgumentParser(description="X9", formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("-l", "--list", help="List of urls to edit.")
    parser.add_argument("-p", "--parameters", required=False, default=None, help="Parameters wordlist to fuzz.")
    parser.add_argument("-c", "--chunk", type=int, default=15, help="Chunk to fuzz the parameters. [default: 15]")
    parser.add_argument("-v", "--value", default=default_values, help="Value for parameters to FUZZ. [default: \"<b/NOOBI,\"NOOBI\",'NOOBI']")
    parser.add_argument("-vL", "--value-list", help="Value list for parameters to FUZZ.")
    parser.add_argument("-gs", "--generate-strategy", required=True, type=str, choices=["normal", "ignore", "combine", "all"], help="""Select the mode strategy from the available choices:
        normal: Remove all parameters and put the worlist
        combine: Pitchfork combine on the existing parameters
        ignore: Don't touch the URL and put the wordlist
        all: All in one method""")
    parser.add_argument("-vs", "--value-strategy", required=True, type=str, choices=["replace", "suffix"],
                        help="""Select the mode strategy from the available choices:
        replace: Replace the value with gathered value
        suffix: Append the value to the end of the parameters""")
    parser.add_argument("-s", "--silent", help="Silent mode", action="store_true")
    parser.add_argument("-o", "--output", help="Output results")
    args = parser.parse_args()

    # Read URLs from file
    if args.list:
        temp_urls = []
        with open(args.list, 'r') as file:
            unknown_urls = [line.strip() for line in file]
            for url in unknown_urls:
                parsed_url = urlparse(url)
                path = parsed_url.path

                if path == '' or path[-1] != '/':
                    # Check if the URL ends with a TLD (e.g., '.com', '.org', etc.)
                    if '.' in parsed_url.netloc:
                        tld = parsed_url.netloc.split('.')[-1]
                        if not tld.isdigit():  # Avoid matching IP addresses
                            path += '/'
                fine_url = urlunparse(parsed_url._replace(path=path))
                append_if_not_exists(temp_urls, fine_url)

    elif not sys.stdin.isatty():
        temp_urls = []
        unknown_urls = []
        for line in sys.stdin:
            unknown_urls.append(line.strip())
        for url in unknown_urls:
            parsed_url = urlparse(url)
            path = parsed_url.path

            if path == '' or path[-1] != '/':
                # Check if the URL ends with a TLD (e.g., '.com', '.org', etc.)
                if '.' in parsed_url.netloc:
                    tld = parsed_url.netloc.split('.')[-1]
                    if not tld.isdigit():  # Avoid matching IP addresses
                        path += '/'
            fine_url = urlunparse(parsed_url._replace(path=path))
            append_if_not_exists(temp_urls, fine_url)

    else:
        print("Please provide the urls list")
        sys.exit(1)

    # Read parameters from file if provided
    if args.parameters:
        with open(args.parameters, 'r') as file:
            params = [line.strip() for line in file]
    else:
        params = []
    
    # Process the results as a single string instead of a list
    all_permutations = []

    if args.value_list:
        with open(args.value_list, 'r') as file:
            values = [line.strip() for line in file]
    else:
        values = args.value.split(',')

    for url in temp_urls:
        if args.value_strategy == "replace":
            replaced_values = []
            for value in values:
                replace_strategy = replace_value_strategy(url,value)
                for result in replace_strategy:
                    append_if_not_exists(replaced_values, result)
            for value in replaced_values:
                if args.generate_strategy == "normal":
                    if not args.parameters:
                        print("For normal mode you should provide parameters wordlist")
                        sys.exit(1)

                    normal_strategy = normal_generatation_strategy(url,value,args.chunk,params)
                    for result in normal_strategy:
                        parsed_url = urlparse(result)
                        encoded_query = urlencode(dict(parse_qsl(parsed_url.query)))
                        encoded_url = urlunparse(parsed_url._replace(query=encoded_query))
                        append_if_not_exists(all_permutations, encoded_url)
                        
                elif args.generate_strategy == "combine":
                    combine_strategy = combine_generatation_strategy(url,value,args.chunk,params)
                    for result in combine_strategy:
                        parsed_url = urlparse(result)
                        encoded_query = urlencode(dict(parse_qsl(parsed_url.query)))
                        encoded_url = urlunparse(parsed_url._replace(query=encoded_query))
                        append_if_not_exists(all_permutations, encoded_url)

                elif args.generate_strategy == "ignore":
                    ignore_strategy = ignore_generatation_strategy(url,value,args.chunk,params)
                    for result in ignore_strategy:
                        parsed_url = urlparse(result)
                        encoded_query = urlencode(dict(parse_qsl(parsed_url.query)))
                        encoded_url = urlunparse(parsed_url._replace(query=encoded_query))
                        append_if_not_exists(all_permutations, encoded_url)

                elif args.generate_strategy == "all":
                    combine_strategy = combine_generatation_strategy(url,value,args.chunk,params)
                    for result in combine_strategy:
                        parsed_url = urlparse(result)
                        encoded_query = urlencode(dict(parse_qsl(parsed_url.query)))
                        encoded_url = urlunparse(parsed_url._replace(query=encoded_query))
                        append_if_not_exists(all_permutations, encoded_url)

                    ignore_strategy = ignore_generatation_strategy(url,value,args.chunk,params)
                    for result in ignore_strategy:
                        parsed_url = urlparse(result)
                        encoded_query = urlencode(dict(parse_qsl(parsed_url.query)))
                        encoded_url = urlunparse(parsed_url._replace(query=encoded_query))
                        append_if_not_exists(all_permutations, encoded_url)
                        
        elif args.value_strategy == "suffix":
            suffixed_values = []
            for value in values:
                suffix_strategy = suffix_value_strategy(url,value)
                for result in suffix_strategy:
                    append_if_not_exists(suffixed_values, result)

            for value in suffixed_values:
                if args.generate_strategy == "normal":
                    if not args.parameters:
                        print("For normal mode you should provide parameters wordlist")
                        sys.exit(1)

                    normal_strategy = normal_generatation_strategy(url,value,args.chunk,params)
                    for result in normal_strategy:
                        parsed_url = urlparse(result)
                        encoded_query = urlencode(dict(parse_qsl(parsed_url.query)))
                        encoded_url = urlunparse(parsed_url._replace(query=encoded_query))
                        append_if_not_exists(all_permutations, encoded_url)

                elif args.generate_strategy == "combine":
                    combine_strategy = combine_generatation_strategy(url,value,args.chunk,params)
                    for result in combine_strategy:
                        parsed_url = urlparse(result)
                        encoded_query = urlencode(dict(parse_qsl(parsed_url.query)))
                        encoded_url = urlunparse(parsed_url._replace(query=encoded_query))
                        append_if_not_exists(all_permutations, encoded_url)

                elif args.generate_strategy == "ignore":
                    ignore_strategy = ignore_generatation_strategy(url,value,args.chunk,params)
                    for result in ignore_strategy:
                        parsed_url = urlparse(result)
                        encoded_query = urlencode(dict(parse_qsl(parsed_url.query)))
                        encoded_url = urlunparse(parsed_url._replace(query=encoded_query))
                        append_if_not_exists(all_permutations, encoded_url)

                elif args.generate_strategy == "all":
                    combine_strategy = combine_generatation_strategy(url,value,args.chunk,params)
                    for result in combine_strategy:
                        parsed_url = urlparse(result)
                        encoded_query = urlencode(dict(parse_qsl(parsed_url.query)))
                        encoded_url = urlunparse(parsed_url._replace(query=encoded_query))
                        append_if_not_exists(all_permutations, encoded_url)

                    ignore_strategy = ignore_generatation_strategy(url,value,args.chunk,params)
                    for result in ignore_strategy:
                        parsed_url = urlparse(result)
                        encoded_query = urlencode(dict(parse_qsl(parsed_url.query)))
                        encoded_url = urlunparse(parsed_url._replace(query=encoded_query))
                        append_if_not_exists(all_permutations, encoded_url)

    if not args.output and not args.silent:
        print(BANNER)
    
    if args.output:
        output_result = "\n".join(all_permutations)
        with open(args.output, 'w') as output_file:
                output_file.write(output_result)
    else:
        for i in all_permutations:
            print(i)

if __name__ == '__main__':
    main()
