import sys, re, argparse

def domtblout_filtering(domtblout, outfile, given_evalue, given_coverage):
	header         = "#target\tt_len\tquery\tq_len\t"+\
                         "E-value\tscore\tc-Evalue\tscore\t"+\
                         "hmm_from\thmm_to\tdomain_from\tdomain_to"
	open_domtblout = open(domtblout, 'r')
	best_hit       = {}
	hit            = []
	record         = ""
	for line in open_domtblout:
		line   = line.rstrip('\n')
		if not line.startswith('#'):
			record  = line
			hit     = record.split()
			query   = hit[3]
			cEvalue = hit[11]
			if hit[3] in best_hit:
				if float(hit[11]) < float(best_hit[hit[3]][11]):
					best_hit[hit[3]] = hit
			else: best_hit[hit[3]] = hit
	open_domtblout.close()

	open_outfile       = open(outfile, 'w')
	open_outfile.write(header+'\n')
	for value in best_hit.values():
		target     = value[0]
		tlen       = int(value[2])
		query      = value[3]
		evalue     = float(value[6])
		cEvalue    = float(value[11])
		hmm_from   = int(value[15])
		hmm_to     = int(value[16])
		m_alignLen = abs(hmm_to-hmm_from)
		g_coverage = int(tlen)*float(given_coverage)
		if (evalue<float(given_evalue)) and (m_alignLen>float(g_coverage)):
			record     = value[0]     + '\t' + value[2]  + '\t' + value[3]  + '\t' + value[5]  + '\t' + str(evalue) + '\t' + value[7] + '\t' +\
                                     str(cEvalue) + '\t' + value[13] + '\t' + value[15] + '\t' + value[16] + '\t' + value[17]   + '\t' + value[18]
			open_outfile.write(record+'\n')
	open_outfile.close()

def main():
	arg_parser = argparse.ArgumentParser(description="Filtering .domtblout file from pHMM search")
	arg_parser.add_argument("-i", dest="domtblout", action="store", required=True, help="input domtblout file (required)")
	arg_parser.add_argument("-o", dest="outfile", action="store", required=True, help="output domtblout file (required)")
	arg_parser.add_argument("-e", "--evalue", dest="given_evalue", type=float, default=1e-130, help="threshold for e-value")
	arg_parser.add_argument("-c", "--coverage", dest="given_coverage", type=float, default=0.5, help="threshold for model coverage")
	args = arg_parser.parse_args()
	domtblout_filtering(args.domtblout, args.outfile, args.given_evalue, args.given_coverage)

if __name__ == "__main__":
	main()
