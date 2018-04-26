'''
USAGE 1: python directConverter.py x.std y.seq
OUTPUT: z.glm
(Uses milToGridlab.py)

USAGE 2: python directConverter.py x.mdb
OUTPUT: y.glm
(Uses cymeToGridlab.py)

'''
from os.path import exists, splitext
from os import getcwd
import argparse, sys

sys.path.append('../')
import milToGridlab as mil
import cymeToGridlab as cyme
import feeder

def handleMilFile(std_path, seq_path, failure = False):
  ''' Conversion routine for the std and seq files. '''
    # Attempt to open std and seq files and convert to glm.
  try:
    with open(std_path, 'r') as std_file, open(seq_path, 'r') as seq_file:
      output_path = std_path.split('/')[-1].replace('.std', '.glm') # We wish to put the file in the current running directory.
      output_file = open(output_path, 'w')
      glm, x_scale, y_scale = mil.convert(std_file, seq_file)
      output_file.write(feeder.sortedWrite(glm))
      print 'GLM FILE WRITTEN FOR STD/SEQ COMBO.'
  except IOError:
    print 'UNABLE TO WRITE GLM FILE.'
    failure = True
  finally:
    output_file.close()
  return failure
  

def handleMdbFile(mdb_path, modelDir, failure = False):
  ''' Convert mdb database to glm file. '''
  try:
    with open(mdb_path, 'r') as infile:
      output_path = mdb_path.split('/')[-1].replace('.mdb', '.glm')
      output_file = open(output_path, 'w')
      glm, x_scale, y_scale = cyme.convertCymeModel(mdb_path, modelDir)
      output_file.write(feeder.sortedWrite(glm))
  except IOError:
    print 'UNABLE TO WRITE GLM FILE.'
    failure = True
  except:
    print 'ERROR IN CYME MODEL FUNCTION.', sys.exc_info()[0]
    failure = True
  finally:
    output_file.close()
  return failure
  
def is_valid_file(parser, file_name):
  ''' Check validity of user input '''
  valid_names = ["mdb", "seq", "std"]

  # Check to see that file exists. 
  if not exists(file_name):
    parser.error("FILE %s DOES NOT EXIST." % file_name)
  suffix = splitext(file_name)[1][1:]

  # Check to ensure that no invalid name is being passed.
  if suffix not in valid_names:
    parser.error("FILE SUFFIX FOR %s INVALID." % file_name)

  print "VALID MATCH CONFIRMED FOR FILE %s." % file_name
  return file_name


def main():

  parser = argparse.ArgumentParser()
  parser.add_argument("-std", help="Single std file. Must go with seq file.", type=lambda f: is_valid_file(parser, f))
  parser.add_argument("-seq", help="Single seq file. Must go with std file.", type=lambda f: is_valid_file(parser, f))
  parser.add_argument("-mdb", help="Single mdb file, with both network and database exported to the same file.", type=lambda f: is_valid_file(parser, f))
  args = parser.parse_args()

  if (args.std and args.seq):
    handleMilFile(args.std, args.seq)
  elif (args.mdb):
    home_folder = '../' + getcwd()
    handleMdbFile(args.mdb, home_folder)
  else:
    raise Exception("INVALID FILE INPUT.")

if __name__ == "__main__":
  main()