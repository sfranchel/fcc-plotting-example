import argparse

from podio import root_io
import ROOT

##################
# Option parser

def parse_args():
    parser = argparse.ArgumentParser(
        description='plot_hits.py',
        epilog='Example:\nplot_hits.py -i ALLEGRO_sim_hits.root',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('-i', '--input',
                        type=str,
                        default='ALLEGRO_sim_hits.root',
                        help='Input ROOT file containing hit data')

    return (parser.parse_args())

options = parse_args()

input_file = options.input

##################
# Prepare histograms

h_hit_t = ROOT.TH1D("h_hit_t", "hist_hit_t; Time [ns]", 200, 0, 20)
h_hit_E = ROOT.TH1D("h_hit_E", "h_hit_E; Energy [MeV]; Hits", 500, 0, 50)


##################
# Read hits

hit_collection_name = "SiWrBCollection" # sim hits collection name for Silicon Wrapper Barrel
#hit_collection_name = "SiWrBDigis" # digitized hits

podio_reader = root_io.Reader(input_file)

# Get metadata and cell ID decoder
metadata = podio_reader.get("metadata")[0]
id_encoding = metadata.get_parameter(hit_collection_name+"__CellIDEncoding")
decoder = ROOT.dd4hep.BitFieldCoder(id_encoding)

# Loop over events
for i,event in enumerate(podio_reader.get("events")):

    #print("processing event:", i) # can be useful for debugging

    # Loop over the hit collection
    for hit in event.get(hit_collection_name):

        # cell_id = hit.getCellID() # maybe useful later
        hit_energy = hit.getEnergy() * 1e3 # convert to MeV
        hit_time = hit.getTime()

        # fill the histograms
        h_hit_E.Fill(hit_energy)
        h_hit_t.Fill(hit_time)


##################
# Save histograms

output_file_name = input_file.replace(".root", "_histograms.root")
output_file = ROOT.TFile(output_file_name, "RECREATE")

h_hit_t.Write()
h_hit_E.Write()

output_file.Close()

print("Histograms saved to:", output_file_name)

