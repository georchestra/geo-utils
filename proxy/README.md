# Link Extractor

This is a simple tool to extract all the links in records from a Geonetwork and retrieve domain name.

## Usage
    
```bash
python proxy-links.py -t my_template -u gn_url -wr -c 'JSESSIONID=node019...node0;' --gn-version 4-
```

## Options

- `-u` or `-url` or `--gn-url'`: Geonetwork URL. Mandatory
- `-t` or `--template`: Template name to use. Default is every .tpl file under templates/ folder.
- `-wr` or `--write-response`: Saves the json body response from ES into `body_response.json` file. Use for debugging purposes.
- `--gn_version`: Geonetwork version. Default is 4.2.5+. If prior to this version, use `4-`.
- `-c` or `-cookie` or `--auth-cookie`: Geonetwork auth cookie. Default is empty. Must contains the JSESSIONID (can be retrieved on the instance directly).

:rotating_light: For mapstore template, remove the first comma  in the result file.
