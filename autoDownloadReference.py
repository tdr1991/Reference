#coding:utf-8

def find_last(string,str) :
    last_position = -1
    while True:
        position = string.find(str, last_position + 1)
        if position == -1 :
            return last_position
        last_position = position

'''解析pdf文件获取每个参考文献题目'''
def getPDFReferencesTitle() :
    
    import sys
    from pdfminer.pdfdocument import PDFDocument
    from pdfminer.pdfparser import PDFParser
    from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
    from pdfminer.pdfdevice import PDFDevice, TagExtractor
    from pdfminer.pdfpage import PDFPage
    from pdfminer.converter import XMLConverter, HTMLConverter, TextConverter
    from pdfminer.cmapdb import CMapDB
    from pdfminer.layout import LAParams
    from pdfminer.image import ImageWriter
    import re
    import codecs


    # debug option
    debug = 0
    # input option
    password = ''
    pagenos = set()
    maxpages = 0
    srcFile = "E:\\论文\\SNP\\学位论文\\基于Relief和SVM-RFE的组合式SNP特征选择.pdf".decode("utf8").encode("gbk")

    # output option
    outfile = "E:\\论文\\SNP\\学位论文\\基于Relief和SVM-RFE的组合式SNP特征选择.txt".decode("utf8").encode("gbk")
    outtype = None
    imagewriter = None
    rotation = 0
    layoutmode = 'normal'
    codec = 'utf-8'
    pageno = 1
    scale = 1
    caching = True
    showpageno = True
    laparams = LAParams()
    
    #
    PDFDocument.debug = debug
    PDFParser.debug = debug
    CMapDB.debug = debug
    PDFResourceManager.debug = debug
    PDFPageInterpreter.debug = debug
    PDFDevice.debug = debug
    #
    rsrcmgr = PDFResourceManager(caching=caching)
    if not outtype:
        outtype = 'text'
        if outfile:
            if outfile.endswith('.htm') or outfile.endswith('.html'):
                outtype = 'html'
            elif outfile.endswith('.xml'):
                outtype = 'xml'
            elif outfile.endswith('.tag'):
                outtype = 'tag'
    if outfile:
        outfp = file(outfile, 'w')
    else:
        outfp = sys.stdout
    if outtype == 'text':
        device = TextConverter(rsrcmgr, outfp, codec=codec, laparams=laparams,
                               imagewriter=imagewriter)
    elif outtype == 'xml':
        device = XMLConverter(rsrcmgr, outfp, codec=codec, laparams=laparams,
                              imagewriter=imagewriter)
    elif outtype == 'html':
        device = HTMLConverter(rsrcmgr, outfp, codec=codec, scale=scale,
                               layoutmode=layoutmode, laparams=laparams,
                               imagewriter=imagewriter)
    elif outtype == 'tag':
        device = TagExtractor(rsrcmgr, outfp, codec=codec)
    
    
    fp = file(srcFile, 'rb')
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    
    for page in PDFPage.get_pages(fp, pagenos,
                                    maxpages=maxpages, password=password,
                                    caching=caching, check_extractable=True):
        page.rotate = (page.rotate+rotation) % 360
        interpreter.process_page(page)
    
    fp.close()
    device.close()
    outfp.close()
    fp = open(outfile, "r")
    data = fp.read()
    fp.close()
    
    if data[:3] == codecs.BOM_UTF8 :  
        data = data[3:]  
    
    '''英文论文'''
    
    position = find_last(data, "REFERENCES")
    refstr = data[position + 10:]    
    
    #refstr = open("ref.txt", "r").read()
    '''英文论文'''
    
    references = re.split("\n\d+.", refstr)
   

    '''中文论文'''
    '''
    position = find_last(data, "参考文献")
    refstr = data[position + 13:]

    references = re.split("\[\d+\]", refstr)
    
    fp = open("ref.txt", "w")
    fp.write(refstr)
    fp.close()
    '''
    
    
    '''
    for ref in references :
        print ref.decode("utf8").encode("gbk")
        print "\n"
    print len(references)
    '''

    fp = open("title.txt", "w")
    num = 0
    for ref in references :
        ''' 
        str = ref.split(".") 
        if len(str) > 1 :       
            str[1] = str[1].replace("\n", " ")
            str[1] = re.subn("\[\w\]", "", str[1])           
            fp.write(str[1][0].strip())
            fp.write("\n")        
            #num += 1
        '''     
        str = re.split("\(\d+\)", ref)
        if len(str) > 1 :
            str = str[1].split(".")                           
            str[0] = str[0].replace("\n", "")                      
            fp.write(str[0].strip())
            fp.write("\n")        
            #num += 1    
           
    fp.close()
    #print num

    

'''把题录写入文件'''
def writeBibliography(url, fp1, fp2) :
    import urllib2 
    import time   
    f = urllib2.urlopen(url)
    time.sleep(3)
    data = f.read() 
    fp1.write(data)    
    fp1.write("\n\n")
    fp2.write(data)    
    fp2.write("\n\n")
    
    

'''下载题录信息'''
def downloadBibliography() :
    from Bio import Entrez    
    import re
    from Bio import Medline
    Entrez.email = "904173120@qq.com"
    fp1 = open("SNP_pubmed_result.txt", "a")
    fp2 = open("new_pubmed_result.txt", "w")
    '''
    all_text_tatol = fp1.read()
    all_text_new = fp2.read()
    '''
    
    input = open("SNP_pubmed_result.txt")
    medline_exist = Medline.read(input)
    input.close()
    for line in open("title.txt", "r").readlines()[:5] :     
        title = line.replace("\n", "")
        handle = Entrez.esearch(db="pubmed", term=title)
        records = Entrez.read(handle)
        if int(records["Count"]) == 1 :
            term = re.sub(" ", "+", title)
            url = "https://www.ncbi.nlm.nih.gov/pubmed/?term="
            url += ''.join(term)
            url += ''.join("&report=medline&format=text")
            medline_handle = Entrez.efetch(db="pubmed", id=records["IdList"], rettype="medline" , retmode="text")
            medline_res = Medline.parse(medline_handle)   
            medline_res_list = list(medline_res)
            PMID = -1
            for record in medline_res_list :
                PMID = record.get("PMID", "?")   
            '''      
            if len(all_text_tatol) == 0 :
                writeBibliography(url, fp1, fp2)
            else :       
            '''              
            if PMID not in medline_exist["PMID"] :
                writeBibliography(url, fp1, fp2)
    fp1.close()
    fp2.close()
'''
abstract_handle = Entrez.esummary(db="pubmed", id=records["IdList"])
records = Entrez.read(abstract_handle)
url = "http://moscow.sci-hub.cc/1384f9ebe3e631236f4bc6f973e8e520/jobling2003.pdf"

import urllib2
f = urllib2.urlopen(url)
data = f.read()
pdfName = title + ".pdf" 
with open(pdfName, "a") as line: 
    line.write(data)


import re, urllib
html_url = "https://www.ncbi.nlm.nih.gov/pmc/articles/pmid/21897858/"    
response = urllib.urlopen(html_url) 
data = response.read() 
print data
f = open("out.html","w")  
f.write(data)  
linksList = re.findall('<a href=(.*?)>.*?</a>',data.decode('utf-8'))
for link in linksList:
    print (link)
'''

if __name__ == "__main__" : 
    #getPDFReferencesTitle()
    #print "asd"
    downloadBibliography()




    



