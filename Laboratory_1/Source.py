from zeep import Client
import os

client_PoSTagger = Client("http://nlptools.info.uaic.ro/WebPosRo/PosTaggerRoWS?wsdl")
result_XML = client_PoSTagger.service.parseText_XML(open("Data.txt", "r").read())
print(result_XML)
client_FDGParser = Client("http://nlptools.info.uaic.ro/WebFdgRo/FdgParserRoWS?wsdl")
result_XML = client_FDGParser.service.parseText(open("Data.txt", "r").read())
print(result_XML)

