from os import walk
import string

list_ID = list(string.ascii_uppercase)

out = open("data/evaluate/setting_opinosis.xml","w")
header = "<ROUGE_EVAL version=\"1.55\">\n"


out.write(header)

mypath = "data/summary"

list_topics = []
for (dirpath, dirnames, filenames) in walk(mypath):
    list_topics.extend(filenames)

number_topic = len(list_topics)

for i in range(number_topic):
    out.write("\t<EVAL ID=\""+str(i) + "\">\n")
    model_root = "\t\t<MODEL-ROOT>\n \t\t\t model \n\t\t</MODEL-ROOT>\n"
    out.write(model_root)
    peer_root = "\t\t<PEER-ROOT>\n\t\t\tpeer \n\t\t</PEER-ROOT>\n"
    out.write(peer_root)
    input_format = "\t\t<INPUT-FORMAT TYPE=\"SPL\">\n\t\t</INPUT-FORMAT>\n"
    out.write(input_format)

    # move summary to peer
    peer = open("data/evaluate/peer/"+list_topics[i],mode = "w+")
    summary = open("data/summary/"+list_topics[i],mode = "r")
    peer.write(summary.read())

    peerstring = "\t\t<PEERS>\n\t\t\t<P ID=\"1\">" + list_topics[i]+" </P> \n\t\t</PEERS>\n"
    out.write(peerstring)
    peer.close()
    summary.close()
    # move gold corpus to model

    list_docs = []
    for (dirpath, dirnames, filenames) in walk("data/goldvn/"+(list_topics[i])[:-9]):
        list_docs.extend(filenames)
    number_doc = len(list_docs)
    out.write("\t\t<MODELS>\n")
    for j in range(number_doc):
        #move goldvn_sum into model
        model = open("data/evaluate/model/"+list_docs[j],"w+")
        summary = open("data/goldvn/"+(list_topics[i])[:-9] + "/" + list_docs[j],"r")
        model.write(summary.read())

        out.write("\t\t\t<M ID=\"" +list_ID[j] +"\" >" + list_docs[j] + "</M>\n")

        model.close()
        summary.close()


    out.write("\t\t</MODELS>\n")
    out.write("\t</EVAL>\n")

out.write("</ROUGE_EVAL>")

out.close()

