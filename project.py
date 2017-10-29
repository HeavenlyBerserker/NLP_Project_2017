


import os
import nltk

def main():
    filedir='developset/texts'
    for filename in os.listdir(filedir):
        print (filename)
        print ("###############################################################")
        
        answer=find(filename, 'developset/answers')
        with open(answer+".anskey", 'r') as input_file:
            prevrole=""
            for line in input_file:
                if ":" in line:
                    linecontent=line.split(":")
                    if linecontent[1].lstrip()!="-":
                        role=linecontent[0]
                        if "/" in linecontent[0]:
                            filler_elements=linecontent[0].split("/")
                            for i in range(0,len(filler_elements)):
                                each_entry=filler_elements[i].lstrip().rstrip()
                                create_pattern(each_entry, filedir, filename)
                        else:
                            each_entry=linecontent[1].lstrip().rstrip()
                            create_pattern(each_entry, filedir, filename)
                            
                        prevrole=role
  
                else:
                    content=line.lstrip().rstrip()
                    if "/" in content:
                        filler_elements=content.split("/")
                        for i in range(0,len(filler_elements)):
                            each_entry=filler_elements[i].lstrip().rstrip()
                            create_pattern(each_entry, filedir, filename)
                    else:
                        each_entry=content.lstrip().rstrip()
                        create_pattern(each_entry, filedir, filename)
                        
                    role=prevrole
                
                

        #print filename
        #print answer
        
        
def create_pattern(each_entry, filedir, txt_file_name):
    with open(filedir+"/"+txt_file_name, 'r') as textfile:
        text=textfile.read()
        sents=nltk.sent_tokenize(text)
        for i in range(0, len(sents)):
            if each_entry in sents[i]:
                print (sents[i])
                #todo
        
    




def find(name, path):
    for root, dirs, files in os.walk(path):
        if name+".anskey" in files:
            return os.path.join(root, name)





if __name__ == "__main__":
    main()
