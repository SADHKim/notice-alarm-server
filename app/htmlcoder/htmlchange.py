htmlEncode = {
    '"' : "&#34;",
    "'" : "&#39;",
    '<' : "&#60;",
    '>' : "&#62;",
}

htmlDecode = {
    "&#34;" : '"',
    "&#39;" : "'",
    "&#60;" : '>',
    "&#62;" : '>'
}

def html_encode(content):
    for key in htmlEncode.keys():
        content = content.replace(key, htmlEncode[key])
        
    return content

def html_decode(content):
    for key in htmlDecode.keys():
        content = content.replace(key, htmlDecode[key])
        
    return content
    