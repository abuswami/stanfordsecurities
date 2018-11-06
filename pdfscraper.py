
import requests
from bs4 import BeautifulSoup
import urllib2
from urllib2 import Request
import unicodedata


# Open stanford.securities.edu


def downloadPDFS(r):
    getRootURL = requests.get(r)
    # Create array of links from rootURL
    pageLinks = []
    soup = BeautifulSoup(getRootURL.content, "html5lib")
    test = soup.find_all("tr", {"class": "table-link"})

    for row in test:
        pageLinks.append(row.get("onclick"))

    pdfLinks = []

    ## Format pageLinks

    formattedPageLinks = []
    for page in pageLinks:
        newPage = page.replace("window.location='filings-case.html","")
        formattedPageLinks.append(newPage)


    caseURL = "http://securities.stanford.edu/filings-case.html"
    pdfLinks = []

    for samplepageURL in formattedPageLinks:
        newURL = caseURL + samplepageURL
        strNewUrl = unicodedata.normalize('NFKD', newURL).encode('ascii','ignore')
        strNewUrl = strNewUrl[:-1]
        getsamplePageURL = requests.get (strNewUrl)
        pagegetsamplePageURL = BeautifulSoup(getsamplePageURL.content, "html5lib")
        pagesamplePageTest = pagegetsamplePageURL.find_all("tr", {"class":"table-link"})

        for pages in pagesamplePageTest:
            pdfLinks.append(pages.get("onclick"))


    complaintPDFS = pdfLinks[::2]
    complaintURL = "http://securities.stanford.edu/filings-documents/"
    finalPdfLinks = []


    for complaintPDF in complaintPDFS:
        newComplaintLink = complaintPDF.replace("window.location='filings-documents/","")
        newComplaintLink = newComplaintLink[:-1]
        newComplaintLink = unicodedata.normalize('NFKD', newComplaintLink).encode('ascii','ignore')
        finalPdfLink = complaintURL + newComplaintLink
        finalPdfLinks.append(finalPdfLink)

    filenumber = 0
    for finaldocumentLinks in finalPdfLinks:
        filename = "test"
        filesuffix = ".pdf"
        fullFileName = filename + str(filenumber) + filesuffix
        openDoc = requests.get(finaldocumentLinks, stream=True)
        with open('downloadedPDFs/'+fullFileName,'wb') as fd:
            fd.write(openDoc.content)
        filenumber = filenumber + 1

rootURL = "http://securities.stanford.edu/filings.html"
numPages = 257
rootURLSuff = "?page="
startPage = 1
currentPage = 1
rootURLS = []
for rootURLs in range(startPage,numPages):
    rootURLS.append(rootURL + rootURLSuff + str(currentPage))
    currentPage = currentPage + 1


for finalURL in rootURLS:
    downloadPDFS(finalURL)
