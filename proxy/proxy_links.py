import re, sys, argparse, requests, os

body = """
{
  "aggregations": {},
  "from": 0,
  "size": 10000,
  "sort": [{"_score": "desc"}],
  "query": {
    "bool": {
      "must": [],
      "must_not": {
        "terms": {"resourceType": ["service","map","map/static","mapDigital"]}
      },
      "should": [],
      "filter": [
        {"terms": {"isTemplate": ["n"]}},
        {
          "nested": {
            "path": "link",
            "query": {
              "bool":{
                "must_not" : {
                  "bool": {
                    "must": {
                      "term": {
                        "link.protocol": "WWW:LINK-1.0-http--link"
                      }
                    }
                  }
                }
              }
            },
            "inner_hits": {"_source" :  ["{0}"]}
          }
        }
      ]
    }
  },
  "track_total_hits": true,
  "_source": ""
}
"""


def apply_template(value: str, template: str):
    return (template
            .replace('DOMAIN_TPL', value.split(".")[0])
            .replace('EXTENSION_TPL', value.split(".")[1]))

def get_domain(domain_pattern: re.Pattern[str], url: str):
    if domain_pattern.search(url):
        return domain_pattern.findall(url)[0]
    return None

def write_file(template: str, domains: list[str]):
    with open(template, 'r') as f:
        template_content = f.read()
    file_name = template.replace('.tpl', '')
    with open(file_name + '_results.txt', 'w') as wf:
        for domain in domains:
            wf.write(apply_template(domain, template_content))

def getDomains(gn_url: str, write_response: bool, cookie: str = '', gn_version: str = '4.2.5+'):
    headers = {'Content-Type': 'application/json', "accept": "application/json"}
    print(cookie)
    if cookie:
        headers['Cookie'] = cookie
    es_obj = 'link.urlObject.default'
    if gn_version != '4.2.5+':
        es_obj = 'link.url'

    res = requests.post(gn_url + '/srv/api/search/records/_search?bucket=bucket', data=body.replace('{0}', es_obj), headers=headers)

    if write_response:
        with open('body_response.json', 'w') as wf:
            wf.write(str(res.json()))

    content = str(res.json())
    url_pattern = re.compile(r'default[\s:\']*https?://([^/"\']*)')
    if gn_version != '4.2.5+':
        url_pattern = re.compile(r'url[\s:\']*https?://([^/"\']*)')
    domain_pattern = re.compile(r'([^\.]+\.[a-z]+)[:\d]*$')
    urls = set(list(filter(None, url_pattern.findall(content))))
    return sorted(set(filter(None, [get_domain(domain_pattern, url) for url in urls])))

def main():
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('-u', '-url', '--gn-url', type=str, help='URL to search for e.g. https://dev.georchestra.org/geonetwork', required=True)
    parser.add_argument('-t', '--tpl', type=str, help='Custom output template, must contain DOMAIN_TPL and EXTENSION_TPL string inside, Default, all .tpl files in templates/', default=None)
    parser.add_argument('-wr', '--write-response', type=bool, help='Write response in file', default=False, const=True, nargs='?')
    parser.add_argument('--gn-version', type=str, help='Gn Version : possible values 4- or 4.2.5+', default='4.2.5+')
    parser.add_argument('-c', '-cookie', '--auth-cookie', type=str, help='Geonetwork auth cookie', default='')
    args = parser.parse_args()

    domains = getDomains(args.gn_url, args.write_response, args.auth_cookie, args.gn_version)

    if args.tpl is not None:
        write_file(args.tpl, domains)
    else:
        for x in os.listdir('templates/'):
            if x.endswith(".tpl"):
                write_file('templates/' + x, domains)

    print('Done with', domains.__len__(), 'unique domains')

if __name__ == '__main__':
    sys.exit(main())




