import os
from KafNafParserPy import *

summary=open("summary.csv", "w")
details=open("details.csv", "w")
details.write("\tFILENAME\t\t\t\tNER_PREC\tNER_RECALL\tNED_PREC\tNED_RECALL\n")
summary.write("NER_PREC\tNER_RECALL\tNED_PREC\tNED_RECALL\n")

# NER
ner_tp=0
ner_fn=0 # In GOLD, not in spotlight_v1
ner_fp=0 # Not in GOLD, yes in spotlight_v1

# NED
ned_tp=0 # Both in GOLD and spotlight_v1
ned_fn=0 # In GOLD, not in spotlight_v1
ned_fp=0 # Not in GOLD, yes in spotlight_v1

for f in os.listdir("corpus"):
	
	print f
	my_parser=KafNafParser("corpus/" + f)

	# NER
	file_ner_tp=0 
        file_ner_fn=0 # In GOLD, not in spotlight_v1
        file_ner_fp=0 # Not in GOLD, yes in spotlight_v1

	# NED
	file_ned_tp=0 # Both in GOLD and spotlight_v1
	file_ned_fn=0 # In GOLD, not in spotlight_v1
	file_ned_fp=0 # Not in GOLD, yes in spotlight_v1

	file_total=0 # Total occurrences

	for entity in my_parser.get_entities():
		print entity.get_id()
		goldrefs=[]
		maxconf=-0.1
		maxref=None
		for extref in entity.get_external_references():
			if extref.get_resource()=="spotlight_v1":
				print extref.get_confidence()
				if float(extref.get_confidence())>maxconf:
					maxconf=float(extref.get_confidence())
					maxref=extref.get_reference()
			elif extref.get_resource()=="GOLD":
				goldrefs.append(extref.get_reference())
		if maxref in goldrefs:
			print "COrrect", maxref, goldrefs
			file_ned_tp+=1
			file_ner_tp+=1
		elif maxref==None:
			file_ned_fn+=1
                        file_ner_fn+=1
                        print "Bzz.. wrong", maxref, goldrefs
		elif '-NAE-' in goldrefs:
			file_ned_fp+=1
                        file_ner_fp+=1
                        print "Bzz.. wrong", maxref, goldrefs
		else:
			file_ned_fp+=1
			file_ned_fn+=1
			file_ner_tp+=1
			print "Bzz.. wrong", maxref, goldrefs
		file_total+=1
	
	# 
	ner_tp+=file_ner_tp
        ner_fp+=file_ner_fp
        ner_fn+=file_ner_fn
        ned_tp+=file_ned_tp
        ned_fp+=file_ned_fp
        ned_fn+=file_ned_fn

	print "NED SCORES:"
	file_ned_prec=file_ned_tp*1.0/(file_ned_tp+file_ned_fp)
	file_ned_recall=file_ned_tp*1.0/(file_ned_tp+file_ned_fn)
	print file_ned_prec, file_ned_recall
	print "NER SCORES:"
        file_ner_prec=file_ner_tp*1.0/(file_ner_tp+file_ner_fp)
        file_ner_recall=file_ner_tp*1.0/(file_ner_tp+file_ner_fn)
        print file_ner_prec, file_ner_recall
	details.write("%s\t%s\t%s\t%s\t%s\n" % (f, file_ner_prec, file_ner_recall, file_ned_prec, file_ned_recall))

#### Overall summary numbers ####
ned_prec=ned_tp*1.0/(ned_tp+ned_fp)
ned_recall=ned_tp*1.0/(ned_tp+ned_fn)
ner_prec=ner_tp*1.0/(ner_tp+ner_fp)
ner_recall=ner_tp*1.0/(ner_tp+ner_fn)
summary.write("%s\t%s\t%s\t%s\n" % (ner_prec, ner_recall, ned_prec, ned_recall))