import sys, os, argparse, glob, time, re
from sklearn.model_selection import LeaveOneOut

# Pre-installed programs
# HMMER3.0 packages (v3.1b2)
# Clustal Omega (v.1.2.4)

def init(text):
	return int(text) if text.isdigit() else text

def natural_keys(text):
	return [ init(c) for c in re.split('(\d+)', text) ]

def GET_SEQUENCE_IDs(fasta):
	open_fasta   = open(fasta, 'r')
	seqID_list   = []
	for line in open_fasta:
		line = line.rstrip('\n')
		if line.startswith('>'):
			seqID = line.split()[0].lstrip('>')
			seqID_list.append(seqID)
	open_fasta.close()

	return seqID_list

def GET_SEQS(fasta, seq_index, outfile):
	flag         = False
	open_outfile = open(outfile, 'w')
	for i in seq_index:
		count        = 0
		open_fasta   = open(fasta, 'r')
		for line in open_fasta:
			line = line.rstrip('\n')
			if line.startswith('>'):
				if flag and c_seq != "":
					open_outfile.write(c_seq+'\n')
				w_header = line
				flag     = False
				if count == i:
					flag = True
				if flag:
					open_outfile.write(w_header+'\n')
				c_seq  = ""
				count += 1
			elif flag:
				c_seq += line
		if flag and c_seq != "":
			open_outfile.write(c_seq+'\n')
		open_fasta.close()
	open_outfile.close()

def LEAVE_ONE_OUT(fasta, seqID_list):
	loo           = LeaveOneOut()
	count         = 1
	outfileprefix = fasta.split('/')[-1].split('.')[0]
	for train_index, test_index in loo.split(seqID_list):
		open_train_outfile = 'training_set_'+str(count)+'.faa'
		open_test_outfile  = 'test_set_'+str(count)+'.faa'
		train_seqs         = GET_SEQS(fasta, train_index, open_train_outfile)
		test_seqs          = GET_SEQS(fasta, test_index, open_test_outfile)
		count             += 1

def RUN_MSA():
	faaList = []
	for f in glob.iglob("training_set*.faa"):
		faaList.append(f)
	for i in range(len(faaList)):
		outfilename = faaList[i].split('/')[-1].split('.')[0] + '.sto'
		msa_cmd = "/home/jhjeon/clustalo -i " + faaList[i] + " -o " + outfilename + " --outfmt st"
		os.system(msa_cmd)

def RUN_HMMBUILD():
	"Running hmmbuild ..."
	for f in glob.iglob("training_set*.sto"):
		outfilename  = f.split('/')[-1].split('.')[0] + '.hmm'
		hmmbuild_cmd = "/program/hmmer-3.1b2-linux-intel-x86_64/binaries/hmmbuild " +\
                               outfilename + ' ' + f 
		os.system(hmmbuild_cmd)

def RUN_HMMPRESS():
	for f in glob.iglob("training_set*.hmm"):
		hmmpress_cmd = "/program/hmmer-3.1b2-linux-intel-x86_64/binaries/hmmpress " + f 
		os.system(hmmpress_cmd)

def RUN_HMMSCAN():
	hmmList  = []
	testList = []
	for hmm in glob.iglob("*.hmm"):
		hmmList.append(hmm)
	for test in glob.iglob("test_set*.faa"):
		testList.append(test)
	
	hmmList.sort(key=natural_keys)
	testList.sort(key=natural_keys)

	for i in range(len(hmmList)):
		outfileprefix = hmmList[i].split('/')[-1].split(".hmm")[0]+'_'+\
                                testList[i].split('/')[-1].split(".faa")[0]
		hmmscan_cmd   = "/program/hmmer-3.1b2-linux-intel-x86_64/binaries/hmmscan "    + \
                                " --cpu 0 --domtblout hmmscan_" + outfileprefix + ".domtblout" + \
                                " -o hmmscan_" + outfileprefix + ".stdout "                    + \
                                hmmList[i] + ' ' + testList[i] + " &"
		os.system(hmmscan_cmd)

def main():
	arg_parser = argparse.ArgumentParser(description="Leave-one-out cross validation using hmmscan.")
	arg_parser.add_argument("--fasta", dest="fasta", action="store", required=True, help="input FASTA file (only protein sequences)")
	args       = arg_parser.parse_args()
	seqID_list = GET_SEQUENCE_IDs(args.fasta)
	LEAVE_ONE_OUT(args.fasta, seqID_list)
	RUN_MSA()
	RUN_HMMBUILD()
	RUN_HMMPRESS()
	RUN_HMMSCAN()

if __name__ == "__main__":
	main()
