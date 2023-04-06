import numpy
import pandas

class SerialStub:

    def __init__(self, port):
        self.name = port + "_stub"
        self.sample = numpy.random.choice(['rood', 'groen', 'blauw'], 
                                         size = 15).tolist()
        for i in range(5):
            self.sample.append('leeg')

        print("stub sample")
        print(self.sample)
        self.count = 0
    
    def write(self, str):
        # print(self.name, ": ", str)
        if(str == "e".encode()): # eject marble, so count + 1 
            self.count += 1
     
    default_mean_RGB_df = pandas.DataFrame(
        [
            {'R': 118.2, 'G': 67., 'B': 59.},
            {'R': 87.6, 'G': 85, 'B': 66.},
            {'R': 76.5, 'G': 83.75, 'B': 80.75},
            {'R' : 93., 'G' : 79., 'B' : 66.25}
        ],
        index=['rood', 'groen', 'blauw', 'leeg']
    )

    def readline(self):
        color = self.sample[self.count]
        rgb = SerialStub.default_mean_RGB_df.loc[color].to_numpy()
        val = numpy.array2string(rgb, separator = ",") .replace('[','') .replace(']','')
        print("Read ", val, "(", self.count, ")")
        #self.count += 1
        return(val)

    def flushInput(self): # Don't need buffers in simulation
        None

    def flushOutput(self): # Don't need buffers in simulation
        None
