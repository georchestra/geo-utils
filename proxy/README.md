# Link Extractor

This is a simple tool to extract all the links in records from a Geonetwork and retrieve domain name.

## Usage
    
```bash
python proxy-links.py -t my_template -g gn_url -wr
```

## Options

- `-u` or `-url` or `--gn-url'`: Geonetwork URL. Mandatory
- `-t` or `--template`: Template name to use. Default is every .tpl file under templates/ folder.
- `-wr` or `--write-response`: Saves the json body response from ES into `body_response.json` file. Use for debugging purposes.

